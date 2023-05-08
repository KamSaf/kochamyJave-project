import flask_testing
from flask_blog import app, db, Users

class TestLogin(flask_testing.TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        user = Users(login='testuser', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_valid_login(self):
        with self.client:
            response = self.client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_invalid_login(self):
        with self.client:
            response = self.client.post('/login', data={'username': 'nonexistentuser', 'password': 'wrongpassword'})
            self.assert_template_used('login_page.html')

    def test_empty_login(self):
        with self.client:
            response = self.client.post('/login', data={'username': '', 'password': 'password'})
            self.assert_template_used('login_page.html')

    def test_empty_password(self):
        with self.client:
            response = self.client.post('/login', data={'username': 'testuser', 'password': ''})
            self.assert_template_used('login_page.html')