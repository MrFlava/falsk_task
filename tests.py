import os
import unittest
import sqlite3

from app import secureApp, db
from models import Users, Items, DeliveryAddress


class AppTestCase(unittest.TestCase):

    def test_index(self):
        tester = secureApp.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists("test_database.db")
        self.assertTrue(tester)


class RequestsTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        secureApp.config['TESTING'] = True
        secureApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        self.app = secureApp.test_client()
        context = secureApp.app_context()
        context.push()

    def test_example(self):
        with secureApp.app_context():
            db.init_app(secureApp)
            db.drop_all()
            db.create_all()

    def tearDown(self):
        db.drop_all()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    # assert functions

    def test_empty_db(self):
        """Ensure database is blank"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login('admin', 'admin')
        self.assertEqual(rv.status_code, 200)
        rv = self.logout()
        self.assertEqual(rv.status_code, 200)

    def test_add_user(self):

        db.drop_all()
        db.create_all()

        users = Users()
        users.email = 'email@email.com'
        users.password = 'admin123123'
        users.active = False

        db.session.add(users)
        db.session.commit()

        self.assertEqual(len(db.session.query(Users).all()), 1)

    def test_add_item(self):

        db.drop_all()
        db.create_all()

        items = Items(color='', weight=0, price=0)
        items.color = 'white'
        items.weight = 200
        items.price = 100

        db.session.add(items)
        db.session.commit()

        self.assertEqual(len(db.session.query(Items).all()), 1)

    def test_add_address(self):
        db.drop_all()
        db.create_all()

        items = DeliveryAddress(country='', city='', street='')
        items.color = 'white'
        items.weight = 200
        items.price = 100

        db.session.add(items)
        db.session.commit()

        self.assertEqual(len(db.session.query(DeliveryAddress).all()), 1)


if __name__ == '__main__':
    unittest.main()
