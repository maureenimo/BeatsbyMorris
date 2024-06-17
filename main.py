from flask_restful import Resource
from flask import Flask, make_response, jsonify, request, json, session
from configuration import db, mash, api, app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Address, Food, User, Review, Location, Reservation, Order, OrderItem, Payment
from flask_restful import Api, Resource, reqparse
import requests
import base64
from datetime import datetime
from configuration import db, mash, api, app, auth
from flask_jwt_extended import create_access_token, jwt_required
from flask_mail import Message
from flask_mail import Mail
import traceback
from requests.auth import HTTPBasicAuth
import os




class Index(Resource):
    def get(self):
        return make_response(
            "Venina API", 200
        )

api.add_resource(Index, '/')


def User_details(user):
    return make_response(
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone}, 200
    )

# login
class Login(Resource):
    def post(self):
        user_signIn = request.get_json()
        password = user_signIn['password']
        user = User.query.filter_by(email=user_signIn['email']).first()

        if user:
            if user.authenticate(password):
                access_token = create_access_token(identity=user.email)
                return {'access_token': access_token}, 200

            return "Enter Correct Username or Password", 400
        return "No such user exists", 404

api.add_resource(Login, '/login')


class CheckSession(Resource):
    def get(self):
        user = session.get('user')
        user_info = User.query.filter_by(email=user).first()

        if user:
            return User_details(user_info)

        return "Please signIn to continue", 404


api.add_resource(CheckSession, '/checksession')

# logout
class Logout(Resource):
    def delete(self):
        user = session.get('user')

        if user:
            session['user'] = None

            return "LogOut Successful", 200
        return make_response("Method not allowed", 404)


api.add_resource(Logout, '/logout')

class UserSchema(mash.SQLAlchemySchema):
    
    class Meta:
        model = User
        load_instance = True

    id = mash.auto_field()
    first_name = mash.auto_field()
    last_name = mash.auto_field()
    email = mash.auto_field()
    phone = mash.auto_field()
    first_name = mash.auto_field()

    url = mash.Hyperlinks(
        {
            "self": mash.URLFor(
                "userbyid",
                values=dict(id="<id>")),
            "collection": mash.URLFor("users")
        }
    )


user_schema = UserSchema()
users_schema = UserSchema(many=True)


