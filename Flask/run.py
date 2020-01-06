########################## --> ye jo kuch bhi neeche likha gaya he wo copy ho chuka he inside the package
from first_flask import create_app

app=create_app()			#after lec:11 configuration

if __name__ == '__main__':				
  ##  app.run(host='0.0.0.0')		#ye network me public access ke liye he look for external server in flask
  app.run(debug=True)











'''
from flask import Flask,render_template,url_for,flash,redirect					#url_for used to locate our files
from flask_sqlalchemy import SQLAlchemy
from forms import Registration,Login
app=Flask(__name__)

app.config['SECRET_KEY']='888b64bbc82791cc5be95bbc8d702b39'			#security purpose so that someone cant modify cookies
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'							#database connection

db=SQLAlchemy(app)


from models import User, Post


dumy_posts=[														#consider it to be dummy data obtained from database calls
	{
		"author":"Anubhav Jain",
		"title":"Flask 1",
		"content":"the quick brown fox jumped over the lazy dog",
		"date_posted": "October 24, 2019"
	},
	{
		'author':"Anubhav Jain",
		"title":"Flask 2",
		"content":"the quick brown fox jumps over the lazy dog",
		"date_posted": "October 25, 2019"
	}
]

@app.route("/")
@app.route("/home")
def home():
	#return "Hellooooooooooooo, World!"			//could have returned multiple lines of html code but better use separate file
	return render_template("Home.html", posts=dumy_posts)

@app.route("/about")
def about():
	return render_template("about.html",title="Flask ka About page")

@app.route("/register",methods=['GET','POST'])		#methods accepted from the form of html
def register():
	form=Registration()
	
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}', 'success')			#2nd argument-> bootstrap class
		return redirect(url_for('home'))
	# else:
	# 	return("Form not validated")

	return render_template("register.html",title="Register Yourself", form=form)

@app.route("/login",methods=['GET','POST'])
def login():
	form=Login()
	if form.validate_on_submit():
		if form.email.data=='admin@blog.com' and form.password.data=='jhamru':
			flash(f'Logged In Successfully','success')
			return redirect(url_for('home'))
		else:
			flash('Loggin Unsuccessfull, please check username and password','danger')

	return render_template("login.html",title="Login", form=form)

########################## --> ye jo kuch bhi upar likha gaya he wo copy ho chuka he inside the package

if __name__ == '__main__':				
  ##  app.run(host='0.0.0.0')		#ye network me public access ke liye he look for external server in flask
  app.run(debug=True)

'''

