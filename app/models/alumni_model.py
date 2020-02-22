from app.main import db, flask_bcrypt


class Alumni(db.Model):
    __tablename__ = "alumni"

    alumni_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    odoo_contact_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_confirmed = db.Column(db.Boolean())

    # repetition =  db.relationship("Repetition", back_populates="admin")

    def __init__(self, odoo_contact_id, email, password):
        self.odoo_contact_id = odoo_contact_id
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password).decode()
        self.user_confirmed = False

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)
