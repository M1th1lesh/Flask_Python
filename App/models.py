from App import db,login_manager , app  #from init 
from flask_login import UserMixin # to get methods like is_authenticated return True/Flase,is active,is getId, is_anonymous,
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
#for token and signature mgmt 

@login_manager.user_loader #this decorater is used so that extention knows this is the function to get a user by an ID
#@decorate
def load_user(user_id):
    return User.query.get(int(user_id))

#SQL model data bases
class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True )
    username = db.Column(db.String(20) , unique=True, nullable=False)
    email = db.Column(db.String(120) , unique=True, nullable=False)
    image_file = db.Column(db.String(20) , nullable=False, default='default.jpg' )
    password =  db.Column(db.String(60) , nullable=False )
    posts = db.relationship('Post',backref= 'author',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id }).decode('utf-8') #returing the token with payload as current user id

#verifies of the token is valid and gets the user details from the token
#setting it as static method so that python doesnot expect self as we are not passing any current varaible into it
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token )['user_id'] #user_id comes from the payload from token
        except:
            return None 
        return User.query.get(user_id)

    def __repr__(self) : #tells how our text is going to print c
        return f"User( '{self.username}', '{ self.email}', '{ self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True )
    title = db.Column(db.String(100),  nullable=False)
    date_posted = db.Column( db.DateTime , nullable=False , default= datetime.utcnow )
    content = db.Column(db.Text , nullable=False)
    user_id =  db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False )

    def __repr__(self):
        return f"Post (' {self.title}' , '{ self.date_posted}') "
