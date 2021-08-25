from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask import Flask, render_template, url_for, redirect
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, current_user, login_required, SQLAlchemySessionUserDatastore

from database import db_session, init_db
from models import db, User, Role, Item, DeliveryAddress

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
app.config['SECURITY_PASSWORD_SALT'] = 'some arbitrary super secret string'

user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

# Create a user to test with

#
# @app.before_first_request
# def create_user():
#     init_db()
#     user_datastore.create_user(email='matt@nobien.net', password='password')
#     db_session.commit()


# admin = Admin(app)
# admin.add_view(ModelView(User, db_session))
# admin.add_view(ModelView(Role, db_session))
# admin.add_view(ModelView(Item, db_session))
# admin.add_view(ModelView(DeliveryAddress, db_session))


class MyAdminIndexView(AdminIndexView):
    pass


admin = Admin(app, 'Admin Area', template_mode='bootstrap4', index_view=MyAdminIndexView())


@login_required
@app.route('/login')
def login():
    return redirect('/admin')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
