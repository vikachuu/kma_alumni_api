import os
from datetime import datetime

from flask import request
from flask_restplus import Namespace, Resource, fields
from cryptography.fernet import Fernet

from app.utils.email_sender import send_confirmation_email


api_register = Namespace("register", description="Request to sign up new alumni.")

register_fields = api_register.model('Register alumni payload.', {
    "odoo_contact_token": fields.String,
    "email": fields.String,
    "password": fields.String,
})


def decode_token(token):
    key = os.getenv('SECRET_FERNET_KEY')
    f = Fernet(key.encode('utf-8'))
    token = f.decrypt(token.encode('utf-8'))
    contact_id, expiration_date = token.decode('utf-8').split(" ", 1)
    return contact_id, datetime.fromisoformat(expiration_date)


@api_register.route("/")
class Register(Resource):

    @api_register.doc(body=register_fields)
    def post(self):
        """Register new alumni user.
        """
        post_data = request.get_json()

        # decode token and check if expired
        token = post_data.get('odoo_contact_token')
        odoo_contact_id, expiration_date = decode_token(token)

        if datetime.now() > expiration_date:
            return {"data": {
                        "token": token
                        },
                    "status": 401,
                    "error": "Registration link is expired."
                    }

        # check if such odoo user exists 
        # TODO: move to a separate controller
        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts_number = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_count',
                [[['id', '=', odoo_contact_id], ]])

        if contacts_number == 0:
            return {"data": {
                        "token": token
                        },
                    "status": 404,
                    "error": f"Contact does not exist."
                    }

        # create alumni user
        from app.controllers.alumni_controller import AlumniController
        post_data.update({'odoo_contact_id': odoo_contact_id})
        response = AlumniController.create_alumni_user(post_data)

        
        if response.get("status") == 201:
            # update record in alumni invite status to registered
            from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
            put_data = {
                "odoo_contact_id": odoo_contact_id,
                "invite_status": "registered"
            }
            AlumniInviteStatusController.update_invite_status_record(put_data)

            # send email for confirmation
            receiver_email = response['data']['alumni']['email']
            alumni_uuid = response['data']['alumni']['alumni_uuid']
            send_confirmation_email(receiver_email, alumni_uuid)

        return response
