from flask_restful import Resource, Api, reqparse 

from resource.utils import min_length_str
from restdemo.app import db
from restdemo.model.user import User as UserModel

class Login(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument(
    'password', 
    type=min_length_str(5), 
    required=True, 
    help='password {error_msg}'
  )
  parser.add_argument(
    'username',
    type=str,
    required=True,
    help='required username'
  )

  def post(self):
    data = Login.parser.parse_args()
    user = db.session.query(UserModel).filter(UserModel.username == data["username"]).first()

    if not user or not user.check_password(data['password']): 
      return { "message": "Please check username or password" }, 404  

    return { 
      "message": "login successful",
      "token": user.generate_token()
    }, 201