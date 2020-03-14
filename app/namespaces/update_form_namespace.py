from flask import request
from flask_restplus import Namespace, Resource, fields


api_update_form = Namespace('update_form', description='Requests to update form model.')

update_form_fields = api_update_form.model('Create update form.', {
    "full_name_uk": fields.String,
    "date_of_birth": fields.String,
    "image": fields.String,

    "country": fields.String,
    "city": fields.String,
    "mobile": fields.String,
    "skype": fields.String,
    "telegram": fields.String,
    "viber": fields.String,
    "facebook": fields.String,
    "linkedin": fields.String,

    "is_bachelor": fields.Boolean,
    "bachelor_faculty": fields.String,
    "bachelor_speciality": fields.String,
    "bachelor_entry_year": fields.String,
    "bachelor_finish_year": fields.String,

    "is_master": fields.Boolean,
    "master_faculty": fields.String,
    "master_speciality": fields.String,
    "master_entry_year": fields.String,
    "master_finish_year": fields.String,

    "company": fields.String,
    "job_position": fields.String,

    "alumni_id": fields.Integer,
    "operator_id": fields.Integer,
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
        'form_id': "Id of update form in which status changed."
    })
    def put(self, form_id):
        """Change update form status and operator id who did the change.
        """
        from app.controllers.update_form_controller import UpdateFormController
        put_data = request.get_json()
        return UpdateFormController.change_update_form_status(form_id, put_data)
