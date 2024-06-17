from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, schema
from flask_session import Session
from flask_restful import Api
from sqlalchemy import inspect
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager

app = Flask(__name__ , static_url_path='/static')
