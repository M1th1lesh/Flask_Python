from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField , SubmitField ,BooleanField
#to import string fields and passowrd fields in froom as fields will be strings , Submit fields to submit teh ddata
# boolen fileds for True false output

from wtforms.validators import DataRequired ,Length  ,EqualTo ,Email
# for data required in fill validation , length for length validation
#emial for email validation , Equalto for comparing strings


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

class LoginForm(FlaskForm):
    #variable = field('lables',valdations)
    #setting conditions/validators for user name
    email = StringField('Email',
                        validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired()])

    #remember me to keep logged in and save the data in form of cookie
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log in')
