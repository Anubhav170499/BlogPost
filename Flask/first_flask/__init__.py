import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY']='888b64bbc82791cc5be95bbc8d702b39'			#security purpose so that someone cant modify cookies
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'							#database connection
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'			#route info di he[same as url_for]
login_manager.login_message_category='info'		#bootstrap ki class he info
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('FLASK_EMAIL')
app.config['MAIL_PASSWORD']=os.environ.get('FLASK_PASS')
mail=Mail(app)

from first_flask import routes