from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField, TextAreaField			#form ki fields he
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError	#validates data entered
from first_flask.models import User

class Registration(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), Length(min=2, max=24)])
	email=StringField('Email', validators=[DataRequired(), Length(min=2, max=40), Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Sign-Up')

	def validate_username(self, username):
		user=User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError('Username already taken.Please choose a different username')

	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError('Email already taken.Please choose a different email')

class Login(FlaskForm):
	email=StringField('Email', validators=[DataRequired(), Length(min=2, max=40), Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	remember=BooleanField("Remember me")
	submit=SubmitField('Log-In')

class UpdateAccount(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), Length(min=2, max=24)])
	email=StringField('Email', validators=[DataRequired(), Length(min=2, max=40), Email()])
	picture=FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png', 'jpeg'])])	
	submit=SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()

			if user:
				raise ValidationError('Username already taken.Please choose a different username')

	def validate_email(self, email):
		if email.data != current_user.email:
			user=User.query.filter_by(email=email.data).first()

			if user:
				raise ValidationError('Email already taken.Please choose a different email')


class PostForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired()])
	content=TextAreaField('Content', validators=[DataRequired()])
	submit=SubmitField('Post')

class RequestResetForm(FlaskForm):
	email=StringField('Email', validators=[DataRequired(), Length(min=2, max=40), Email()])
	submit=SubmitField('Request Password Reset')
	
	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user is None:
				raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
	password=PasswordField('Password', validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Reset Password')
