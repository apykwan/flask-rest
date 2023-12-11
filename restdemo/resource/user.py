from flask import request, current_app
from flask_restful import Resource, Api, reqparse

from restdemo.resource.utils import min_length_str, jwt_required
from restdemo.model.user import User as UserModel

class User(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument(
    'password', 
    type=min_length_str(5), 
    required=True, 
    help='password {error_msg}'
  )
  parser.add_argument(
    'email',
    type=str,
    required=True,
    help='required email'
  )

  def get(self, username):
    user = UserModel.get_by_username(username)
    if not user: return { "message": "user not found" }
    
    return user.as_dict(), 201

  def post(self, username):
    check_exist_user = UserModel.get_by_username(username)
    if check_exist_user: return { "message": "username has been taken" }
      
    data = User.parser.parse_args()
    user = UserModel(
      username=username,
      email=data['email']
    )
    user.set_password(data['password'])

    user.add()
    return user.as_dict(), 201

  def delete(self, username):
    user = UserModel.get_by_username(username)
    if not user: return { "message": "no such user" }, 404

    user.delete()
    return { "message": "user deleted" }, 200

  def put(self, username):
    user = UserModel.get_by_username(username)
    if not user: return { "message": "no such user" }, 404

    data = User.parser.parse_args()
    user.email = data['email']
    user.set_password(data['password'])
    user.update()
    return user.as_dict(), 201

class UserList(Resource):
  @jwt_required
  def get(self):
    users = UserModel.get_user_list()
    return [u.as_dict() for u in users]