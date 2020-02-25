from flask import request
from flask_restplus import Namespace, Resource, fields


api_alumni = Namespace('alumni', description='Requests to alumni model')

resource_fields = api_alumni.model('Create alumni user payload', {
    "odoo_contact_id": fields.String,
    "email": fields.String,
    "password": fields.String,
})


@api_alumni.route("/")
class Alumni(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',
                    'tag': 'Filter by tag from Odoo contact. For example - \'Alumni\'',
                    'is_activated': 'Returns only activated in alumni service alumni if `True`, all others if `False`.'})
    def get(self):
        """Return all alumni
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

        # Get all activated alumni ids with statuses
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        not_activated_alumni_records = AlumniInviteStatusController.get_id_status_records_dict()

        # map odoo contacts with statuses
        for x in contacts:
            status = not_activated_alumni_records.get(str(x['id']))
            x.update({
                "alumni_status": status if status else "not invited"
            })

        if is_activated == 'True':
            return {
                "data": [x for x in contacts if x['alumni_status'] == "registered"],
                "status": 200,
                "error": None
            }
            
        elif is_activated == 'False':
            return {
                "data": [x for x in contacts if x['alumni_status'] != "registered"],
                "status": 200,
                "error": None
            }

        return {
                "data": contacts,
                "status": 200,
                "error": None
            }

    @api_alumni.doc(body=resource_fields)
    def post(self):
        """Create alumni user
        """
        from app.controllers.alumni_controller import AlumniController
        post_data = request.get_json()
        return AlumniController.create_alumni_user(post_data)
