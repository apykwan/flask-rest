import json

from restdemo.tests.base import Base

class TestTeet(Base):
  def test_post_tweet(self):
    # Insert an user
    url = f"/user/{self.user_data['username']}"
    self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    )   
  
    # login the user
    url = '/auth/login'
    res = self.client().post(
      url,
      data=json.dumps({
        'username': 'test',
        'password': 'test123'
      }),
      content_type='application/json'
    )  

    res_data = json.loads(res.get_data(as_text=True))
    token = res_data.get("token")

    # create tweet
    url = f"/tweet/{self.user_data['username']}"
    res = self.client().post(
      url,
      data=json.dumps({
        'body': 'my first tweet'
      }),
      headers={
        'Authorization': token,
        'Content-Type': 'application/json'
      }
    )
    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 201)
    self.assertEqual(res_data.get("message"), "post success")

  def test_get_tweet(self):
    # Insert an user
    url = f"/user/{self.user_data['username']}"
    self.client().post(
      url,
      data=json.dumps(self.user_data),
      content_type='application/json'
    )   
  
    # login the user
    url = '/auth/login'
    res = self.client().post(
      url,
      data=json.dumps({
        'username': 'test',
        'password': 'test123'
      }),
      content_type='application/json'
    )  

    res_data = json.loads(res.get_data(as_text=True))
    token = res_data.get("token")

    # create tweet
    url = f"/tweet/{self.user_data['username']}"
    res = self.client().post(
      url,
      data=json.dumps({
        'body': 'my first tweet'
      }),
      headers={
        'Authorization': token,
        'Content-Type': 'application/json'
      }
    )

    # fetch tweets by username
    url = f"/tweet/{self.user_data['username']}"
    res = self.client().get(url)

    res_data = json.loads(res.get_data(as_text=True))
    self.assertEqual(res.status_code, 201)
    self.assertEqual(len(res_data), 1)
    