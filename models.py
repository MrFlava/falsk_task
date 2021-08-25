from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username


class Item(db.Model):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True)
    color = Column(String(80))
    weight = Column(Integer, default=0)
    price = Column(Integer, default=0)

    def __init__(self, color, weight, price):
        self.color = color
        self.weight = weight
        self.price = price

    def __repr__(self):
        return '<Item %r>' % self.color


class DeliveryAddress(db.Model):
    __tablename__ = 'Delivery'
    id = Column(Integer, primary_key=True)
    country = Column(String(120))
    city = Column(String(120))
    street = Column(String(120))

    def __init__(self, country, city, street):
        self.country = country
        self.city = city
        self.street = street

    def __repr__(self):
        return '<Address %r>' % self.country

