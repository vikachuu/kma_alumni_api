import uuid
from app.main import db, flask_bcrypt


class Alumni(db.Model):
    __tablename__ = "alumni"

    alumni_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumni_uuid = db.Column(db.String(50), unique=True)
    odoo_contact_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_confirmed = db.Column(db.Boolean())
    allow_show_contacts = db.Column(db.Boolean())

    def __init__(self, odoo_contact_id, email, password, allow_show_contacts):
        self.alumni_uuid = str(uuid.uuid4())
        self.odoo_contact_id = odoo_contact_id
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password).decode()
        self.user_confirmed = False
        self.allow_show_contacts = allow_show_contacts

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)
