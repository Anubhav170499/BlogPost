from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from first_flask import db, login_manager
from flask import current_app
from flask_login import UserMixin			#helps in logging in user

#from first_flask import db				cant do this -> circular import
#option 2-> from __main__ import db 	but then, db ka error aayega and also database process karne me bhi error aayega
#solution-> create the whole mess into a package

@login_manager.user_loader										#this whole thing will help us to login user and manage session for them
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):												#Model classes bana rahe he for db
	id= db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(24), nullable=False, unique=True)	
	email=db.Column(db.String(120), nullable=False, unique=True)
	password=db.Column(db.String(60),nullable=False)								#string size is 60 bcz ye hash me convert hogi aage
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')		#same image bhi hash hogi

	posts=db.relationship('Post', backref='author', lazy=True)						#its a relationship not a column, no idea about lazy=True

	def get_reset_token(self, expires_sec=1800):						#it generates and return a token that have an expiry of 30 minutes 
		s=Serializer(current_app.config['SECRET_KEY'], expires_sec)				#initiate an object s to create a token with the secret key and expires seconds
		return s.dumps({'user_id':self.id}).decode('utf-8')			#dumps is the method that creates the token with payload of user_id, alos it returns a byte stream therefore we decode it in utf-8

	@staticmethod						#bcoz it isn't using self and we have manually tell python that its a static method
	def verify_reset_token(token):
		s=Serializer(current_app.config['SECRET_KEY'])	#no need to pass expirey time
		try:
			user_id=s.loads(token)['user_id']	#this may throw exception like time expired,etc.
			#loads is the method that loads the token into its corresponding value, here ['user_id'] shows that we specificaally want user_id
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	content=db.Column(db.Text, nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)			#utcnow ke aage () nahi lagaye, here the whole func. is passed as argument

	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)				
	#'user.id' here is a table and not a class but, in above class relationship,'Post' is referenced as a class

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
