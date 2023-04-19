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

# posts =[
# {
#    'author': 'pablo escobar',
#    'title': "first post",
#    'content': 'i love italian cars',
#    'post_date': '27/03/2023'
# },
# {
#    'author': 'george clooney',
#    'title': "second post",
#    'content': 'i love fixing pablo\'s cars',
#    'post_date': '28/03/2023'
# }
# ]

@app.route('/')
def home_window():
   posts = Post.query.all()
   return render_template('home.html', posts = posts)

@app.route("/add", methods=["POST"]) #Dodawanie postu do bazy
def add():
   new_post = Post(userId = request.form.get("user_id"), title = request.form.get("title"), body = request.form.get("body"))
   with app.app_context():
      db.session.add(new_post)
      db.session.commit()
   return redirect(url_for("home_window"))

@app.route("/delete/<int:id>")
def delete(id):
    #delete existing post
    with app.app_context():
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("home_window"))

@app.route("/new_post")
def new_post():
   return render_template('new_post.html')

@app.route('/about')
def about_app():
   return render_template('about.html')

@app.route('/login_page')
def login_page():
   return render_template('login_page.html')

@app.route('/post_details')
def post_details():
    posts = Post.query.filter_by()
    return render_template('post_details.html', posts=posts)



if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug=True)
