from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin

db = SQLAlchemy()

roles_users_table = db.Table(
    "roles_users",
    db.Column("users_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("roles_id", db.Integer(), db.ForeignKey("roles.id")),
)


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())

    roles = db.relationship("Roles", secondary=roles_users_table, backref="user", lazy=True)


class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(80))
    weight = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)

    def __init__(self, color, weight, price):
        self.color = color
        self.weight = weight
        self.price = price

    def __repr__(self):
        return "<Item %r>" % self.color


class DeliveryAddress(db.Model):
    __tablename__ = "delivery"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(120))
    city = db.Column(db.String(120))
    street = db.Column(db.String(120))

    item_id = db.Column(db.BigInteger, db.ForeignKey("items.id"), nullable=False, index=True)
    item = db.relationship("Items", backref="delivery_addresses", foreign_keys=[item_id])

    def __init__(self, country, city, street, item):
        self.country = country
        self.city = city
        self.street = street
        self.item = item

    def __repr__(self):
        return "<Address %r>" % self.country
