#users_routes.py
# contains 
# >register 
# >login
# >logout
# >account
# >user_posts
# >reset_request
# >reset_token

from flask import render_template,url_for,flash,redirect,request, Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from App import db,bcrypt
from App.models import User,Post
from App.users.forms import (RegistrationForm , LoginForm , UpdateAccoutForm ,
                                RequestResetForm , ResetPasswordForm)
from App.users.utils import save_picture,send_reset_email

users = Blueprint('users', __name__)


#Registration page route
@users.route("/register" , methods= ['GET','POST']) #givng list of allowed methods
def register():
    if current_user.is_authenticated:
        print("you are already logged in ")
        return redirect(url_for('main.home'))
    form = RegistrationForm() #creating an instance of registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data , password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your accout is created ! you will be able to log in','success')
        #print('Your accout is created ! you will be able to log in')
        return redirect(url_for('users.login'))
    return render_template('register.html', title ='Registration Page' , form = form) 
    # the last field is passing our registrationform on above line

#Log in page route
@users.route("/login", methods= ['GET','POST'])
def login():
    if current_user.is_authenticated:
        print("you are already logged in ")
        return redirect(url_for('main.home'))
    form = LoginForm() #creating an instance of login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') # to get the next page from the querey passed before login required
            print("Logged in successfully")
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            #redirect to nect page if next_page exits else redirect to home
        else:
            print("Unsuccessful log in ")
            flash('Unsuccessful Log in Please check password','error')
    return render_template('login.html', title ='Log In Page' , form = form) 
    # the last field is passing our loginform on above line

#Log out
@users.route("/logout")
def logout():
    logout_user()
    print("You are logged out ")
    return redirect(url_for('main.home'))


#Accoutn 
@users.route("/account", methods= ['GET','POST'])
@login_required   #to keep a check for log in required
def account():
    form = UpdateAccoutForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data 
        current_user.email = form.email.data
        db.session.commit()
        print("Account updated")
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file =  image_file, form = form)

#displaying only post by the clicked user
@users.route("/user/<string:username>") 
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user =  User.query.filter_by(username=username).first_or_404() #if found return else 404
    posts =  Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        #\ is used to break the qurey in diff lines . filter_by(author=user) filter the post only by that user
    #order by helps to show the latest post first
    return render_template('user_posts.html',posts=posts ,user=user)


#reseting our request 
@users.route("/reset_password" , methods= ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #now once we have the user we need to send him a email with a token
        send_reset_email(user)
        print("an email has been sent with instruction ")
        flash('An email has been sent with instructions to reset your passsword','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password' , form = form)

#route to set the password by accepting token from user 
@users.route("/reset_password/<token>" , methods= ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None :
        print("That is an invalid or expired token")
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form =  ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your accout is created ! you will be able to log in','success')
        print('Your password is updated')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title ='Reset Password',form = form)


