import unittest
import flaskBlog



class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flaskBlog.app.test_client()

    def test_home_page(self):
        rv = self.app.get('/')
        self.assertIn(b'Home page', rv.data)

    def test_about_page(self):
        rv = self.app.get('/about')
        self.assertIn(b'About', rv.data)

    def test_new_post_page(self):
        rv = self.app.get('/new_post')
        self.assertIn(b'Opublikuj', rv.data)


if __name__ == '__main__':
    unittest.main()
