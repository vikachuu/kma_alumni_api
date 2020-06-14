from app.main import db
from app.models.update_form_model import UpdateForm


class UpdateFormController:
    
    @staticmethod
    def create_update_form(post_data):
        # check if there is active update form for this alumni
        update_form = UpdateForm.query.filter_by(alumni_id=post_data.get('alumni_id'), form_status='new').first()
        if not update_form:
            update_form = UpdateForm(
                name=post_data.get('name'),
                birth_date=post_data.get('birth_date'),
                image_1920=post_data.get('image_1920'),

                contact_country=post_data.get('contact_country'),
                contact_city=post_data.get('contact_city'),

                mobile=post_data.get('mobile'),
                skype=post_data.get('skype'),
                telegram=post_data.get('telegram'),
                viber=post_data.get('viber'),

                facebook_link=post_data.get('facebook_link'),
                linkedin_link=post_data.get('linkedin_link'),

                diploma_naukma=post_data.get('diploma_naukma'),

                bachelor_degree=post_data.get('bachelor_degree'),
                bachelor_faculty=post_data.get('bachelor_faculty'),
                bachelor_speciality=post_data.get('bachelor_speciality'),
                bachelor_year_in=post_data.get('bachelor_year_in'),
                bachelor_year_out=post_data.get('bachelor_year_out'),

                master_degree=post_data.get('master_degree'),
                master_faculty=post_data.get('master_faculty'),
                master_speciality=post_data.get('master_speciality'),
                master_year_in=post_data.get('master_year_in'),
                master_year_out=post_data.get('master_year_out'),

                parent_id=post_data.get('parent_id'),
                company_name=post_data.get('company_name'),
                function=post_data.get('function'),

                alumni_id=post_data.get('alumni_id'),
                operator_id=None,
            )

            # insert new update form
            db.session.add(update_form)
            db.session.commit()

            return {
                "form_id": update_form.form_id,
                "form_status": update_form.form_status,
                "name": update_form.name,
                "birth_date": update_form.birth_date.strftime('%Y-%m-%d'),
                "image_1920": update_form.image_1920,

                "contact_country": update_form.contact_country,
                "contact_city": update_form.contact_city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook_link": update_form.facebook_link,
                "linkedin_link": update_form.linkedin_link,

                "diploma_naukma": update_form.diploma_naukma,

                "bachelor_degree": update_form.bachelor_degree,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_year_in": update_form.bachelor_year_in,
                "bachelor_year_out": update_form.bachelor_year_out,

                "master_degree": update_form.master_degree,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_year_in": update_form.master_year_in,
                "master_year_out": update_form.master_year_out,

                "parent_id": update_form.parent_id,
                "company_name": update_form.company_name,
                "function": update_form.function,

                "alumni_id": update_form.alumni_id,
                "operator_id": update_form.operator_id,
                }, 201
        else:
            return {
                "error_id": "active_form_exists_error",
                "message": "There is an active update form for this alumnus. Only one active form is accepted."
            }, 400

    @staticmethod
    def get_all_update_forms(form_status):
        if form_status is not None:
            update_forms = UpdateForm.query.filter_by(form_status=form_status).all()
        else:
            update_forms = UpdateForm.query.all()
        # TODO: write custom JSONifier

        result_forms = [
            {
                "form_id": update_form.form_id,
                "form_status": update_form.form_status,
                "name": update_form.name,
                "birth_date": update_form.birth_date.strftime('%Y-%m-%d'),
                "image_1920": update_form.image_1920,

                "contact_country": update_form.contact_country,
                "contact_city": update_form.contact_city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook_link": update_form.facebook_link,
                "linkedin_link": update_form.linkedin_link,

                "diploma_naukma": update_form.diploma_naukma,

                "bachelor_degree": update_form.bachelor_degree,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_year_in": update_form.bachelor_year_in,
                "bachelor_year_out": update_form.bachelor_year_out,

                "master_degree": update_form.master_degree,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_year_in": update_form.master_year_in,
                "master_year_out": update_form.master_year_out,

                "parent_id": update_form.parent_id,
                "company_name": update_form.company_name,
                "function": update_form.function,

                "alumni_id": update_form.alumni_id,
                "operator_id": update_form.operator_id,
            } for update_form in update_forms]

        return result_forms, 200

    @staticmethod
    def get_alumni_update_form_history(alumni_id):
        update_forms = UpdateForm.query.filter_by(alumni_id=alumni_id).all()
        result_forms = [
            {
                "form_id": update_form.form_id,
                "form_status": update_form.form_status,
                "name": update_form.name,
                "birth_date": update_form.birth_date.strftime('%Y-%m-%d'),
                "image_1920": update_form.image_1920,

                "contact_country": update_form.contact_country,
                "contact_city": update_form.contact_city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook_link": update_form.facebook_link,
                "linkedin_link": update_form.linkedin_link,

                "diploma_naukma": update_form.diploma_naukma,

                "bachelor_degree": update_form.bachelor_degree,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_year_in": update_form.bachelor_year_in,
                "bachelor_year_out": update_form.bachelor_year_out,

                "master_degree": update_form.master_degree,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_year_in": update_form.master_year_in,
                "master_year_out": update_form.master_year_out,

                "parent_id": update_form.parent_id,
                "company_name": update_form.company_name,
                "function": update_form.function,

                "alumni_id": update_form.alumni_id,
                "operator_id": update_form.operator_id,
            } for update_form in update_forms]
        return result_forms, 200

    @staticmethod
    def change_update_form_status(form_id, put_data):
        update_form = UpdateForm.query.filter_by(form_id=form_id).first()
        if not update_form:
            return {
                "error_id": "form_not_found_error",
                "message": "Form not found."
            }, 404
        else:
            update_form.form_status = put_data.get('form_status')
            update_form.operator_id = put_data.get('operator_id')
            db.session.add(update_form)
            db.session.commit()

            return {
                "message": "Form successfully updated."
                }, 200

    @staticmethod
    def edit_update_form(form_id, put_data):
        update_form = UpdateForm.query.filter_by(form_id=form_id).first()
        if not update_form:
            return {
                "error_id": "form_not_found_error",
                "message": "Form not found."
            }, 404
        else:
            update_form.update(put_data)

            return {
                "message": "Form successfully updated."
                }, 200

    @staticmethod
    def get_update_form_by_id(form_id):
        update_form = UpdateForm.query.filter_by(form_id=form_id).first()
        if not update_form:
            return {
                "error_id": "form_not_found_error",
                "message": "Form not found."
            }, 404
        else:
            return {
                "form_id": update_form.form_id,
                "form_status": update_form.form_status,
                "name": update_form.name,
                "birth_date": update_form.birth_date.strftime('%Y-%m-%d'),
                "image_1920": update_form.image_1920,

                "contact_country": update_form.contact_country,
                "contact_city": update_form.contact_city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook_link": update_form.facebook_link,
                "linkedin_link": update_form.linkedin_link,

                "diploma_naukma": update_form.diploma_naukma,

                "bachelor_degree": update_form.bachelor_degree,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_year_in": update_form.bachelor_year_in,
                "bachelor_year_out": update_form.bachelor_year_out,

                "master_degree": update_form.master_degree,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_year_in": update_form.master_year_in,
                "master_year_out": update_form.master_year_out,

                "parent_id": update_form.parent_id,
                "company_name": update_form.company_name,
                "function": update_form.function,

                "alumni_id": update_form.alumni_id,
                "operator_id": update_form.operator_id,
                }, 200

    @staticmethod
    def get_active_update_form_exists(alumni_id):
        update_form = UpdateForm.query.filter_by(alumni_id=alumni_id, form_status="new").first()
        return update_form is not None
