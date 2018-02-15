from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])


class AddBookForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	author = StringField('author', validators=[DataRequired()])
