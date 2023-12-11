# import unittest
# import json
# from werkzeug.security import check_password_hash

# from restdemo import create_app, db

# class TestLogin(unittest.TestCase):
#   def setUp(self):
#     self.app = create_app(config_name='testing')
#     self.client = self.app.test_client
#     self.user_data = {
#       'username': 'test',
#       'password': 'test123',
#       'email': 'test@test.com'
#     }
#     with self.app.app_context():
#       db.create_all()
  
#   def tearDown(self):
#     with self.app.app_context():
#       db.session.remove()

#   def test_login(self):
#     # create an user
#     url = f"/user/{self.user_data['username']}"
#     self.client().post(
#       url,
#       data=json.dumps(self.user_data),
#       content_type='application/json'
#     )   

#     url = '/auth/login'
#     res = self.client().post(
#       url,
#       data=json.dumps({
#         'username': 'test',
#         'password': 'test123'
#       }),
#       content_type='application/json'
#     )

#     res_data = json.loads(res.get_data(as_text=True))
#     self.assertEqual(res.status_code, 201)
#     self.assertEqual(res_data.get('message'), "login successful")

#   def test_login_failed(self):
#     # create an user
#     url = f"/user/{self.user_data['username']}"
#     self.client().post(
#       url,
#       data=json.dumps(self.user_data),
#       content_type='application/json'
#     )   

#     url = '/auth/login'
#     res = self.client().post(
#       url,
#       data=json.dumps({
#         'username': 'test',
#         'password': 'test1234'
#       }),
#       content_type='application/json'
#     )

#     res_data = json.loads(res.get_data(as_text=True))
#     self.assertEqual(res.status_code, 404)
#     self.assertEqual(res_data.get('message'), "Please check username or password")

  