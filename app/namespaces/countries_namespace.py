from flask import request
from flask_restplus import Namespace, Resource, abort

from app.utils.exceptions import OdooIsDeadError

api_country = Namespace('countries', description='Request to odoo countries.')


@api_country.route("/")
class Country(Resource):

    def get(self):
        """Get all countries from odoo.
        """
        from app.controllers.odoo_controller import OdooController
        try:
            response = OdooController.get_odoo_countries()
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')
        return response
