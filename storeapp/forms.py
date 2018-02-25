from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField

class LoginForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])

class SignUpForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password1 = StringField('Password', validators=[DataRequired()])
	password2 = StringField('Password', validators=[DataRequired()])
	recaptcha = RecaptchaField()



#class AddBookForm(FlaskForm):
	#title = StringField('Title', validators=[DataRequired()])
	#author = StringField('Author', validators=[DataRequired()])
	#category = StringField('Category', validators=[DataRequired()])
