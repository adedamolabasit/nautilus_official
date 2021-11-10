from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import LoginManager

# from authlib.integrations.flask_client import OAuth
# from six.moves.urllib.parse import urlencode



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nautilus5he!@localhost:5432/nauts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)




from create import app