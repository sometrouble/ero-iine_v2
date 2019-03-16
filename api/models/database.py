from flask_sqlalchemy import SQLAlchemy

from main import api
from settings import SETTINGS

api.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['DATABASE_URL']
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(api)
