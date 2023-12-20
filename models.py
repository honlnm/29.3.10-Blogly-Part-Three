import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(250), nullable=True, default='https://media.giphy.com/media/sFeYjWYUZtOE87iifm/giphy.gif')

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(250), nullable=False)

    content = db.Column(db.String(10000), nullable=False)

    image_url = db.Column(db.String(250), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class PostTag(db.Model):
    __tablename__="post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

    __table_args__ = (PrimaryKeyConstraint('post_id','tag_id'),)

class Tag(db.Model):
    __tablename__= "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(30), nullable=False, unique=True)

    posts = db.relationship('Post', secondary="post_tags", backref="tags",)

def connect_db(app):
    db.app = app
    db.init_app(app)


