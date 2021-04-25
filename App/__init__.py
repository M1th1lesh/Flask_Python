from flask import Flask
from flask_sqlalchemy import SQLAlchemy   #for database things

app = Flask(__name__)

#set secret key for application so that it can protect your application from cookie modification , cross site request forgery
#generate key using python in terminal
# import secrets
#secrets.token_hex(number of bytes)

#give random key to secret key 
app.config['SECRET_KEY'] = '2e898bf09a9b59247b89ea7ce1ae45cd'


#setting up data base 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flask_app_site.db'
db = SQLAlchemy(app)

from App import routes
