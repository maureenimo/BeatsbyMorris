from datetime import datetime
from configuration import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from configuration import bcrypt

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    
    order_items=db.relationship('OrderItem')
    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)
    orders = db.relationship('Order')
    reservation = db.relationship('Reservation')
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def authenticate(self, pwd):
        return bcrypt.check_password_hash(self.password_hash, pwd)
        

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    sub_total_price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    order_items = db.relationship(
        'OrderItem')
