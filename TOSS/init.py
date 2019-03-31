from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '572c558d83dc2f9750e4366d9e245aae'
#dummy data 

posts = [
    {
        'author': 'Vinny Karanja',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': '04/20/2018'
    },
    {
        'author': 'Linet Karanja',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': '03/20/2018'
    }
]
#create route 

#make the route work with two or more names 
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

#add new route 
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    form = RegistrationForm()
    return return_template('register.html', title='')