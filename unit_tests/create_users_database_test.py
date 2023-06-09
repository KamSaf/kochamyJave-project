import flask_testing
from flask_blog import app, db, create_posts_database, create_users_database, create_comments_database


class TestDatabase(flask_testing.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_create_users_database(self):
        assert create_users_database('testing') is True
