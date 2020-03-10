from app.main import db
from app.models.alumni_model import Alumni


class AlumniController:

    @staticmethod
    def get_alumni_by_uuid(alumni_uuid):
        alumni = Alumni.query.filter_by(alumni_uuid=alumni_uuid).first()
        return alumni

    @staticmethod
    def get_all_registered_alumni_odoo_ids():
        ids = db.session.query(Alumni.odoo_contact_id).all()
        return [int(x) for x, in ids]

    @staticmethod
    def get_alumni_user_by_email(email):
        alumni = Alumni.query.filter_by(email=email).first()
        return alumni

    @staticmethod
    def create_alumni_user(post_data):
        # check if user already exists
        alumni = Alumni.query.filter_by(odoo_contact_id=post_data.get('odoo_contact_id')).first()
        if not alumni:
            alumni = Alumni(
                odoo_contact_id=post_data.get('odoo_contact_id'),
                email=post_data.get('email'),
                password=post_data.get('password'),
            )

            # insert the user
            db.session.add(alumni)
            db.session.commit()

            return {"data": {
                        "alumni": {
                            "alumni_id": alumni.alumni_id,
                            "odoo_contact_id": alumni.odoo_contact_id,
                            "alumni_uuid": alumni.alumni_uuid,
                            "email": alumni.email,
                            "password": alumni.password,
                            "user_confirmed": alumni.user_confirmed,
                        }},
                    "status": 201,
                    "error": None
                    }
        else:
            return {"data": {
                        "alumni": {
                            "alumni_id": alumni.alumni_id,
                            "odoo_contact_id": alumni.odoo_contact_id,
                            "alumni_uuid": alumni.alumni_uuid,
                            "email": alumni.email,
                            "password": alumni.password,
                            "user_confirmed": alumni.user_confirmed,
                        }},
                    "status": 200,
                    "error": f"Alumni already exists."
                    }

    @staticmethod
    def update_alumni_user(put_data):
        alumni = Alumni.query.filter_by(alumni_id=put_data.get('alumni_id')).first()
        alumni.user_confirmed = put_data.get('user_confirmed')
        db.session.add(alumni)
        db.session.commit()
        
        return {
            "data": None,
            "status": 200,
            "error": None
        }
