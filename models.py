import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(250), nullable=True, default='https://media.giphy.com/media/sFeYjWYUZtOE87iifm/giphy.gif')

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(250), nullable=False)

    content = db.Column(db.String(10000), nullable=False)

    image_url = db.Column(db.String(250), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

def connect_db(app):
    db.app = app
    db.init_app(app)


