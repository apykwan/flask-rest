import unittest
import json
from werkzeug.security import check_password_hash

from restdemo import create_app, db

class TestLogin(unittest.TestCase):
  def setUp(self):
    self.app = create_app(config_name='testing')
    self.client = self.app.test_client
    self.user_data = {
      'username': 'test',
      'password': 'test123',
      'email': 'test@test.com'
    }
    with self.app.app_context():
      db.create_all()
  
  def tearDown(self):
    with self.app.app_context():
      db.session.remove()

  def login(self):
    # create an user
    self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    )   

    url = '/auth/login'
    res = self.client().post(
      url,
      data=json.dumps({
        'password': 'test123',
        'email': 'test@test.com'
      }),
      content_type='application/json'
    )
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 200)
    print(res_data)
    self.assertEqual("token", res_data)