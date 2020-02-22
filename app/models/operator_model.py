from app.main import db


class Operator(db.Model):
    __tablename__ = "operator"

    operator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, operator_id, username, email, password):
        self.username = username
        self.email = email
        self.password = password
