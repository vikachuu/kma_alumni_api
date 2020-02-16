from flask import request
from flask_restplus import Namespace, Resource


api_alumni = Namespace('alumni', description='Requests to alumni model')


@api_alumni.route("/")
@api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',
                    'tag': 'Filter by tag from Odoo contact. For example - \'Alumni\''})
class Alumni(Resource):

    def get(self):
        """
        Return all alumni
        """

        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 1)
        tag = query_params.get('tag')

        filter_list = []
        filter_list.append(['is_company', '=', False])
        filter_list.append(['category_id', '=', tag]) if tag else None

        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [filter_list],
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920'],
                'offset': int(offset),
                'limit': int(limit)})

        return contacts
