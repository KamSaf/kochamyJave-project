from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home_window():
   return render_template('home.html')

@app.route('/about')
def about_app():
   return render_template('about.html')

if __name__ == '__main__':
   app.run(debug=True)