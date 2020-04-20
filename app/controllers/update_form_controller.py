from app.main import db
from app.models.update_form_model import UpdateForm


class UpdateFormController:
    
    @staticmethod
    def create_update_form(post_data):
        # check if there is active update form for this alumni
        update_form = UpdateForm.query.filter_by(alumni_id=post_data.get('alumni_id'), form_status='new').first()
        if not update_form:
            update_form = UpdateForm(
                full_name_uk=post_data.get('full_name_uk'),
                date_of_birth=post_data.get('date_of_birth'),
                image=post_data.get('image'),
                email=post_data.get('email'),

                country=post_data.get('country'),
                city=post_data.get('city'),

                mobile=post_data.get('mobile'),
                skype=post_data.get('skype'),
                telegram=post_data.get('telegram'),
                viber=post_data.get('viber'),

                facebook=post_data.get('facebook'),
                linkedin=post_data.get('linkedin'),

                is_bachelor=post_data.get('is_bachelor'),
                bachelor_faculty=post_data.get('bachelor_faculty'),
                bachelor_speciality=post_data.get('bachelor_speciality'),
                bachelor_entry_year=post_data.get('bachelor_entry_year'),
                bachelor_finish_year=post_data.get('bachelor_finish_year'),

                is_master=post_data.get('is_master'),
                master_faculty=post_data.get('master_faculty'),
                master_speciality=post_data.get('master_speciality'),
                master_entry_year=post_data.get('master_entry_year'),
                master_finish_year=post_data.get('master_finish_year'),

                company=post_data.get('company'),
                job_position=post_data.get('job_position'),

                alumni_id=post_data.get('alumni_id'),
                operator_id=None,
            )

            # insert new update form
            db.session.add(update_form)
            db.session.commit()

            return {
                "form_id": update_form.form_id,
                "form_status": update_form.form_status,
                "full_name_uk": update_form.full_name_uk,
                "date_of_birth": update_form.date_of_birth.strftime('%Y-%m-%d'),
                "image": update_form.image,
                "email": update_form.email,

                "country": update_form.country,
                "city": update_form.city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook": update_form.facebook,
                "linkedin": update_form.linkedin,

                "is_bachelor": update_form.is_bachelor,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_entry_year": update_form.bachelor_entry_year,
                "bachelor_finish_year": update_form.bachelor_finish_year,

                "is_master": update_form.is_master,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_entry_year": update_form.master_entry_year,
                "master_finish_year": update_form.master_finish_year,

                "company": update_form.company,
                "job_position": update_form.job_position,

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
                "full_name_uk": update_form.full_name_uk,
                "date_of_birth": update_form.date_of_birth.strftime('%Y-%m-%d'),
                "image": update_form.image,
                "email": update_form.email,

                "country": update_form.country,
                "city": update_form.city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook": update_form.facebook,
                "linkedin": update_form.linkedin,

                "is_bachelor": update_form.is_bachelor,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_entry_year": update_form.bachelor_entry_year,
                "bachelor_finish_year": update_form.bachelor_finish_year,

                "is_master": update_form.is_master,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_entry_year": update_form.master_entry_year,
                "master_finish_year": update_form.master_finish_year,

                "company": update_form.company,
                "job_position": update_form.job_position,

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
                "full_name_uk": update_form.full_name_uk,
                "date_of_birth": update_form.date_of_birth.strftime('%Y-%m-%d'),
                "image": update_form.image,
                "email": update_form.email,

                "country": update_form.country,
                "city": update_form.city,
                "mobile": update_form.mobile,
                "skype": update_form.skype,
                "telegram": update_form.telegram,
                "viber": update_form.viber,
                "facebook": update_form.facebook,
                "linkedin": update_form.linkedin,

                "is_bachelor": update_form.is_bachelor,
                "bachelor_faculty": update_form.bachelor_faculty,
                "bachelor_speciality": update_form.bachelor_speciality,
                "bachelor_entry_year": update_form.bachelor_entry_year,
                "bachelor_finish_year": update_form.bachelor_finish_year,

                "is_master": update_form.is_master,
                "master_faculty": update_form.master_faculty,
                "master_speciality": update_form.master_speciality,
                "master_entry_year": update_form.master_entry_year,
                "master_finish_year": update_form.master_finish_year,

                "company": update_form.company,
                "job_position": update_form.job_position,

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
