from flask import request
from flask_restplus import Namespace, Resource, fields

from app.utils.exceptions import OdooIsDeadError


api_update_form = Namespace('update_form', description='Requests to update form model.')

update_form_fields = api_update_form.model('Create update form.', {
    "name": fields.String,
    "birth_date": fields.String,
    "image_1920": fields.String,

    "contact_country": fields.String,
    "contact_city": fields.String,
    "mobile": fields.String,
    "skype": fields.String,
    "telegram": fields.String,
    "viber": fields.String,
    "facebook_link": fields.String,
    "linkedin_link": fields.String,

    "diploma_naukma": fields.Boolean,

    "bachelor_degree": fields.Boolean,
    "bachelor_faculty": fields.String,
    "bachelor_speciality": fields.String,
    "bachelor_year_in": fields.String,
    "bachelor_year_out": fields.String,

    "master_degree": fields.Boolean,
    "master_faculty": fields.String,
    "master_speciality": fields.String,
    "master_year_in": fields.String,
    "master_year_out": fields.String,

    "parent_id": fields.Integer,
    "company_name": fields.String,
    "function": fields.String,

    "alumni_id": fields.Integer,
})


@api_update_form.route("/")
class UpdateForm(Resource):

    @api_update_form.doc(body=update_form_fields)
    def post(self):
        """Create update form.
        """
        from app.controllers.update_form_controller import UpdateFormController
        post_data = request.get_json()
        return UpdateFormController.create_update_form(post_data)

    @api_update_form.doc(params={
        'form_status': 'Update form status. Values: `new`, `approved`, `rejected`.',
    })
    def get(self):
        """Get all update forms by status filters.
        """
        query_params = request.args
        form_status = query_params.get('form_status')
        from app.controllers.update_form_controller import UpdateFormController
        return UpdateFormController.get_all_update_forms(form_status)


@api_update_form.route("/history/<alumni_id>")
class UpdateFormHistory(Resource):

    @api_update_form.doc(params={
        'alumni_id': 'Alumnus id to get update form history for.',
    })
    def get(self, alumni_id):
        """Get all alumni update forms.
        """
        from app.controllers.update_form_controller import UpdateFormController
        return UpdateFormController.get_alumni_update_form_history(alumni_id)

change_update_form_status_fields = api_update_form.model('Update update form status.', {
    'form_status': fields.String,
    'operator_id': fields.Integer,
})

@api_update_form.route("/<form_id>")
class UpdateFormId(Resource):

    @api_update_form.doc(body=change_update_form_status_fields, params={
        'form_id': "Id of update form in which status changed.",
    })
    def put(self, form_id):
        """Change update form status and operator id who did the change.
        """
        from app.controllers.update_form_controller import UpdateFormController
        put_data = request.get_json()
        return UpdateFormController.change_update_form_status(form_id, put_data)


confirm_update_form_fields = api_update_form.model('Confirm update form.', {
    "form_id": fields.Integer,
    "name": fields.String,
    "birth_date": fields.String,
    "image_1920": fields.String,

    "contact_country": fields.String,
    "contact_city": fields.String,

    "mobile": fields.String,
    "skype": fields.String,
    "telegram": fields.String,
    "viber": fields.String,
    "facebook_link": fields.String,
    "linkedin_link": fields.String,

    "diploma_naukma": fields.Boolean,

    "bachelor_degree": fields.Boolean,
    "bachelor_faculty": fields.String,
    "bachelor_speciality": fields.String,
    "bachelor_year_in": fields.String,
    "bachelor_year_out": fields.String,

    "master_degree": fields.Boolean,
    "master_faculty": fields.String,
    "master_speciality": fields.String,
    "master_year_in": fields.String,
    "master_year_out": fields.String,

    "parent_id": fields.Integer,
    "function": fields.String,

    "alumni_id": fields.Integer,
    "operator_id": fields. Integer
})


@api_update_form.route("/confirm")
class UpdateFormConfirm(Resource):

    @api_update_form.doc(body=confirm_update_form_fields)
    def post(self):
        """Confirm update form - send data to odoo.
        """
        post_data = request.get_json()
        print(post_data)
        from app.controllers.alumni_controller import AlumniController
        odoo_contact_id = AlumniController.get_odoo_contact_id_by_alumni_id(post_data.get('alumni_id'))

        from app.controllers.odoo_controller import OdooController
        try:
            OdooController.update_odoo_contact(odoo_contact_id, post_data)
        except OdooIsDeadError as err:
            abort(503, err, error_id='odoo_connection_error')

        # if success - change update form status and operator who confirmed
        from app.controllers.update_form_controller import UpdateFormController
        form_id = post_data.get('form_id')
        put_data = {
            'form_status': 'approved',
            'operator_id': post_data.get('operator_id')
        }
        UpdateFormController.change_update_form_status(form_id, put_data)

        return {"message": "Odoo contact successfully updated."}, 200
