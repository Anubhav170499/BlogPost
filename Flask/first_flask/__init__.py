from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from first_flask.config import Config


'''
EARLIER:

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'			#route info di he[same as url_for]
login_manager.login_message_category='info'		#bootstrap ki class he info
mail=Mail(app)
'''

db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'			#route info di he[same as url_for]
login_manager.login_message_category='info'		#bootstrap ki class he info
mail=Mail()

#above are all extensions, which are only declared and not initialised
#created outside the func but initialised with the app
#so that one extension object can be used for multiple apps


def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(Config)					#config.py se Config values set kari he
	#creations of 'app' above


	db.init_app(app)								#and here the above extensions are initialised, with the function call
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from first_flask.users.routes import users		
	from first_flask.posts.routes import posts		#all these 3 imports are actually instances of blueprint class 
	from first_flask.main.routes import main 		#eg: main=Blueprint('main', __name__)

	app.register_blueprint(users)
	app.register_blueprint(posts)					#registering blueprints of every module
	app.register_blueprint(main)
	#blueprints are also included and only extensions are outside

	return app 

'''
IMPORTANT:
after configuration-lec:11

we shifted our app config to config.py file and created the above 'create_app' method
but now we don't have the 'app' that we can directly import .AAAAHHHHHHH!!!!!!!!!!!!!!

flask gives us the solution and provides : current_app 

so now we have to change app to current_app in other files
AAAAAHHHHHHHHHHHH!!!!!!!!!!!!!


'''