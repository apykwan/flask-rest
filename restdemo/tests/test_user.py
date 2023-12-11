import unittest
import json
from werkzeug.security import check_password_hash

from restdemo import create_app, db

class TestUser(unittest.TestCase):
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
      db.drop_all()

  def test_user_create(self):
    url = f"/user/{self.user_data['username']}"

    # insert an user
    res = self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    )   
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 201)
    self.assertEqual(res_data.get('username'), self.user_data['username'])
    self.assertEqual(res_data.get('email'), self.user_data['email'])

    # insert user with same username
    res = self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    )
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res_data.get('message'), "username has been taken")

  def test_user_delete(self):
    url = f"/user/{self.user_data['username']}"

    # insert an user
    res = self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    ) 

    # delete the user
    res = self.client().delete(url)
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res_data, { "message": "user deleted" })

  def test_user_delete_not_exist(self):
    url = f"/user/{self.user_data['username']}"
    res = self.client().delete(url)
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 404)
    self.assertEqual(res_data, { "message": "no such user" })

  def test_user_update(self):
    url = f"/user/{self.user_data['username']}"

     # insert an user
    res = self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    ) 

    # update user's email and password
    res = self.client().put(
      url,
      data=json.dumps({
        "password": "newpassword",
        "email": "new@new.com"
      }),
      content_type='application/json'
    )
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 201)
    self.assertEqual(res_data.get('email'), 'new@new.com')
    self.assertEqual(check_password_hash(res_data.get('password'), 'newpassword'), True)

  def test_user_update_not_exist(self):
    url = f"/user/{self.user_data['username']}"

     # update user's email and password
    res = self.client().put(
      url,
      data=json.dumps({
        "password": "newpassword",
        "email": "new@new.com"
      }),
      content_type='application/json'
    )
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 404)
    self.assertEqual(res_data, { "message": "no such user" })

