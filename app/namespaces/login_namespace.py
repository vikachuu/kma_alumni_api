from flask import request
from flask_restplus import Namespace, Resource, fields, abort
from flask_jwt_extended import create_access_token, create_refresh_token

from app.utils.exceptions import OdooIsDeadError


api_login = Namespace('login', description='Login to alumni service.')

login_fields = api_login.model('Login alumni payload.', {
    "email": fields.String,
    "password": fields.String,
})


@api_login.route("/")
class Login(Resource):

    @api_login.doc(body=login_fields)
    def post(self):
        """
        Login to alumni service.
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        from app.controllers.alumni_controller import AlumniController
        alumni = AlumniController.get_alumni_user_by_email(email)

        if alumni is None:
            return {
                "error_id": "alumni_login_wrong_email_error",
                "message": "Unauthorized: wrong email."
                }, 401

        if not alumni.check_password(password):
            return {
                "error_id": "alumni_login_wrong_password_error",
                "message": "Unauthorized: wrong password."
                }, 401
        
        # if user exists get data from odoo contact and create access token for the user
        filter_list = []
        filter_list.append(['id', '=', int(alumni.odoo_contact_id)])

        from app.controllers.odoo_controller import OdooController
        try:
            contact = OdooController.get_odoo_contacts_by_filter_list(filter_list, 0, 0)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        if not contact:
            return {
                "error_id": "odoo_contact_not_found_error",
                "message": "Odoo contact not found."
                }, 404

        # return alumni data
        contact[0].update({
            "alumni_uuid": alumni.alumni_uuid,
            "user_confirmed": alumni.user_confirmed,
        })

        return {
            "alumni": contact,
            "access_token": create_access_token(identity=alumni.email),
            "refresh_token": create_refresh_token(identity=alumni.email)
            }, 200
