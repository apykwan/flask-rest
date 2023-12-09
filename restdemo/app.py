from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from resource.tweet import Tweet 
from resource.user import User, UserList
from resource.hello import Helloworld
from resource.auth import Login
from config import Config


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Routes
api.add_resource(Helloworld, '/')
api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:username>')
api.add_resource(Login, '/auth/login')
api.add_resource(Tweet, '/tweet/<string:username>')

if __name__ == "__main__":
  app.run()