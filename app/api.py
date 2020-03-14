from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/docs')

from app.namespaces.health_namespace import api_health
from app.namespaces.alumni_namespace import api_alumni
from app.namespaces.operator_namespace import api_operator
from app.namespaces.link_namespace import api_register_link
from app.namespaces.register_namespace import api_register
from app.namespaces.alumni_invite_status_namespace import api_alumni_invite_status
from app.namespaces.confirm_namespace import api_confim
from app.namespaces.login_namespace import api_login
from app.namespaces.operator_login_namespace import api_operator_login
from app.namespaces.update_form_namespace import api_update_form


api.add_namespace(api_health)
api.add_namespace(api_alumni)
api.add_namespace(api_operator)
api.add_namespace(api_register_link)
api.add_namespace(api_register)
api.add_namespace(api_alumni_invite_status)
api.add_namespace(api_confim)
api.add_namespace(api_login)
api.add_namespace(api_operator_login)
api.add_namespace(api_update_form)
