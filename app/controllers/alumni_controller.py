from app.main import db
from app.models.alumni_model import Alumni


class AlumniController:

    @staticmethod
    def get_all_alumni_ids():
        alumni_ids = db.session.query(Alumni.alumni_id).all()
        return alumni_ids

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
                            "email": alumni.email,
                            "password": alumni.password,
                        }},
                    "status": 201,
                    "error": None
                    }
        else:
            return {"data": {
                        "alumni": {
                            "alumni_id": alumni.alumni_id,
                            "odoo_contact_id": alumni.odoo_contact_id,
                            "email": alumni.email,
                            "password": alumni.password,
                        }},
                    "status": 200,
                    "error": f"Alumni {alumni.email} already exists."
                    }
