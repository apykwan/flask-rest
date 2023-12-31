import jwt
from flask import current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

from restdemo import db
from restdemo.model.base import Base

class User(Base):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  password = db.Column(db.String(255))
  email = db.Column(db.String(64))
  
  tweet = relationship('Tweet')

  def __repr__(self):
    return f"id={self.id} username={self.username} email={self.email}"
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  def set_password(self, password):
        self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def generate_token(self):
    try:
      payload = {
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
        'sub': self.username
      }

      jwt_token = jwt.encode(
        payload,
        current_app.config.get('SECRET'),
        algorithm='HS256'
      )
      return jwt_token
    
    except Exception as error:
      return str(error)
  
  @staticmethod
  def get_by_username(username):
    return db.session.query(User).filter(User.username == username).first()

  @staticmethod
  def get_by_id(id):
    return db.session.query(User).filter(User.id == id).first()

  @staticmethod
  def get_user_list():
    return db.session.query(User).all()