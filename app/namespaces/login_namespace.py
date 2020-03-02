from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token


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
                "data": None,
                "status": 401,
                "error": "No alumni user with such an email exists."
            }

        if not alumni.check_password(password):
            return {
                "data": None,
                "status": 401,
                "error": "Wrong password."
            }
        
        # if user exists get data from odoo contact and create access token for the user
        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contact = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                    [[['id', '=', int(alumni.odoo_contact_id)],]],
                    {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                    'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                    'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                    'image_1920'],})

        # return alumni data
        contact[0].update({
            "alumni_uuid": alumni.alumni_uuid,
            "password": alumni.password,
            "user_confirmed": alumni.user_confirmed,
        })

        return {
            "data": {
                "alumni": contact,
                "access_token": create_access_token(identity=alumni.email),
                "refresh_token": create_refresh_token(identity=alumni.email)
            },
            "status": 200,
            "error": None
        }
