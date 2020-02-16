import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS

from xmlrpc import client

from app.api import blueprint as api


web_app = Flask("Alumni sevice")
web_app.config.from_object('config')

web_app.register_blueprint(api, url_prefix='/api/v1')

db = SQLAlchemy(web_app)
heroku = Heroku(web_app)
cors = CORS(web_app, resources={r"/api/*": {"origins": "*"}})

# initialize Odoo
odoo_url = os.getenv('ODOO_URL')
odoo_db = os.getenv('ODOO_DB')
odoo_username = os.getenv('ODOO_USERNAME')
odoo_password = os.getenv('ODOO_PASSWORD')

odoo_common = client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
odoo_uid = odoo_common.authenticate(odoo_db, odoo_username, odoo_password, {})
odoo_models = client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))


if __name__ == "__main__":
    web_app.run("0.0.0.0", 8080)
