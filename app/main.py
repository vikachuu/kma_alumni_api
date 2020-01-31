import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS

from app.api import blueprint as api


web_app = Flask("Alumni sevice")
web_app.config.from_object('config')

web_app.register_blueprint(api, url_prefix='/api/v1')

db = SQLAlchemy(web_app)
heroku = Heroku(web_app)
cors = CORS(web_app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    web_app.run("0.0.0.0", 8080)