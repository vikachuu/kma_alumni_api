from flask import request
from flask_restplus import Namespace, Resource, fields, abort
from flask_jwt_extended import create_access_token, create_refresh_token

from app.utils.exceptions import OdooIsDeadError


api_confim = Namespace("confirm", description="Request to confirm new alumni creation.")

confirm_fields = api_confim.model('Confirm alumni payload.', {
    "alumni_uuid": fields.String,
})


@api_confim.route("/")
class Confirm(Resource):

    @api_confim.doc(body=confirm_fields)
    def post(self):
        """Confirm new created alumni.
        """
        post_data = request.get_json()
        alumni_uuid = post_data.get("alumni_uuid")

        # check alumni with uuid exists
        from app.controllers.alumni_controller import AlumniController
        alumni = AlumniController.get_alumni_by_uuid(alumni_uuid)

        if alumni is None:
            return {
                "error_id": "alumni_not_found_error",
                "message": "Alumni not found."
                }, 404
        else:
            # update alumni status to confirmed
            from app.controllers.alumni_controller import AlumniController
            put_data = {
                "alumni_id": alumni.alumni_id,
                "user_confirmed": True
            }
            AlumniController.update_alumni_user(put_data)

            # get alumni odoo contact
            filter_list = []
            filter_list.append(['id', '=', int(alumni.odoo_contact_id)])

            from app.controllers.odoo_controller import OdooController
            try:
                contacts = OdooController.get_odoo_contacts_by_filter_list(filter_list, 0, 0)
            except OdooIsDeadError as err:
                abort(503, err, error_id='odoo_connection_error')

            contact = contacts[0]

            # return alumni data
            contact.update({
                "alumni_id": alumni.alumni_id,
                "alumni_email": alumni.email,
                "alumni_uuid": alumni.alumni_uuid,
                "user_confirmed": alumni.user_confirmed,
                "allow_show_contacts": alumni.allow_show_contacts,
            })
            return {
                "alumni": contact,
                "access_token": create_access_token(identity=alumni.email),
                "refresh_token": create_refresh_token(identity=alumni.email)
                }, 200
