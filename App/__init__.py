from flask import Flask
from flask_sqlalchemy import SQLAlchemy   #for database things
from flask_bcrypt import Bcrypt #to hash passwords
from flask_login import LoginManager # to manager logins and login session management
from flask_mail import Mail
import os 
from App.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #db is object of SQlAlchemy 
bcrypt = Bcrypt(app) # bcrpyt object of Bcrypt
login_manager = LoginManager(app) # login_manager is obj
login_manager.login_view = 'users.login' #passing fucntion name of log in so that it redirects if user is not 
#logged in and tries to go a page where login_required is added
login_manager.login_message_category = 'info'

#setting up constants for mailing server 

mail = Mail(app)

# from App import routes
from App.users.routes import users  #this users is the instance of the blueprint class
from App.posts.routes import posts #this posts is the instance of the blueprint class
from App.main.routes import main #this main is the instance of the blueprint class

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)