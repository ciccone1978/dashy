import unittest
import logging
import sys
from apps import create_app, db
from apps.authentication.models import Users
from apps.config import Config
from flask import current_app
import jwt
from time import time

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("TestLog")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Users(username='Susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))   

    def test_reset_password_token(self):
        secret = 'd99AA'
        u1 = Users(username='Susan')
        db.session.add(u1)
        db.session.commit()

        token = jwt.encode({'reset_password':u1.id, 'exp':time()+600}, secret, algorithm='HS256')
        id = jwt.decode(token, secret, algorithms='HS256')['reset_password']
        
        #token = u1.get_reset_password_token()
        #self.log.debug(token)
        #u2 = Users.verify_reset_password_token(token)
        self.assertEqual(u1, Users.query.get(id))
        #self.assertEqual(u1.id, u2.id)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)