# Flask_Python

***** do not push as email and password are there in file 

Trying to learn Flask

Completed : 
navbar completed \n
sign up page completed
log in completed
db tables created
part 5 : packages completed - creating a modular structure 
separating routes models and packages
unquie entries in register complete
authentication of log in complete
profile page completed with ability to updated new image and image resize
Create , Update and delete post completed
Pagination completed : 
pages divided with per page 5 .
once we click on author we get posts by that particular user 
posts ordered as latest post first
Email and password reset
Blueprint and configuration
Moved creation of app to a function

Working  : 




Pending errors : 

***** Flash message not showing up after form submission
***** Formatting of text and text sizes pending
IN SQLalchemy
Lazy ??


import os 

pip install Pillow ?  watch  video

app.config['MAIL_SERVER']= 'smtp.googlemail.com'  #setting up our mail server as gmail server
app.config['MAIL_PORT']= 587 
app.config['MAIL_USER_TLS']= True  

setting up of environment variable of password and emial
#pending setting up of environment varaibles  os.environ.get('USER_EMAIL') and 'USER_PASS'
app.config['MAIL_USERNAME'] = 'dbitbatch2017@gmail.com'
app,config['MAIL_PASSWORD'] = '8446830125'
SECRET_KEY = '2e898bf09a9b59247b89ea7ce1ae45cd'
SQLALCHEMY_DATABASE_URI='sqlite:///flask_app_site.db'


1. Post content moving out of the div
2. Do not share it with anyone else as this contents passwords
3. sender name not set to noreply@mydocs.com


Installments needed : 

1. pip3 install flask-wtf 
2. pip3 install email-validator
3. pip3 install flask-sqlalchemy
4. pip install flask-bcrypt
5. pip install flask-login
6. pip install Pillow
7. pip install flask-mail
