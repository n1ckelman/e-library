from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir
from flask.ext.login import LoginManager
#from flask_googlelogin import GoogleLogin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
#googlelogin = GoogleLogin(app, login_manager)

from app import views, models