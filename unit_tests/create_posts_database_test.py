import unittest
from unittest.mock import patch, MagicMock
from flask_blog import app, db, Post, create_posts_database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class CreatePostsDatabaseTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            app.testing = True
            db.create_all()

    def tearDown(self):
        with app.app_context():
            post = Post.query.filter_by(title='Test Title').first()
            db.session.delete(post)
            db.session.commit()
            db.session.remove()

    @patch('flask_blog.requests.get')
    def test_create_posts_database(self, mock_get):
        with app.app_context():
            mock_response = MagicMock()
            mock_response.text = '[{"userId": 1, "title": "Test Title", "body": "Test Body"}]'
            mock_get.return_value = mock_response
            result = create_posts_database()

            self.assertTrue(result)
            post = Post.query.filter_by(title="Test Title").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.userId, 1)
            self.assertEqual(post.title, 'Test Title')
            self.assertEqual(post.body, 'Test Body')


if __name__ == '__main__':
    unittest.main()
