from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField			#form ki fields he
from wtforms.validators import DataRequired							#validates data entered

class PostForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired()])
	content=TextAreaField('Content', validators=[DataRequired()])
	submit=SubmitField('Post')

  