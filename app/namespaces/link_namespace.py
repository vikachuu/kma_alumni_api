import os
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from flask_restplus import Namespace, Resource


api_register_link = Namespace('register_link', description='Requests to get link to register.')


def encode_token(odoo_contact_id):
    key = os.getenv('SECRET_FERNET_KEY')
    f = Fernet(key.encode('utf-8'))
    token = f"{odoo_contact_id} {datetime.now() + timedelta(days=7)}"  # add expiration date
    token = f.encrypt(token.encode('utf-8'))
    return token.decode('utf-8')



@api_register_link.route("/<odoo_contact_id>")
@api_register_link.doc(params={'odoo_contact_id': 'An Odoo contact id.'})
class RegisterLink(Resource):

    def get(self, odoo_contact_id):
        """Return generated unique link for alumni to register. Link will be expired in 1 week.
        """
        # check if such odoo user exists
        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts_number = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_count',
                [[['id', '=', odoo_contact_id], ]])

        if contacts_number == 0:
            return {"data": {
                        "token": None
                        },
                    "status": 404,
                    "error": f"Contact with id {odoo_contact_id} does not exist."
                    }

        # encrypt odoo user id
        token = encode_token(odoo_contact_id)

        # create/update record in alumni invite status
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        put_data = {
            "odoo_contact_id": odoo_contact_id,
            "invite_status": "invited"
        }
        response = AlumniInviteStatusController.update_invite_status_record(put_data)

        return {"data": {
                        "token": token
                        },
                "status": 200,
                "error": None
                }
