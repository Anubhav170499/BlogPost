from flask import render_template,url_for,flash,redirect,request,Blueprint				#url_for used to locate our files
from flask_login import login_user, current_user, logout_user, login_required
from first_flask import db, bcrypt
from first_flask.models import User, Post
from first_flask.users.forms import (Registration,Login, UpdateAccount,
								RequestResetForm, ResetPasswordForm)
from first_flask.users.utils import set_profile_pic, send_reset_email


users=Blueprint('users', __name__)


#earlier all the routes were @app.route, but after blueprinting these are set to @users.route



@users.route("/register",methods=['GET','POST'])		#methods accepted from the form of html
def register():
	if current_user.is_authenticated:				#don't put () after is_authenticated, its an object not method
		return redirect(url_for('main.home'))

	form=Registration()

	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash(f'Account created Successfully!, Login to continue', 'success')			#2nd argument-> bootstrap class
		return redirect(url_for('users.login'))
	# else:
	# return("Form not validated")

	return render_template("register.html",title="Register Yourself", form=form)

@users.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form=Login()

	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')										
			#ex: if you click on a link and you are redirected to a website, 
			#but you are not loggind in there, so first you have to login then continue
			return redirect(next_page) if next_page else redirect(url_for('main.home')) 
			#ternary operator jesa
		else:
			flash('Loggin Unsuccessfull, please check your email and password','danger')

	return render_template("login.html",title="Login", form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form=UpdateAccount()
	if form.validate_on_submit():
		if form.picture.data:			#to set profile picture
			picture_file=set_profile_pic(form.picture.data)
			current_user.image_file=picture_file		#this sets the pic as new DP

		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))

	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email

	image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):								#this is to get all the posts created by a particular user, triggered when you click on the 'username' hyperlink
	page=request.args.get('page', 1, type=int)		
	user=User.query.filter_by(username=username).first_or_404()			#get the username, first username from query or 404 error	
	posts=Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)
		#above 3 lines are actually a single code of line, its a query broken up by using '\' bcoz query can be too long 
	return render_template("user_posts.html", posts=posts,user=user)



@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form=RequestResetForm()

	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent to your mail id with instructions to reset password.', 'info')
		return redirect(url_for('users.login'))

	return render_template('reset_request.html', form=form, title='Reset Password')

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user=User.verify_reset_token(token)

	if user is None:
		flash('This is an invalid or expired request', 'warning')
		return redirect(url_for('users.reset_request'))

	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_password
		db.session.commit()
		flash(f'Your password has been updated! Login to continue', 'success')			#2nd argument-> bootstrap class
		return redirect(url_for('users.login'))
	return render_template('reset_password.html',form=form, title='Reset Password')
