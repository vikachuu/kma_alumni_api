from flask_restplus import Namespace, Resource


api_alumni = Namespace('alumni', description='Requests to alumni model')


@api_alumni.route("/")
class Alumni(Resource):

    def get(self):
        """
        Return all alumni
        """

        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [[['is_company', '=', False]]], 
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920']})

        return contacts
