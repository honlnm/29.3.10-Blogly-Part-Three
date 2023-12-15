import os
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLACHEMY_ECHO'] = True
app.config['TESTING'] = False
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    """shows list of all users in db"""
    users = User.query.all()
    return render_template('user-listing.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    """show new user form"""
    return render_template('new-user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """create new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if request.form["image_url"] != "":
        image_url = request.form["image_url"]
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    else:
        new_user = User(first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:userId>/edit')
def display_user(userId):
    """show selected user for edit"""
    user = User.query.get(userId)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:userId>/edit', methods=["POST"])
def edit_user(userId):
    """edit selected user"""
    user = User.query.get(userId)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if request.form["image_url"] != "":
        image_url = request.form["image_url"]
        user.image_url = image_url

    user.first_name = first_name
    user.last_name = last_name

    db.session.add(user)
    db.session.commit()

    return redirect('/users')
    

@app.route('/users/<int:userId>')
def show_user(userId):
    """show details about a single user"""
    user = User.query.get_or_404(userId)
    posts = Post.query.filter_by(user_id=userId)
    return render_template("user-detail.html", user=user, posts=posts)

@app.route('/users/<int:userId>/delete')
def delete_user(userId):
    """delete selected user"""
    row = User.query.filter(User.id == userId)

    row.delete()
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:userId>/posts/new')
def post_form(userId):
    """create user post"""
    user = User.query.get_or_404(userId)
    return render_template("create-post.html", user=user)

@app.route('/users/<int:userId>/posts/new', methods=['POST'])
def create_post(userId):
    """log post to db and redirect"""
    title = request.form["title"]
    content = request.form["content"]
    user_id = userId
    if request.form["post_image_url"] != "":
        image_url = request.form["post_image_url"]
        new_post = Post(title=title, content=content, image_url=image_url, user_id=user_id)
    else:
        new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect('/users/' + str(userId))
 
@app.route('/posts/<int:postId>')
def show_post(postId):
    """show details about a single post"""
    post = Post.query.get_or_404(postId)
    user = User.query.get_or_404(post.user_id)
    return render_template("post-detail.html", user=user, post=post)

@app.route('/posts/<int:postId>/edit')
def display_post(postId):
    """show selected post for edit"""
    post = Post.query.get(postId)
    user = User.query.get_or_404(post.user_id)
    return render_template('edit-post.html', post=post, user=user)

@app.route('/posts/<int:postId>/edit', methods=['POST'])
def edit_post(postId):
    """edit selected post"""
    post = Post.query.get(postId)
    user = User.query.get_or_404(post.user_id)
    title = request.form["title"]
    content = request.form["content"]
    if request.form["post_image_url"] != "":
        image_url = request.form["post_image_url"]
        post.image_url = image_url

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect('/posts/' + str(postId))

@app.route('/posts/<int:postId>/delete')
def delete_post(postId):
    """delete selected post"""
    row = Post.query.filter(Post.id == postId)

    row.delete()
    db.session.commit()

    return redirect('/')