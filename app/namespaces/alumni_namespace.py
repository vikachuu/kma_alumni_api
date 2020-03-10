from flask import request
from flask_restplus import Namespace, Resource, fields


api_alumni = Namespace('alumni', description='Requests to alumni model.')

resource_fields = api_alumni.model('Create alumni user payload', {
    "odoo_contact_id": fields.String,
    "email": fields.String,
    "password": fields.String,
})


@api_alumni.route("/registered")
class AlumniRegistered(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',})
    def get(self):
        """Return all registered alumni.
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [[['id', 'in', registered_alumni_odoo_ids]]],
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920'],
                'offset': int(offset),
                'limit': int(limit)})

        # get all registered alumni odoo ids with statuses
        # map contacts with statuses

        return {
                "data": contacts,
                "status": 200,
                "error": None
            }


@api_alumni.route("/unregistered")
class AlumniUnregistered(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',})
    def get(self):
        """Return all unregistered alumni.
        """

        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        filter_list = []
        filter_list.append(['is_company', '=', False])
        filter_list.append(['is_alumni', '=', True])

        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models

        # get all odoo alumni ids
        all_alumni_ids = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner',
                        'search',[filter_list])

        # get all registered alumni ids
        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        # not registered and not invited alumni ids together
        not_registered_alumni_odoo_ids = [x for x in all_alumni_ids if x not in registered_alumni_odoo_ids]

        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [[['id', 'in', not_registered_alumni_odoo_ids]]],
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link', 'is_alumni',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920'],
                'offset': int(offset),
                'limit': int(limit)})

        # get all NOT registered alumni ids with statuses (invited, no response, rejected etc.)
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        not_registerd_alumni_records = AlumniInviteStatusController.get_id_status_records_dict()

        # map odoo contacts with statuses
        for x in contacts:
            status = not_registerd_alumni_records.get(str(x['id']))
            x.update({
                "alumni_status": status if status else "not invited"
            })

        return {
                "data": contacts,
                "status": 200,
                "error": None
            }


@api_alumni.route("/")
class Alumni(Resource):

    @api_alumni.doc(body=resource_fields)
    def post(self):
        """Create alumni user
        """
        from app.controllers.alumni_controller import AlumniController
        post_data = request.get_json()
        return AlumniController.create_alumni_user(post_data)


@api_alumni.route("/<odoo_contact_id>")
class AlumniId(Resource):

    @api_alumni.doc(params={
                    'odoo_contact_id': 'An Odoo contact id.',})
    def get(self, odoo_contact_id):
        """Get odoo contact by id
        """

        filter_list = []
        filter_list.append(['id', '=', int(odoo_contact_id)])

        from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
        contacts = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                [filter_list],
                {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                'image_1920'],})

        if not len(contacts):
            return {
                "data": None,
                "status": 404,
                "error": "No odoo contact with such id exists."
                }

        contact = contacts[0]

        # get alumni user
        from app.controllers.alumni_controller import AlumniController
        alumni = AlumniController.get_alumni_by_odoo_id(str(contact.get('id')))

        if alumni is not None:
            contact.update({
                    "alumni_uuid": alumni.alumni_uuid,
                    "user_confirmed": alumni.user_confirmed,
                })

        return {
                "data": {
                    "alumni": contact
                },
                "status": 200,
                "error": None
                }
