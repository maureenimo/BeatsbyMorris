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

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SECRET_KEY'] = 'no_key'
app.config['JWT_SECRET_KEY'] = 'secret-key'

migrate = Migrate(app, db)
CORS(app)
api = Api(app)


db.init_app(app)
jwt = JWTManager(app)
Session(app)

mash = Marshmallow(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()

with app.app_context():
    # Check if the 'foods' table exists
    db.create_all()
    inspector = inspect(db.engine)
    # print all table names
    if 'foods' in inspector.get_table_names():
        print(inspector.get_table_names())