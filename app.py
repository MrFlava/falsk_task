from flask import Flask
from flask_admin import Admin
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Column, Integer, String

from models import db, User, Item, DeliveryAddress

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'

db.init_app(app)

with app.app_context():
    db.create_all()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(DeliveryAddress, db.session))

if __name__ == '__main__':
    app.run(debug=True)
