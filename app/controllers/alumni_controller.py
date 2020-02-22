from app.main import db
from app.models.alumni_model import Alumni


class AlumniController:

    @staticmethod
    def get_all_alumni_ids():
        alumni_ids = db.session.query(Alumni.alumni_id).all()
        return alumni_ids
