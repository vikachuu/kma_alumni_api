from flask import render_template_string
from flask_restplus import Namespace, Resource


api_health = Namespace('health', description='Test app health')


@api_health.route("/")
class Health(Resource):

    def get(self):
        """
        Test health
        """

        return {"status": "ok"}