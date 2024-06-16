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