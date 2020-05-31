from flask import request
from flask_restplus import Namespace, Resource, fields, abort

from app.utils.exceptions import OdooIsDeadError


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
                    'bachelor_year_in': 'Bachelor entry year value.',
                    'bachelor_year_out': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_year_in': 'Master entry year value.',
                    'master_year_out': 'Master finish year value.',
                    
                    'user_confirmed': 'Alumni confirmed status values: `True`, `False`.'})
    def get(self):
        """Return all registered alumni (for operator side).
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_year_in = query_params.get('bachelor_year_in')
        bachelor_year_out = query_params.get('bachelor_year_out')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_year_in = query_params.get('master_year_in')
        master_year_out = query_params.get('master_year_out')

        user_confirmed = query_params.get('user_confirmed')

        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        filter_list = []
        filter_list.append(['id', 'in', registered_alumni_odoo_ids])

        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_faculty else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_year_in]) if bachelor_year_in else None
        filter_list.append(['bachelor_year_out', '=', bachelor_year_out]) if bachelor_year_out else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_year_in]) if master_year_in else None
        filter_list.append(['master_year_out', '=', master_year_out]) if master_year_out else None

        from app.controllers.odoo_controller import OdooController
        try:
            contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        # map contact
        for x in contacts:
            alumni = AlumniController.get_alumni_by_odoo_id(str(x['id']))
            x.update({
                "alumni_id": alumni.alumni_id,
                "alumni_email": alumni.email,
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
                    'bachelor_year_in': 'Bachelor entry year value.',
                    'bachelor_year_out': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_year_in': 'Master entry year value.',
                    'master_year_out': 'Master finish year value.',
                    
                    'invite_status': 'Invite status values: `not invited`, `invited`, `no response`, `rejected`.'})
    def get(self):
        """Return all unregistered alumni (for operator side).
        """

        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_year_in = query_params.get('bachelor_year_in')
        bachelor_year_out = query_params.get('bachelor_year_out')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_year_in = query_params.get('master_year_in')
        master_year_out = query_params.get('master_year_out')

        invite_status = query_params.get('invite_status')

        filter_list = []
        filter_list.append(['is_company', '=', False])
        filter_list.append(['is_alumni', '=', True])

        # get all odoo alumni ids
        from app.controllers.odoo_controller import OdooController
        try:
            all_alumni_ids = OdooController.get_odoo_contacts_ids_by_filter_list(filter_list)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        # get all registered alumni ids
        from app.controllers.alumni_controller import AlumniController
        registered_alumni_odoo_ids = AlumniController.get_all_registered_alumni_odoo_ids()

        # not registered and not invited alumni ids together
        not_registered_alumni_odoo_ids = [x for x in all_alumni_ids if x not in registered_alumni_odoo_ids]

        filter_list.append(['id', 'in', not_registered_alumni_odoo_ids])
        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_faculty else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_year_in]) if bachelor_year_in else None
        filter_list.append(['bachelor_year_out', '=', bachelor_year_out]) if bachelor_year_out else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_year_in]) if master_year_in else None
        filter_list.append(['master_year_out', '=', master_year_out]) if master_year_out else None

        # get contacts from odoo
        try:
            contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

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
                    'bachelor_year_in': 'Bachelor entry year value.',
                    'bachelor_year_out': 'Bachelor finish year value.',

                    'master_faculty': 'Master faculty value.',
                    'master_speciality': 'Master speciality value.',
                    'master_year_in': 'Master entry year value.',
                    'master_year_out': 'Master finish year value.',})
    def get(self):
        """Get all alumni (for alumni side).
        """
        query_params = request.args
        offset = query_params.get('offset', 0)
        limit = query_params.get('limit', 0)

        bachelor_faculty = query_params.get('bachelor_faculty')
        bachelor_speciality = query_params.get('bachelor_speciality')
        bachelor_year_in = query_params.get('bachelor_year_in')
        bachelor_year_out = query_params.get('bachelor_year_out')

        master_faculty = query_params.get('master_faculty')
        master_speciality = query_params.get('master_speciality')
        master_year_in = query_params.get('master_year_in')
        master_year_out = query_params.get('master_year_out')

        filter_list = []
        filter_list.append(['is_alumni', '=', True])

        filter_list.append(['bachelor_faculty', '=', bachelor_faculty]) if bachelor_faculty else None
        filter_list.append(['bachelor_speciality', '=', bachelor_speciality]) if bachelor_speciality else None
        filter_list.append(['bachelor_year_in', '=', bachelor_year_in]) if bachelor_year_in else None
        filter_list.append(['bachelor_year_out', '=', bachelor_year_out]) if bachelor_year_out else None

        filter_list.append(['master_faculty', '=', master_faculty]) if master_faculty else None
        filter_list.append(['master_speciality', '=', master_speciality]) if master_speciality else None
        filter_list.append(['master_year_in', '=', master_year_in]) if master_year_in else None
        filter_list.append(['master_year_out', '=', master_year_out]) if master_year_out else None

        # get all alumni from odoo
        from app.controllers.odoo_controller import OdooController
        try:
            contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, offset, limit)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

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


@api_alumni.route("/<alumni_id>")
class AlumniId(Resource):

    @api_alumni.doc(params={
                    'alumni_id': 'An alumni id.',})
    def delete(self, alumni_id):
        """Delete alumni on alumni service side
        """
        from app.controllers.alumni_controller import AlumniController
        response = AlumniController.delete_alumni_user(alumni_id)
        return response


@api_alumni.route("/<odoo_contact_id>")
class AlumniOdooContactId(Resource):

    @api_alumni.doc(params={
                    'odoo_contact_id': 'An Odoo contact id.',})
    def get(self, odoo_contact_id):
        """Get odoo contact by id
        """

        filter_list = []
        filter_list.append(['id', '=', int(odoo_contact_id)])

        from app.controllers.odoo_controller import OdooController
        try:
            contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, 0, 0)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        if not len(contacts):
            return {
                "error_id": "odoo_contact_not_found_error",
                "message": "No odoo contact with such an id exists."
                }, 404

        contact = contacts[0]

        # get alumni user
        from app.controllers.alumni_controller import AlumniController
        alumni = AlumniController.get_alumni_by_odoo_id(str(contact.get('id')))

        if alumni is not None:
            contact.update({
                    "alumni_id": alumni.alumni_id,
                    "alumni_email": alumni.email,
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
        try:
            contacts = OdooController.get_odoo_contact_with_groupmates_fields(filter_list)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        # TODO: throw contact not found error
        if not len(contacts):
            return {
                "error_id": "odoo_contact_not_found_error",
                "message": "No odoo contact with such an id exists."
                }, 404

        contact = contacts[0]
        print(f"CONTACT {contact}")

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
                "error_id": "no_required_groupmates_fields_error",
                "message": "No required fields to get groupmates: should be both speciality and entry year given."
                }, 400

        # get all groupmates (both bachelor and masters)
        try:
            contacts = OdooController.get_odoo_contacts_by_filter_list(groupmates_filter_list, offset, limit)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

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
