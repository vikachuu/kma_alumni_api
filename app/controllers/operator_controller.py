from app.main import db
from app.models.operator_model import Operator


class OperatorController:

    @staticmethod
    def create_operator_user(post_data):
        # check if user already exists
        operator = Operator.query.filter_by(email=post_data.get('email')).first()
        if not operator:
            operator = Operator(
                username=post_data.get('username'),
                email=post_data.get('email'),
                password=post_data.get('password'),
                is_admin=post_data.get('is_admin'),
            )

            # insert the user
            db.session.add(operator)
            db.session.commit()

            return {"data": {
                        "operator": {
                            "operator_id": operator.operator_id,
                            "username": operator.username,
                            "email": operator.email,
                            "password": operator.password,
                            "is_admin": operator.is_admin,
                        }},
                    "status": 201,
                    "error": None
                    }
        else:
            return {"data": {
                        "operator": {
                            "operator_id": operator.operator_id,
                            "username": operator.username,
                            "email": operator.email,
                            "password": operator.password,
                            "is_admin": operator.is_admin,
                        }},
                    "status": 200,
                    "error": f"Alumni already exists."
                    }

    @staticmethod
    def get_operator_by_id(operator_id):
        operator = Operator.query.filter_by(operator_id=operator_id).first()
        if not operator:
            return {
                "data": None,
                "status": 404,
                "error": "No such operator exists."
            }

        else:
            return {"data": {
                        "operator": {
                            "operator_id": operator.operator_id,
                            "username": operator.username,
                            "email": operator.email,
                            "password": operator.password,
                            "is_admin": operator.is_admin,
                        }},
                    "status": 200,
                    "error": None
                    }

    @staticmethod
    def get_operator_by_email(email):
        operator = Operator.query.filter_by(email=email).first()
        return operator