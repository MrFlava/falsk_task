from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from flask_security import current_user, login_required, RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin

from database import Base

db = SQLAlchemy()


class RolesUsers(Base):
    __tablename__ = 'roles_users'

    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'

    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Item(Base):
    __tablename__ = 'item'

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


class DeliveryAddress(Base):
    __tablename__ = 'delivery'

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
