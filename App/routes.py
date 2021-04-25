from flask import render_template,url_for,flash,redirect
from App import app #app is imported from teh __init__ file
#flash is used to give one time alerts , url_for is used to find methods/pages on it's own
#redirect to move to another page
from App.forms import RegistrationForm,LoginForm  #importing  classes from our forms.py
from App.models import User, Post

posts= [
    {
        'author': 'Robin Sharma ',
        'title':'The 5 AM Club',
        'content':'Own your Morning , Elevate your life',
        'date_posted':'19th april 2021'
    },
    {
        'author': 'JAy  Shetty ',
        'title':'Think like a monk',
        'content':'imporve your thinking',
        'date_posted':'20th april 2021'
    }
]


@app.route("/")
@app.route("/home") #home page route
def home():
    return render_template('home.html',posts=posts)

#About Page route
@app.route("/about")
def about():
    return render_template('about.html',title='About')

#Registration page route
@app.route("/register" , methods= ['GET','POST']) #givng list of allowed methods
def register():
    form = RegistrationForm() #creating an instance of registration form
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title ='Registration Page' , form = form) 
    # the last field is passing our registrationform on above line

#Log in page route
@app.route("/login", methods= ['GET','POST'])
def login():
    form = LoginForm() #creating an instance of login form
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in ','message')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful Log in Please check password','error')
    return render_template('login.html', title ='Log In Page' , form = form) 
    # the last field is passing our loginform on above line

