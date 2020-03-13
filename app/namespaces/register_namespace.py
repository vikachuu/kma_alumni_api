import os
from datetime import datetime
from dateutil import parser

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
    return contact_id, parser.parse(expiration_date)


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
        filter_list = []
        filter_list.append(['id', '=', odoo_contact_id])
        from app.controllers.odoo_controller import OdooController
        contacts_number = OdooController.count_number_of_odoo_contacts_by_filter_list(filter_list)

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
            # delete record in alumni invite status
            from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
            AlumniInviteStatusController.delete_invite_status_record(odoo_contact_id)

            # send email for confirmation
            receiver_email = response['data']['alumni']['email']
            alumni_uuid = response['data']['alumni']['alumni_uuid']
            send_confirmation_email(receiver_email, alumni_uuid)

        return response
