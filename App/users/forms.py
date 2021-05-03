#user_forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from App.models import User

# to create registration forms in flask
class RegistrationForm(FlaskForm):
    #variable = field('lables',valdations)
    #form fields
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)] )
    #setting conditions/validators for user name
    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    #these functions are created so that we can throw error before commiting to database .These will validate the fields for errors 
    #of duplicated entries of user_name or email
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first() 
        if user : 
            raise ValidationError('This username is taken . Please user different one')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first() 
        if user : 
            raise ValidationError('This email is taken . Please user different one')

class LoginForm(FlaskForm):
    #variable = field('lables',valdations)
    #setting conditions/validators for user name
    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired()])

    #remember me to keep logged in and save the data in form of cookie
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log in')

# to create update forms forms in flask
class UpdateAccoutForm(FlaskForm):
    #variable = field('lables',valdations)
    #form fields
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)] )
    #setting conditions/validators for user name
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    picture = FileField('Update Profile picture' ,validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    #these functions are created so that we can throw error before commiting to database .These will validate the fields for errors 
    #of duplicated entries of user_name or email
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() 
            if user : 
                raise ValidationError('This username is taken . Please user different one')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() 
            if user : 
                raise ValidationError('This email is taken . Please user different one')

#go to reset password page
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    submit =  SubmitField('Request Password Reset')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first() 
        if user is None : 
            raise ValidationError('There is no account with this email . You must first register')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit =  SubmitField('Reset Password')

