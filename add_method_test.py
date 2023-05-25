import unittest
from flask_testing import TestCase
from flask_blog import app, db, Users, Post


class TestAddRoute(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        user = Users(login='testuser', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        user = Users.query.filter_by(login='testuser').first()
        if user:
            db.session.delete(user)
        post = Post.query.filter_by(title='Test Post').first()
        if post:
            db.session.delete(post)
        db.session.commit()
        db.session.remove()

    def test_add_route(self):
        with self.client:
            self.client.set_cookie('/', 'username', 'testuser')

            response = self.client.post('/add', data={'title': 'Test Post', 'body': 'test post'})

            post = Post.query.order_by(Post.id.desc()).first()
            self.assertIsNotNone(post)
            self.assertEqual(post.title, 'Test Post')
            self.assertEqual(post.body, 'test post')


if __name__ == '__main__':
    unittest.main()
