from flask import request
from flask_restplus import Namespace, Resource, fields


api_operator = Namespace('operator', description='Requests to operator model.')

operator_fields = api_operator.model('CReate operator payload.', {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
})

@api_operator.route("/")
class Operator(Resource):

    @api_operator.doc(body=operator_fields)
    def post(self):
        """Create operator user.
        """
        from app.controllers.operator_controller import OperatorController
        post_data = request.get_json()
        return OperatorController.create_operator_user(post_data)


@api_operator.route("/<operator_id>")
class OperatorId(Resource):

    @api_operator.doc(params={
                    'operator_id': 'An operator id.',})
    def get(self, operator_id):
        """Get operator by id.
        """
        from app.controllers.operator_controller import OperatorController
        return OperatorController.get_operator_by_id(operator_id)
