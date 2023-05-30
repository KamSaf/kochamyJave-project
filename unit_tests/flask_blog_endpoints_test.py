import flask_testing
from flask_blog import app, db, Post, Users, Comments


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
        comment = Comments(postId=1, name='test comment', email='test@email.com', body='test comment content')
        db.session.add(comment)
        db.session.commit()

    def tearDown(self):
        user = Users.query.filter_by(login='testuser').first()
        db.session.delete(user)
        post = Post.query.filter_by(title='test post').first()
        db.session.delete(post)
        comment = Comments.query.filter_by(name='test comment').first()
        db.session.delete(comment)
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

    def test_filtered_loggedin(self):
        with self.client:
            self.client.set_cookie('/', 'username', 'testuser')
            response = self.client.post('/filtered', data={'lower_bound': '3', 'upper_bound': '13'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_searched_page(self):
        with self.client:
            response = self.client.post('/search', data={'searched_string': 'est'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_search_empty_string(self):
        with self.client:
            response = self.client.post('/search', data={'searched_string': ''}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_searched_loggedin(self):
        with self.client:
            self.client.set_cookie('/', 'username', 'testuser')
            response = self.client.post('/search', data={'searched_string': 'est'}, follow_redirects=True)
            self.assert_template_used('home.html')

    def test_get_post_details_page(self):
        with self.client:
            response = self.client.get('/post_details/' + str(Post.query.filter_by(title='test post').first().id))
            self.assert_template_used('post_details.html')

    def test_get_post_details_page_loggedin(self):
        with self.client:
            self.client.set_cookie('/', 'username', 'testuser')
            response = self.client.get('/post_details/' + str(Post.query.filter_by(title='test post').first().id))
            self.assert_template_used('post_details.html')

    def test_get_logut_endpoint(self):
        with self.client:
            response = self.client.post('/logout', follow_redirects=True)
            self.assert_template_used('home.html')

    def test_new_comment(self):
        with self.client:
            response = self.client.get('/new_comment/' + str(Post.query.filter_by(title='test post').first().id))
            self.assert_template_used('new_comment.html')
