from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
   userId = db.Column(db.Integer)
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100))
   body = db.Column(db.String(200))

posts =[
{
   'author': 'pablo escobar',
   'title': "first post",
   'content': 'i love italian cars',
   'post_date': '27/03/2023'
},
{
   'author': 'george clooney',
   'title': "second post",
   'content': 'i love fixing pablo\'s cars',
   'post_date': '28/03/2023'
}
]

@app.route('/')
def home_window():
   return render_template('home.html', posts = posts)

#dodać @app.route
def add():
   new_post = Post(userId = 1, id = 1, title = 'placeholder title', body = 'placeholder text')
   with app.app_context():
      db.session.add(new_post)
      db.session.commit()
   return redirect(url_for("home"))

@app.route('/about')
def about_app():
   return render_template('about.html')



if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug=True)
