from datetime import datetime

from app.main import db


class AlumniInviteStatus(db.Model):
    __tablename__ = "alumni_invite_status"

    odoo_contact_id = db.Column(db.String(50), primary_key=True)
    invite_status = db.Column(db.String(50))
    status_set_date = db.Column(db.Date)

    def __init__(self, odoo_contact_id, invite_status):
        self.odoo_contact_id = odoo_contact_id
        self.invite_status = invite_status
        self.status_set_date = datetime.now().date()
