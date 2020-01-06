import os

class Config:
	SECRET_KEY='888b64bbc82791cc5be95bbc8d702b39'			#security purpose so that someone cant modify cookies
	SQLALCHEMY_DATABASE_URI='sqlite:///site.db'							#database connection
	#set the above 2 values as environment variables for security reeasons, like the last 2
	MAIL_SERVER='smtp.googlemail.com'
	MAIL_PORT=587
	MAIL_USE_TLS=True
	MAIL_USERNAME=os.environ.get('FLASK_EMAIL')
	MAIL_PASSWORD=os.environ.get('FLASK_PASS')
		