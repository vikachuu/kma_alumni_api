from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/docs')

from app.namespaces.health_namespace import api_health
from app.namespaces.alumni_namespace import api_alumni
from app.namespaces.link_namespace import api_register_link
from app.namespaces.register_namespace import api_register
from app.namespaces.alumni_invite_status_namespace import api_alumni_invite_status

api.add_namespace(api_health)
api.add_namespace(api_alumni)
api.add_namespace(api_register_link)
api.add_namespace(api_register)
api.add_namespace(api_alumni_invite_status)
