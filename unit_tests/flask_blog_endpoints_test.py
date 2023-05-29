import flask_testing
from flask_blog import app, db, Post, Users


class TestPages(flask_testing.TestCase):
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
        user = Users.query.filter_by(login='testuser').first()
        db.session.delete(user)
        post = Post.query.filter_by(title='test post').first()
        db.session.delete(post)
        db.session.commit()
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
            response = self.client.post('/filtered', data={'lower_bound': '3', 'upper_bound': '13'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_filtered_empty_page(self):
        with self.client:
            response = self.client.post('/filtered', data={'lower_bound': '', 'upper_bound': ''}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_searched_page(self):
        with self.client:
            response = self.client.post('/search', data={'searched_string': 'est'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_post_details_page(self):
        with self.client:
            response = self.client.get('/post_details/1')
            self.assert_template_used('post_details.html')

    def test_get_logut_endpoint(self):
        with self.client:
            response = self.client.post('/logout', follow_redirects=True)
            self.assert_template_used('home.html')