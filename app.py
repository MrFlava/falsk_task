from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore

import local_settings
from models import db, Users, Roles, Items, DeliveryAddress

# Instantiate the Flask application with configurations
secureApp = Flask(__name__)
# Configure a specific Bootswatch theme
secureApp.config['FLASK_ADMIN_SWATCH'] = local_settings.FLASK_ADMIN_SWATCH
secureApp.config['SECRET_KEY'] = local_settings.SECRET_KEY
secureApp.config['SECURITY_PASSWORD_SALT'] = local_settings.SECURITY_PASSWORD_SALT
# Configure application to route to the Flask-Admin index view upon login
secureApp.config['SECURITY_POST_LOGIN_VIEW'] = local_settings.SECURITY_POST_LOGIN_VIEW
# Configure application to route to the Flask-Admin index view upon logout
secureApp.config['SECURITY_POST_LOGOUT_VIEW'] = local_settings.SECURITY_POST_LOGOUT_VIEW
# Configure application to route to the Flask-Admin index view upon registering
secureApp.config['SECURITY_POST_REGISTER_VIEW'] = local_settings.SECURITY_POST_REGISTER_VIEW
secureApp.config['SECURITY_REGISTERABLE'] = local_settings.SECURITY_REGISTERABLE
# Configure application to not send an email upon registration
secureApp.config['SECURITY_SEND_REGISTER_EMAIL'] = local_settings.SECURITY_SEND_REGISTER_EMAIL
secureApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = local_settings.SQLALCHEMY_TRACK_MODIFICATIONS
secureApp.config['SQLALCHEMY_DATABASE_URI'] = local_settings.SQLALCHEMY_DATABASE_URI

db.init_app(secureApp)

# Create a datastore and instantiate Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(secureApp, user_datastore)


# Create the tables for the users and roles and add a user to the user table
# This decorator registers a function to be run before the first request to the app
# @secureApp.before_first_request
# def create_user():
#     db.drop_all()
#     db.create_all()
#     user_datastore.create_user(email='admin', password='admin')
#     db.session.commit()


# Instantiate Flask-Admin
admin = Admin(secureApp, name='Admin', base_template='my_master.html', template_mode='bootstrap4')


# Create a ModelView to add to our administrative interface
class UserModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    column_list = ['email', 'password']


# Add administrative views to Flask-Admin
admin.add_view(UserModelView(Users, db.session))
admin.add_view(ModelView(Items, db.session))
admin.add_view(ModelView(DeliveryAddress, db.session))


# Add the context processor
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for,
        h=admin_helpers
    )


# Define the index route
@secureApp.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    # app_dir = os.path.realpath(os.path.dirname(__file__))
    # database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    #     build_sample_db()

    # Start app
    secureApp.run(debug=True)

