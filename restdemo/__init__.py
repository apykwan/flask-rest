from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from restdemo.resource.tweet import Tweet 
from restdemo.resource.user import User, UserList
from restdemo.resource.hello import Helloworld
from restdemo.resource.auth import Login
from restdemo.config import app_config

def create_app(config_name='development'):
  app = Flask(__name__)
  api = Api(app)

  app.config.from_object(app_config[config_name])

  db.init_app(app)
  migrate = Migrate(app, db)

  # Routes
  api.add_resource(Helloworld, '/')
  api.add_resource(UserList, '/users')
  api.add_resource(User, '/user/<string:username>')
  api.add_resource(Login, '/auth/login')
  api.add_resource(Tweet, '/tweet/<string:username>')

  return app