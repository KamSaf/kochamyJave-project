from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# creating SQLAlchemy database models
class Post(db.Model): # posts database
    userId = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(200))


class Users(db.Model): # users database
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(200)) # temporarily password is stored without using a hashing function


# getting data from JSONPlaceholder API
api_response = requests.get('https://jsonplaceholder.typicode.com/posts')
data = api_response.text
json_posts = json.loads(data)


@app.route('/') # Rendering all posts in database
def home_window():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/add", methods=["POST"])  # Adding post to the database
def add():
    new_post = Post(userId=request.form.get("user_id"), title=request.form.get("title"), body=request.form.get("body"))
    with app.app_context():
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for("home_window"))


@app.route("/delete/<int:id>") # Deleting post from database
def delete(id):
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("home_window"))


@app.route("/new_post") # url to the new post page
def new_post():
    return render_template('new_post.html')


@app.route('/about') # url to the about page
def about_app():
    return render_template('about.html')


@app.route('/login_page') # url to login page
def login_page():
   return render_template('login_page.html')


@app.route('/post_details/<int:id>') # url to details of a post
def post_details(id):
    #posts = Post.query.filter_by()
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
    return render_template('post_details.html', post=post)


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
    app.run() # when debug=True for some reason the for loop above adds posts twice
