from sqlalchemy import ForeignKey, func
from datetime import datetime

from restdemo.app import db

class Tweet(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = "tweet"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey('user.id'))
  body = db.Column(db.String(140))
  created_at = db.Column(db.DateTime, server_default=func.now())

  def __repr__(self):
    return "user_id={}, tweet={}".format(
        self.user_id, self.body
    )
  
  def add(self):
    db.session.add(self)
    db.session.commit()

  def as_dict(self):
    t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    t['created_at'] = t['created_at'].isoformat()
    return t

  @staticmethod
  def get_tweets_by_user(user_id):
    return db.session.query(Tweet).filter(Tweet.user_id == user_id).all()