import flask_testing
from flask_blog import app, db


class TestPages(flask_testing.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_get_home_page(self):
        with self.client:
            response = self.client.get('/')
            self.assert_template_used('home.html')

    def test_get_about_page(self):
        with self.client:
            response = self.client.get('/about')
            self.assert_template_used('about.html')

    def test_get_new_post_page(self):
        with self.client:
            response = self.client.get('/new_post')
            self.assert_template_used('new_post.html')

    def test_get_login_page(self):
        with self.client:
            response = self.client.get('/login_page')
            self.assert_template_used('login_page.html')

    def test_get_filtered_page(self):
        with self.client:
            response = self.client.post('/filtered', data={'filtered_string': 'est'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_filtered_empty_page(self):
        with self.client:
            response = self.client.post('/filtered', data={'filtered_string': ''}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_searched_page(self):
        with self.client:
            response = self.client.post('/search', data={'searched_string': 'est'}, follow_redirects=True)
            self.assert_template_used('home.html')