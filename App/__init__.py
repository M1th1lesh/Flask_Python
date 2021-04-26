from flask import Flask
from flask_sqlalchemy import SQLAlchemy   #for database things
from flask_bcrypt import Bcrypt #to hash passwords
from flask_login import LoginManager # to manager logins and login session management

app = Flask(__name__)

#set secret key for application so that it can protect your application from cookie modification , cross site request forgery
#generate key using python in terminal
# import secrets
#secrets.token_hex(number of bytes)
#give random key to secret key 
app.config['SECRET_KEY'] = '2e898bf09a9b59247b89ea7ce1ae45cd'


#setting up data base 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flask_app_site.db'
db = SQLAlchemy(app) #db is object of SQlAlchemy 
bcrypt = Bcrypt(app) # bcrpyt object of Bcrypt
login_manager = LoginManager(app) # login_manager is obj
login_manager.login_view = 'login' #passing fucntion name of log in so that it redirects if user is not 
#logged in and tries to go a page where login_required is added
login_manager.login_message_category = 'info'

from App import routes
