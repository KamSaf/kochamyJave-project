import flask_testing
from flask_blog import app, db, Users


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


# import unittest
# import flaskBlog
# from flaskBlog import check_login_data
#
# class MyTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = flaskBlog.app.test_client()
#
#     def test_get_home_page(self):
#         rv = self.app.get('/')
#         self.assertIn(b'Home page', rv.data)
#
#     def test_get_about_page(self):
#         rv = self.app.get('/about')
#         self.assertIn(b'About', rv.data)
#
#     def test_get_new_post_page(self):
#         rv = self.app.get('/new_post')
#         self.assertIn(b'Share', rv.data)
#
#     def test_get_login_page(self):
#         rv = self.app.get('/login_page')
#         self.assertIn(b'Login page', rv.data)
#
#     def test_invalid_login(self):
#         login = "invalid_login"
#         password = "kamil"
#         rv = self.app.get(check_login_data(login, password))
#         self.assertIn(b'Login page', rv.data)
#
# if __name__ == '__main__':
#     unittest.main()


