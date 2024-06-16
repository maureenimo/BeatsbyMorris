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


with app.app_context():
    # Check if the 'foods' table exists
    db.create_all()
    inspector = inspect(db.engine)
        # print all table names
    if 'foods' in inspector.get_table_names():
        print(inspector.get_table_names())
        

#Mpesa
consumer_key='7GSlEmZiocYKga9acUBDyIYiuJqOvZvHd6XGzbcVZadPm93f'
consumer_secret='Vh2mvQS4GKyo6seUtpAApN1plTwMDTeqyGZNBEtESYH05sBfRMSddn5vnlJ4zifA'
base_url='https://1115-105-161-25-71.ngrok-free.app'

#Dishes API
@app.route('/dishes', methods=['GET'])
def get_foods():
    foods = []
    for food in Food.query.all():
        response_body = {
            "id": food.id,
            "name": food.name,
            "image": food.image,
            "description": food.description,
            "price": food.price
        }
        foods.append(response_body)

    response = make_response(
        jsonify(foods),
        200
    )
    return response


#register users
@app.route('/user', methods=['POST'])
def register_user():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return make_response(jsonify({"error": "User with this email already exists"}), 409)

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "phone": new_user.phone,
        "created_at": new_user.created_at,
    }

    return make_response(jsonify(response_body), 201)
    

# View all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    if users:
        users_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "created_at": user.created_at,
            }
            users_list.append(user_data)

        return make_response(jsonify(users_list), 200)
    else:
        return make_response(jsonify({"error": "No users found"}), 404)
