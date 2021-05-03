#pending setting up of environment variables
import os

class Config:
    
    #set secret key for application so that it can protect your application from cookie modification , cross site request forgery
    #generate key using python in terminal
    # import secrets
    #secrets.token_hex(number of bytes)
    #give random key to secret key 
    SECRET_KEY = '2e898bf09a9b59247b89ea7ce1ae45cd'
    #setting up data base 
    SQLALCHEMY_DATABASE_URI='sqlite:///flask_app_site.db'
    
    MAIL_SERVER= 'smtp.googlemail.com'  #setting up our mail server as gmail server
    MAIL_PORT= 587 
    MAIL_USE_TLS= True  
    #pending setting up of environment varaibles  os.environ.get('USER_EMAIL') and 'USER_PASS'
    MAIL_USERNAME = "dbitbatch2017@gmail.com"
    MAIL_PASSWORD = "8446830125"

        