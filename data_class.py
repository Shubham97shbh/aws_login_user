from models import *

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_data = relationship('Data', back_populates='data_c')


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    data_c = relationship('User', back_populates='user_data')
    data_link = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Boolean,default=False,nullable=False)

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer,primary_key=True)
    state = db.Column(db.String(100),nullable=False)
    lat = db.Column(db.Float,nullable=False)
    long = db.Column(db.Float,nullable=False)

db.create_all()
