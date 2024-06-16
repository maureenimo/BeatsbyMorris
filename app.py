from flask import Flask, make_response, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Address, db, Food, User, Review, Location
from requests.auth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
import requests
import base64
from datetime import datetime
from sqlalchemy import inspect
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False  
app.config['MAIL_USERNAME'] = 'nimz69509@gmail.com'
app.config['MAIL_PASSWORD'] = 'zabc lnoq cbkv nupc'
app.config['MAIL_DEFAULT_SENDER'] = 'nimz69509@gmail.com'
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

mail = Mail(app)