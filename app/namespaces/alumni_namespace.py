from flask import request
from flask_restplus import Namespace, Resource


api_alumni = Namespace('alumni', description='Requests to alumni model')


@api_alumni.route("/")
@api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',
                    'tag': 'Filter by tag from Odoo contact. For example - \'Alumni\'',
                    'is_activated': 'Returns only activated in alumni service alumni if `True`, all others if `False`.'})
class Alumni(Resource):

    def get(self):
        """
        Return all alumni
        """

        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)
        tag = query_params.get('tag')
        is_activated = query_params.get('is_activated')

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

        # Get all activated alumni ids from alumni service
        from app.controllers.alumni_controller import AlumniController
        activated_alumni_ids = AlumniController.get_all_alumni_ids()

        if is_activated == 'True':
            return [x for x in contacts if x['id'] in activated_alumni_ids]
        elif is_activated == 'False':
            return [x for x in contacts if x['id'] not in activated_alumni_ids]

        return contacts
