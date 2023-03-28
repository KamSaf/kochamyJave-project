from flask import Flask, render_template
app = Flask(__name__)

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

@app.route('/about')
def about_app():
   return render_template('about.html')

if __name__ == '__main__':
   app.run(debug=True)