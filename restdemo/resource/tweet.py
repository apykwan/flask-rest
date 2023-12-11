from flask_restful import Resource, reqparse

from restdemo.resource.utils import jwt_required
from restdemo.model.user import User as UserModel
from restdemo.model.tweet import Tweet as TweetModel

class Tweet(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument(
    'body', type=str, required=True,
    help='body required'
  )

  @jwt_required
  def post(self, username, sub):
    if sub != username:
        return {'message': 'please use the right token'}
    user = UserModel.get_by_username(username)
    if not user:
        return {'message': 'user not found'}, 404
    data = Tweet.parser.parse_args()
    tweet = TweetModel(body=data['body'], user_id=user.id)
    tweet.add()
    return {'message': 'post success'}, 201

  def get(self, username):
    user = UserModel.get_by_username(username)

    if not user:
        return {'message': 'user not found'}, 404

    tweets = TweetModel.get_tweets_by_user(user.id)
    return [t.as_dict() for t in tweets], 201