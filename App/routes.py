from flask import render_template,url_for,flash,redirect , request , abort #
from App import app , db , bcrypt ,mail  #app,db , bcrypt is imported from teh __init__ file
#flash is used to give one time alerts , url_for is used to find methods/pages on it's own
#redirect to move to another page
from App.forms import (RegistrationForm,LoginForm,UpdateAccoutForm , 
                        PostForm ,RequestResetForm ,ResetPasswordForm) #importing  classes from our forms.py
from App.models import User, Post
from flask_login import login_user,current_user,logout_user ,login_required
import secrets
import os #for path functionality
from PIL import Image
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  
#for token and signatture management 

from flask_mail import Message




@app.route("/")
@app.route("/home") #home page route
def home():
    page = request.args.get('page',1,type=int)
    posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #order by helps to show the latest post first
    return render_template('home.html',posts=posts)

#About Page route
@app.route("/about")
def about():
    return render_template('about.html',title='About')

#Registration page route
@app.route("/register" , methods= ['GET','POST']) #givng list of allowed methods
def register():
    if current_user.is_authenticated:
        print("you are already logged in ")
        return redirect(url_for('home'))
    form = RegistrationForm() #creating an instance of registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data , password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your accout is created ! you will be able to log in','success')
        #print('Your accout is created ! you will be able to log in')
        return redirect(url_for('login'))
    return render_template('register.html', title ='Registration Page' , form = form) 
    # the last field is passing our registrationform on above line

#Log in page route
@app.route("/login", methods= ['GET','POST'])
def login():
    if current_user.is_authenticated:
        print("you are already logged in ")
        return redirect(url_for('home'))
    form = LoginForm() #creating an instance of login form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') # to get the next page from the querey passed before login required
            print("Logged in successfully")
            return redirect(next_page) if next_page else redirect(url_for('home'))
            #redirect to nect page if next_page exits else redirect to home
        else:
            print("Unsuccessful log in ")
            flash('Unsuccessful Log in Please check password','error')
    return render_template('login.html', title ='Log In Page' , form = form) 
    # the last field is passing our loginform on above line

#Log out
@app.route("/logout")
def logout():
    logout_user()
    print("You are logged out ")
    return redirect(url_for('home'))


# Saving Image 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



#Accoutn 
@app.route("/account", methods= ['GET','POST'])
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
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file =  image_file, form = form)

#new post
@app.route("/post/new" , methods= ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data ,author =  current_user)
        db.session.add(post)
        db.session.commit()
        flash("your post has been created" , 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form =form ,legend= 'New Post')


# getting to the post via post_id and displaying indiviuallly
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #give me the id or return 404 if id doesnot exixts
    return render_template('post.html' , title = post.title , post=post)

# Updating the post 
@app.route("/post/<int:post_id>/update",methods= ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 response is for http response for forbidden route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() #directly commiting as it is already in data bases
        flash("your post has been updated ", 'success')
        print("Post updated")
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form =form , legend= 'Update Post')
    
#Deelete post route
@app.route("/post/<int:post_id>/delete",methods= ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 response is for http response for forbidden rou
    db.session.delete(post)
    db.session.commit()
    flash('Your post hass been deleted', 'success')
    return redirect(url_for('home'))

#displaying only post by the clicked user
@app.route("/user/<string:username>") 
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user =  User.query.filter_by(username=username).first_or_404() #if found return else 404
    posts =  Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
        #\ is used to break the qurey in diff lines . filter_by(author=user) filter the post only by that user
    #order by helps to show the latest post first
    return render_template('user_posts.html',posts=posts ,user=user)

#sending the email request to reset email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request ', sender='noreply@demo.com',recipients=[user.email]) # this will be subject in first then sender
    #external = True is set ot that we get an absolute URL instead of relative url
    msg.body = f''' To reset your password , visit the following link 
        {url_for('reset_token',token=token,_external=True )}

        If you did not make this request then simply ignore this mail and no changes will be made!!

    '''
    mail.send(msg)


#reseting our request 
@app.route("/reset_password" , methods= ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #now once we have the user we need to send him a email with a token
        send_reset_email(user)
        print("an email has been sent with instruction ")
        flash('An email has been sent with instructions to reset your passsword','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password' , form = form)

#route to set the password by accepting token from user 
@app.route("/reset_password/<token>" , methods= ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None :
        print("That is an invalid or expired token")
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form =  ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your accout is created ! you will be able to log in','success')
        print('Your password is updated')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title ='Reset Password',form = form)


