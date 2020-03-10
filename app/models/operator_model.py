from app.main import db, flask_bcrypt


class Operator(db.Model):
    __tablename__ = "operator"

    operator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean)

    def __init__(self, username, email, password, is_admin):
        self.username = username
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password).decode()
        self.is_admin = is_admin if is_admin is not None else False

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)
