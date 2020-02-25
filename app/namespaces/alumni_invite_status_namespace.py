from flask import request
from flask_restplus import Namespace, Resource, fields


api_alumni_invite_status = Namespace('alumni_invite_status', description='Requests to create a record of invited alumni status.')

invite_status_fields = api_alumni_invite_status.model('Alumni invite status payload.', {
    "odoo_contact_id": fields.String,
    "invite_status": fields.String,
})


@api_alumni_invite_status.route("/")
class AlumniInviteStatus(Resource):

    def get(self):
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        return AlumniInviteStatusController.get_id_status_records_dict()

    @api_alumni_invite_status.doc(body=invite_status_fields)
    def post(self):
        """Create new alumni status record.
        """
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        post_data = request.get_json()
        return AlumniInviteStatusController.create_invite_status_record(post_data)

    @api_alumni_invite_status.doc(body=invite_status_fields)
    def put(self):
        """Update alumni status record.
        """
        from app.controllers.alumni_invite_status_controller import AlumniInviteStatusController
        put_data = request.get_json()
        return AlumniInviteStatusController.update_invite_status_record(put_data)
