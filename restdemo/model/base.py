from restdemo import db

class Base(db.Model):
  __abstract__ = True
  __table_args__ = { 'extend_existing': True }
  
  def add(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()