import unittest
from unittest.mock import patch, MagicMock
from flask_blog import app, db, Comments, create_comments_database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class CreatePostsDatabaseTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            app.testing = True
            db.create_all()

    def tearDown(self):
        with app.app_context():
            comment = Comments.query.filter_by(name='test name').first()
            db.session.delete(comment)
            db.session.commit()
            db.session.remove()

    @patch('flask_blog.requests.get')
    def test_create_posts_database(self, mock_get):
        with app.app_context():
            # Prepare mock response
            mock_response = MagicMock()
            mock_response.text = '[{"postId": 1,"name": "test name", "email": "email@gmail.com", "body": "Test Body"}]'
            mock_get.return_value = mock_response

            # Call the method being tested
            result = create_comments_database()

            # Assert that the method returns True
            self.assertTrue(result)

            # Assert that the Post was added to the database correctly
            comment = Comments.query.filter_by(name='test name').first()
            self.assertIsNotNone(comment)
            self.assertEqual(comment.postId, 1)
            self.assertEqual(comment.name, 'test name')
            self.assertEqual(comment.email, 'email@gmail.com')
            self.assertEqual(comment.body, "Test Body")


if __name__ == '__main__':
    unittest.main()
