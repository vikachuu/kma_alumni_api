from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token


api_operator_login = Namespace('operator_login', description='Login operator.')

operator_login_fields = api_operator_login.model('Login operator payload.', {
    "email": fields.String,
    "password": fields.String,
})

@api_operator_login.route("/")
class OperatorLogin(Resource):

    @api_operator_login.doc(body=operator_login_fields)
    def post(self):
        """
        Operator login to alumni service.
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        from app.controllers.operator_controller import OperatorController
        operator  = OperatorController.get_operator_by_email(email)

        if operator is None:
            return {
                "error": "Wrong email.",
                "message": "Unauthorized: wrong email."
                }, 401

        if not operator.check_password(password):
            return {
                "error": "Wrong password.",
                "message": "Unauthorized: wrong password."
                }, 401

        return {
            "operator": {
                "operator_id": operator.operator_id,
                "username": operator.username,
                "email": operator.email,
                "is_admin": operator.is_admin,
                },
            "access_token": create_access_token(identity=operator.email),
            "refresh_token": create_refresh_token(identity=operator.email)
            }, 200
