import unittest
from flask_testing import TestCase
from flask_blog import app, db, Users, Post, Comments


class TestAddDeleteCommentsRoutes(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        user = Users(login='testuser', password='password')
        db.session.add(user)
        post = Post(userId='1', title='test post', body='test post')
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        comment = Comments.query.filter_by(name='test comment').first()
        if comment:
            db.session.delete(comment)
        post = Post.query.filter_by(title='test post').first()
        if post:
            db.session.delete(post)
        user = Users.query.filter_by(login='testuser').first()
        if user:
            db.session.delete(user)
        db.session.commit()
        db.session.remove()

    def test_add_route(self):
        response = self.client.post('/add_comment/'+str(Post.query.filter_by(title='test post').first().id), data={'name': 'test comment', 'email':'test@email.com', 'body': 'test content'})
        comment = Comments.query.filter_by(name='test comment').first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.name, 'test comment')
        self.assertEqual(comment.body, 'test content')
        self.assertEqual(comment.email, 'test@email.com')

    def test_delete_route(self):
        comment = Comments(postId='999', name='test comment', email='test@email.com', body='test content')
        db.session.add(comment)
        db.session.commit()
        comment_id = Comments.query.filter_by(name='test comment').first().id
        response = self.client.get(f'/delete_comment/{comment_id}')
        post = Post.query.filter_by(id=comment_id).first()
        self.assertIsNone(post)


if __name__ == '__main__':
    unittest.main()
