from flask import request
from flask_restplus import Namespace, Resource, abort

from app.utils.exceptions import OdooIsDeadError

api_company = Namespace('companies', description='Request to odoo companies.')


@api_company.route("")
class Company(Resource):

    def get(self):
        """Get all companies from odoo.
        """
        from app.controllers.odoo_controller import OdooController
        return OdooController.get_odoo_companies()
