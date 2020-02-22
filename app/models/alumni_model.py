from app.main import db


class Alumni(db.Model):
    __tablename__ = "alumni"

    alumni_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    odoo_contact_id = db.Column(db.String(100), unique=True, nullable=False)
    alumni_status = db.Column(db.String(100)) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_confirmed = db.Column(db.Boolean())

    # repetition =  db.relationship("Repetition", back_populates="admin")

    def __init__(self, odoo_contact_id, alumni_status, email, password, user_confirmed=False):
        self.odoo_contact_id = odoo_contact_id
        self.alumni_status = alumni_status
        self.email = email
        self.password = password
        self.user_confirmed = user_confirmed
