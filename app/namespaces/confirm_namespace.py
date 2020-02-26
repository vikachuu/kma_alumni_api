from flask import request
from flask_restplus import Namespace, Resource, fields


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
            return {"data": {
                        "alumni_uuid": alumni_uuid
                        },
                    "status": 404,
                    "error": f"Alumni does not exist."
                    }
        else:
            # update alumni status to confirmed
            from app.controllers.alumni_controller import AlumniController
            put_data = {
                "alumni_id": alumni.alumni_id,
                "user_confirmed": True
            }
            AlumniController.update_alumni_user(put_data)

            # get alumni odoo contact
            from app.main import odoo_db, odoo_uid, odoo_password, odoo_models
            contact = odoo_models.execute_kw(odoo_db, odoo_uid, odoo_password, 'res.partner', 'search_read',
                    [[['id', '=', int(alumni.odoo_contact_id)],]],
                    {'fields': ['name', 'email', 'function', 'parent_id', 'facebook_link', 'linkedin_link',
                    'bachelor_degree', 'bachelor_faculty', 'bachelor_speciality', 'bachelor_year_in', 'bachelor_year_out',
                    'master_degree', 'master_faculty', 'master_speciality', 'master_year_in', 'master_year_out',
                    'image_1920'],})

            # return alumni data
            contact[0].update({
                "alumni_uuid": alumni.alumni_uuid,
                "password": alumni.password,
                "user_confirmed": alumni.user_confirmed,
            })
            return {
                "data": {
                    "alumni": contact
                },
                "status": 200,
                "error": None
            }
