from app import app
from unittest import TestCase
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLACHEMY_ECHO'] = True
app.config['TESTING'] = True

class UserTestCase(TestCase):
    """test for model for Users"""

    def setUp(self):
        """clear the table contents and add user"""
        with app.app_context():
            db.create_all()
            db.session.commit()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """clear up all transactions"""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_showUsers(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)

    def test_addUser(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)

    def test_editUser(self):
        with app.test_client() as client:
            res = client.get('/users/1/edit')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)

    def test_deleteUser(self):
        with app.test_client() as client:
            res = client.get('/users/1/delete')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)

class PostTestCase(TestCase):
    """test model for posts"""
 
    def setUp(self):
        """clear the table contents and add user"""
        with app.app_context():
            db.create_all()
            db.session.commit()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """clear up all transactions"""
        with app.app_context():
            db.session.rollback()
            db.drop_all()
 
    def test_postForm(self):
        with app.test_client() as client:
            res = client.get('/users/1/posts/new')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
   
    def test_addPost(self):
        with app.test_client() as client:
            res = client.post('/users/1/posts/new', data={
            "title": "title",
            "content": "content",
            "post_image_url": "",
            })
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
 
    def test_showPost(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title="title", content="content", user_id=1)
                db.session.add(post)
                db.session.commit()
            res = client.get('/posts/1')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
 
    def test_postEditForm(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title="title", content="content", user_id=1)
                db.session.add(post)
                db.session.commit()
            res = client.get('/posts/1/edit')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
 
    def test_editPost(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title="title", content="content", user_id=1)
                db.session.add(post)
                db.session.commit()
            res = client.post('/posts/1/edit', data={
                "title": "abc",
                "content": "def",
                "post_image_url": "",
            })
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)

 
    def test_deletePost(self):
        with app.test_client() as client:
            with app.app_context():
                post = Post(title="title", content="content", user_id=1)
                db.session.add(post)
                db.session.commit()
            res = client.get('/posts/1/delete')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
 
 