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