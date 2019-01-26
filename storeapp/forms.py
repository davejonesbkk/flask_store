from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class LoginForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired])

class SignUpForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password1 = PasswordField('Password1', validators=[DataRequired()])
	password2 = PasswordField('Password2', validators=[DataRequired()])
	

class AddBookForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	author = StringField('Author', validators=[DataRequired()])
	category = StringField('Category', validators=[DataRequired()])
	image = FileField('Image', validators=[FileRequired()])
	