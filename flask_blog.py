from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'test_database': 'sqlite:///test.db',
    'production_database': 'sqlite:///db.sqlite'
}
db = SQLAlchemy(app)


# creating SQLAlchemy database models
class Post(db.Model):  # posts database
    userId = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(200))


class Users(db.Model):  # users database
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200), unique=True)  # temporarily password is stored without using a hashing function


# with app.app_context():
#     print(Users.query.first().login)
def create_users_database():
    with app.app_context():
        db.create_all()
        if Users.query.first() is None:
            new_user = Users(login="Kamil", password="kamil")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Slawek", password="slawek")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Marcin", password="marcin")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Ola", password="ola")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Marek", password="marek")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Patryk", password="patryk")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Pawel", password="pawel")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="mateusz", password="mateusz")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Laura", password="laura")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            new_user = Users(login="Patrycja", password="patrycja")
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()


# getting data from JSONPlaceholder API
api_response = requests.get('https://jsonplaceholder.typicode.com/posts')
data = api_response.text
json_posts = json.loads(data)


@app.route('/')  # Rendering all posts in database
def home_window():
    if Users.query.first() is None:
        create_users_database()
    logged_user = request.cookies.get('username')
    posts = Post.query.all()
    users = Users.query.all()
    if logged_user is None or logged_user == 'none':
        return render_template('home.html', posts=posts, users=users)
    else:
        return render_template('home.html', posts=posts, users=users, logged_user=logged_user)

# @app.route('/')  # Rendering all posts in database
# def home_window():
#     return render_template('home.html')


@app.route("/add", methods=["POST"])  # Adding post to the database
def add():
    logged_user = request.cookies.get('username')
    print(logged_user)
    new_post = Post(userId=Users.query.filter_by(login=logged_user).first().id, title=request.form.get("title"), body=request.form.get("body"))
    with app.app_context():
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for("home_window"))


@app.route("/delete/<int:id>")  # Deleting post from database
def delete(id):
    logged_user = request.cookies.get('username')
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("home_window"))


@app.route("/new_post")  # url to the new post page
def new_post():
    return render_template('new_post.html')


@app.route("/search", methods=["POST"])  # Searching posts by substring in post title
def search_post():
    logged_user = request.cookies.get('username')
    if request.form.get("searched_string") == '':
        return redirect(url_for("home_window"))
    with app.app_context():
        posts = Post.query.filter(Post.title.contains(request.form.get("searched_string"))).all()
        users = Users.query.all()
    if logged_user is None or logged_user == 'none':
        return render_template('home.html', posts=posts, users=users)
    else:
        return render_template('home.html', posts=posts, users=users, logged_user=logged_user)


@app.route("/filtered", methods=["POST"])  # Filtering posts by author
def filtered_post():
    logged_user = request.cookies.get('username')
    if request.form.get("filtered_string") == '':
        return redirect(url_for("home_window"))
    with app.app_context():
        posts = Post.query.filter(Post.userId == (request.form.get("filtered_string"))).all()
        users = Users.query.all()
    if logged_user is None or logged_user == 'none':
        return render_template('home.html', posts=posts, users=users)
    else:
        return render_template('home.html', posts=posts, users=users, logged_user=logged_user)


@app.route('/about')  # url to the about page
def about_app():
    return render_template('about.html')


@app.route('/login_page')  # url to login page
def login_page():
    return render_template('login_page.html')


@app.route('/login', methods=["POST"])  # method checking if entered data is valid
def check_login_data():
    with app.app_context():
        entered_login = request.form.get("username")
        entered_password = request.form.get("password")
        if Users.query.filter_by(login=entered_login).first() is None or entered_login == '' or entered_password == '':
            return render_template('login_page.html')
        elif Users.query.filter_by(login=entered_login).first() is not None \
                and Users.query.filter_by(login=entered_login).first().password == entered_password:
            resp = make_response(redirect(url_for("home_window")))
            resp.set_cookie('username', entered_login)
            return resp
        else:
            return render_template('login_page.html')


@app.route('/post_details/<int:id>')  # url to details of a post
def post_details(id):
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
        user = Users.query.filter_by(id=post.userId).first()
    return render_template('post_details.html', post=post, user=user)

@app.route('/logout', methods=["POST"])
def log_out():
    with app.app_context():
        resp = make_response(redirect(url_for("home_window")))
        resp.set_cookie('username', 'none')
        return resp


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Post.query.first() is None:
            for post in json_posts:
                new_post = Post(userId=post['userId'], title=post['title'], body=post['body'])
                with app.app_context():
                    db.session.add(new_post)
                    db.session.commit()
                    posts_added = True
    app.run()  # when debug=True for some reason the for loop above adds posts twice
