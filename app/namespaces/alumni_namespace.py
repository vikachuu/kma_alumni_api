from flask import request
from flask_restplus import Namespace, Resource, fields, abort


api_alumni = Namespace('alumni', description='Requests to alumni model.')

resource_fields = api_alumni.model('Create alumni user payload', {
    "odoo_contact_id": fields.String,
    "email": fields.String,
    "password": fields.String,
    "allow_show_contacts": fields.Boolean,
})


@api_alumni.route("/registered")
class AlumniRegistered(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',
                    
                    'bachelor_faculty': 'Bachelor faculty value.',
                    'bachelor_speciality': 'Bachelor speciality value.',
                    'bachelor_entry_year': 'Bachelor entry year value.',
                    'bachelor_finish_year': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_entry_year': 'Master entry year value.',
                    'master_finish_year': 'Master finish year value.',
                    
                    'user_confirmed': 'Alumni confirmed status values: `True`, `False`.'})
    def get(self):
        """Return all registered alumni (for operator side).
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_entry_year = query_params.get('bachelor_entry_year')
        bachelor_finish_year = query_params.get('bachelor_finish_year')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_entry_year = query_params.get('master_entry_year')
        master_finish_year = query_params.get('master_finish_year')

        user_confirmed = query_params.get('user_confirmed')

        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        filter_list = []
        filter_list.append(['id', 'in', registered_alumni_odoo_ids])

        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_entry_year else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_entry_year]) if bachelor_entry_year else None
        filter_list.append(['bachelor_year_out', '=', bachelor_finish_year]) if bachelor_finish_year else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_entry_year]) if master_entry_year else None
        filter_list.append(['master_year_out', '=', master_finish_year]) if master_finish_year else None

        from app.controllers.odoo_controller import OdooController
        contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)

        # map contact
        for x in contacts:
            alumni = AlumniController.get_alumni_by_odoo_id(str(x['id']))
            x.update({
                "alumni_uuid": alumni.alumni_uuid,
                "user_confirmed": alumni.user_confirmed,
                "allow_show_contacts": alumni.allow_show_contacts,
            })

        # filter contact by user confirmed status of exists
        if user_confirmed is not None:
            contacts = [x for x in contacts if x['user_confirmed']]


        return contacts, 200


@api_alumni.route("/unregistered")
class AlumniUnregistered(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',

                    'bachelor_faculty': 'Bachelor faculty value.',
                    'bachelor_speciality': 'Bachelor speciality value.',
                    'bachelor_entry_year': 'Bachelor entry year value.',
                    'bachelor_finish_year': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_entry_year': 'Master entry year value.',
                    'master_finish_year': 'Master finish year value.',
                    
                    'invite_status': 'Invite status values: `not invited`, `invited`, `no response`, `rejected`.'})
    def get(self):
        """Return all unregistered alumni (for operator side).
        """

        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_entry_year = query_params.get('bachelor_entry_year')
        bachelor_finish_year = query_params.get('bachelor_finish_year')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_entry_year = query_params.get('master_entry_year')
        master_finish_year = query_params.get('master_finish_year')

        invite_status = query_params.get('invite_status')

        filter_list = []
        filter_list.append(['is_company', '=', False])
        filter_list.append(['is_alumni', '=', True])

        # get all odoo alumni ids
        from app.controllers.odoo_controller import OdooController
        all_alumni_ids = OdooController.get_odoo_contacts_ids_by_filter_list(filter_list)

        # get all registered alumni ids
        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        # not registered and not invited alumni ids together
        not_registered_alumni_odoo_ids = [x for x in all_alumni_ids if x not in registered_alumni_odoo_ids]

        filter_list.append(['id', 'in', not_registered_alumni_odoo_ids])
        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_faculty else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_entry_year]) if bachelor_entry_year else None
        filter_list.append(['bachelor_year_out', '=', bachelor_finish_year]) if bachelor_finish_year else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_entry_year]) if master_entry_year else None
        filter_list.append(['master_year_out', '=', master_finish_year]) if master_finish_year else None

        # get contacts from odoo
        contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)

        # get all NOT registered alumni ids with statuses (invited, no response, rejected etc.)
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        not_registerd_alumni_records = AlumniInviteStatusController.get_id_status_records_dict()

        # map odoo contacts with statuses
        for x in contacts:
            status = not_registerd_alumni_records.get(str(x['id']))
            x.update({
                "alumni_status": status if status else "not invited"
            })

        # filter by status query param if exists
        if invite_status is not None:
            contacts = [x for x in contacts if x['alumni_status'] == invite_status]

        return contacts, 200


@api_alumni.route("/")
class Alumni(Resource):

    @api_alumni.doc(params={
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',

                    'bachelor_faculty': 'Bachelor faculty value.',
                    'bachelor_speciality': 'Bachelor speciality value.',
                    'bachelor_entry_year': 'Bachelor entry year value.',
                    'bachelor_finish_year': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_entry_year': 'Master entry year value.',
                    'master_finish_year': 'Master finish year value.',})
    def get(self):
        """Get all alumni (for alumni side).
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_entry_year = query_params.get('bachelor_entry_year')
        bachelor_finish_year = query_params.get('bachelor_finish_year')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_entry_year = query_params.get('master_entry_year')
        master_finish_year = query_params.get('master_finish_year')

        filter_list = []
        filter_list.append(['is_alumni', '=', True])

        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_entry_year else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_entry_year]) if bachelor_entry_year else None
        filter_list.append(['bachelor_year_out', '=', bachelor_finish_year]) if bachelor_finish_year else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_entry_year]) if master_entry_year else None
        filter_list.append(['master_year_out', '=', master_finish_year]) if master_finish_year else None

        # get all alumni from odoo
        from app.controllers.odoo_controller import OdooController
        contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)

        # get all registered alumni id
        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids_allow_show_contacts = AlumniController.get_alumni_odoo_id_allow_show_contacts_dict()

        # map contacts with statuses (registered/unregistered) and allow_show_contacts field
        for x in contacts:
            x.update({
                "alumni_status": "registered" if str(x['id']) in registered_alumni_odoo_ids_allow_show_contacts else "unregistered",
                "allow_show_contacts": registered_alumni_odoo_ids_allow_show_contacts.get(str(x['id']), False)
            })

        return contacts, 200

    @api_alumni.doc(body=resource_fields)
    def post(self):
        """Create alumni user.
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

        from app.controllers.odoo_controller import OdooController
        contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, 0, 0)

        if not len(contacts):
            return {
                "error": "Odoo contact not found.",
                "message": "No odoo contact with such an id exists."
                }, 404

        contact = contacts[0]

        # get alumni user
        from app.controllers.alumni_controller import AlumniController
        alumni = AlumniController.get_alumni_by_odoo_id(str(contact.get('id')))

        if alumni is not None:
            contact.update({
                    "alumni_uuid": alumni.alumni_uuid,
                    "user_confirmed": alumni.user_confirmed,
                    "allow_show_contacts": alumni.allow_show_contacts,
                })

        return contact, 200


@api_alumni.route("/<odoo_contact_id>/groupmates")
class AlumniGroupmates(Resource):

    @api_alumni.doc(params={
                    'odoo_contact_id': 'Odoo contact id.',
                    'offset': 'Offset value for pagination. Default: 0.',
                    'limit': 'Limit value for pagination. Default: 0.',})
    def get(self, odoo_contact_id):
        """Get Bachelor and Master groupmates for alumni with given alumni id.
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        # get odoo contact by id
        filter_list = []
        filter_list.append(['id', '=', int(odoo_contact_id)])

        from app.controllers.odoo_controller import OdooController
        contacts = OdooController.get_odoo_contact_with_groupmates_fields(filter_list)

        if not len(contacts):
            return {
                "error": "Odoo contact not found.",
                "message": "No odoo contact with such an id exists."
                }, 404

        contact = contacts[0]

        # append filters for groupmates
        bachelor_speciality = contact.get('bachelor_speciality')
        bachelor_year_in = contact.get('bachelor_year_in')
        master_speciality = contact.get('master_speciality')
        master_year_in = contact.get('master_year_in')

        if bachelor_speciality and bachelor_year_in and master_speciality and master_year_in:
            groupmates_filter_list = ['&', ('id', '!=', odoo_contact_id),
                                      '|', '&', ('bachelor_speciality', '=', bachelor_speciality), ('bachelor_year_in', '=', bachelor_year_in),
                                            '&', ('master_speciality', '=', master_speciality), ('master_year_in', '=', master_year_in)]

        elif bachelor_speciality and bachelor_year_in:
            groupmates_filter_list = ['&', ('id', '!=', odoo_contact_id),
                                      '&', ('bachelor_speciality', '=', bachelor_speciality), ('bachelor_year_in', '=', bachelor_year_in)]

        elif master_speciality and master_year_in:
            groupmates_filter_list = ['&', ('id', '!=', odoo_contact_id),
                                      '&', ('master_speciality', '=', master_speciality), ('master_year_in', '=', master_year_in)]

        else:
            return {
                "error": "No required query parameters.",
                "message": "No required query parameters."
                }, 400

        # get all groupmates (both bachelor and masters)
        contacts = OdooController.get_odoo_contacts_by_filter_list(groupmates_filter_list, offset, limit)

         # get all registered alumni id
        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids_allow_show_contacts = AlumniController.get_alumni_odoo_id_allow_show_contacts_dict()

        # map contacts with statuses (registered/unregistered) and allow_show_contacts field
        for x in contacts:
            x.update({
                "alumni_status": "registered" if str(x['id']) in registered_alumni_odoo_ids_allow_show_contacts else "unregistered",
                "allow_show_contacts": registered_alumni_odoo_ids_allow_show_contacts.get(str(x['id']), False)
            })

        return contacts, 200
