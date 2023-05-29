from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # creating SQLAlchemy instance


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


class Comments(db.Model):  # comments database
    postId = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    body = db.Column(db.String(500))


def create_users_database(testing=''):  # users database
    with app.app_context():
        db.create_all()
        new_user = Users(login="Kamil", password="kamil")
        db.session.add(new_user)

        new_user = Users(login="Slawek", password="slawek")
        db.session.add(new_user)

        new_user = Users(login="Marcin", password="marcin")
        db.session.add(new_user)

        new_user = Users(login="Ola", password="ola")
        db.session.add(new_user)

        new_user = Users(login="Marek", password="marek")
        db.session.add(new_user)

        new_user = Users(login="Patryk", password="patryk")
        db.session.add(new_user)

        new_user = Users(login="Pawel", password="pawel")
        db.session.add(new_user)

        new_user = Users(login="Mateusz", password="mateusz")
        db.session.add(new_user)

        new_user = Users(login="Laura", password="laura")
        db.session.add(new_user)

        new_user = Users(login="Patrycja", password="patrycja")
        db.session.add(new_user)
        if testing == 'testing':
            db.session.rollback()
        else:
            db.session.commit()
    return True


def create_posts_database():
    with app.app_context():
        db.create_all()
        api_response = requests.get('https://jsonplaceholder.typicode.com/posts')
        data = api_response.text
        json_posts = json.loads(data)
        for post in json_posts:
            new_post = Post(userId=post['userId'], title=post['title'], body=post['body'])
            with app.app_context():
                db.session.add(new_post)
                db.session.commit()
        db.session.remove()
        return True


def create_comments_database():
    with app.app_context():
        db.create_all()
        api_response = requests.get('https://jsonplaceholder.typicode.com/comments')
        data = api_response.text
        json_comments = json.loads(data)
        for comment in json_comments:
            new_comment = Comments(postId = comment['postId'], name=comment['name'], email=comment['email'], body=comment['body'])
            with app.app_context():
                db.session.add(new_comment)
                db.session.commit()
    db.session.remove()
    return True


# with app.app_context():
#     users = Users.query.all()
#     for user in users:
#         print(user.login)
@app.route('/')  # Rendering all posts in database
def home_window():
    logged_user = request.cookies.get('username')
    posts = Post.query.order_by(Post.id.desc()).all()
    users = Users.query.all()
    if logged_user is None or logged_user == 'none':
        return render_template('home.html', posts=posts, users=users)
    else:
        return render_template('home.html', posts=posts, users=users, logged_user=logged_user)


@app.route("/add", methods=["POST"])  # Adding post to the database
def add():
    logged_user = request.cookies.get('username')
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
        posts = Post.query.filter(Post.title.contains(request.form.get("searched_string"))).order_by(Post.id.desc()).all()
        users = Users.query.all()
    if logged_user is None or logged_user == 'none':
        return render_template('home.html', posts=posts, users=users)
    else:
        return render_template('home.html', posts=posts, users=users, logged_user=logged_user)


# @app.route("/filtered", methods=["POST"])  # Filtering posts by author
# def filtered_post():
#     logged_user = request.cookies.get('username')
#     if request.form.get("filtered_string") == '':
#         return redirect(url_for("home_window"))
#     with app.app_context():
#         posts = Post.query.filter(Post.userId == (request.form.get("filtered_string"))).order_by(Post.id.desc()).all()
#         users = Users.query.all()
#     if logged_user is None or logged_user == 'none':
#         return render_template('home.html', posts=posts, users=users)
#     else:
#         return render_template('home.html', posts=posts, users=users, logged_user=logged_user)

@app.route("/filtered", methods=["POST"])  # Filter posts by number of characters in title
def filtered_post():
    logged_user = request.cookies.get('username')
    param1 = 0
    param2 = 0
    posts = Post.query.order_by(Post.id.desc()).all()
    users = Users.query.all()
    if request.form.get("upper_bound") != '' or request.form.get("lower_bound") != '':
        if request.form.get("upper_bound").isdigit():
            param1 = int(request.form.get("upper_bound"))
        if request.form.get("lower_bound").isdigit():
            param2 = int(request.form.get("lower_bound"))
        filtered_posts = []
        for post in posts:
            if param2 <= len(post.title) <= param1:
                filtered_posts.append(post)
        posts = filtered_posts
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
    logged_user = request.cookies.get('username')
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
        user = Users.query.filter_by(id=post.userId).first()
        comments = Comments.query.filter_by(postId=id).all()
    if logged_user is None or logged_user == 'none':
        return render_template('post_details.html', post=post, user=user, comments=comments)
    else:
        return render_template('post_details.html', post=post, user=user, logged_user=logged_user, comments=comments)


@app.route('/logout', methods=["POST"])
def log_out():
    with app.app_context():
        resp = make_response(redirect(url_for("home_window")))
        resp.set_cookie('username', 'none')
        return resp


@app.route("/new_comment/<int:post_id>")  # url to the new post page
def new_comment(post_id):
    return render_template('new_comment.html', post_id=post_id)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    with app.app_context():
        new_comment = Comments(email=request.form.get("email"), name=request.form.get("name"),
                        body=request.form.get("body"), postId=post_id)
        with app.app_context():
            db.session.add(new_comment)
            db.session.commit()
        return redirect(f'/post_details/{post_id}')


@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    with app.app_context():
        post_id = Comments.query.filter_by(id=comment_id).first().postId
        comment = Comments.query.filter_by(id=comment_id).first()
        db.session.delete(comment)
        db.session.commit()
    return redirect(f'/post_details/{post_id}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Post.query.first() is None:
            create_posts_database()
        if Users.query.first() is None:
            create_users_database()
        if Comments.query.first() is None:
            create_comments_database()
    app.run()
