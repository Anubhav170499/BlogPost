import secrets
import os
from PIL import Image 			#Pillow package(pip installed) used to scale and resize images
from flask import render_template,url_for,flash,redirect,request,abort				#url_for used to locate our files
from first_flask.models import User, Post
from first_flask import app, db, bcrypt, mail
from first_flask.forms import (Registration,Login, UpdateAccount, PostForm,
								RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


''' this was used earlier but now we can get these from users
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
'''


@app.route("/")
@app.route("/home")
def home():
	#return "Hellooooooooooooo, World!"			//could have returned multiple lines of html code but better use separate file
	#posts=Post.query.all()
	
	page=request.args.get('page', 1, type=int)			#returns current page, default vale, type check constraint->int
	posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
	return render_template("Home.html", posts=posts)

@app.route("/about")
def about():
	return render_template("about.html",title="Flask ka About page")

@app.route("/register",methods=['GET','POST'])		#methods accepted from the form of html
def register():
	if current_user.is_authenticated:				#don't put () after is_authenticated, its an object not method
		return redirect(url_for('home'))

	form=Registration()

	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash(f'Account created Successfully!, Login to continue', 'success')			#2nd argument-> bootstrap class
		return redirect(url_for('login'))
	# else:
	# return("Form not validated")

	return render_template("register.html",title="Register Yourself", form=form)

@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form=Login()

	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')										
			#ex: if you click on a link and you are redirected to a website, 
			#but you are not loggind in there, so first you have to login then continue
			return redirect(next_page) if next_page else redirect(url_for('home')) 
			#ternary operator jesa
		else:
			flash('Loggin Unsuccessfull, please check your email and password','danger')

	return render_template("login.html",title="Login", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def set_profile_pic(form_pic):
	random_hex=secrets.token_hex(8)				#a random name to be generated
	_,file_ext=os.path.splitext(form_pic.filename)		
	#here '_' is just an unused varialbe,in place of file_name to be taken out of the pic submitted by user
	pic_file_name=random_hex + file_ext	
	pic_path=os.path.join(app.root_path, 'static/profile_pics', pic_file_name)
	
	output_size=(125,125)			#resized to 125X125 pixels
	i=Image.open(form_pic)			#open form_pic
	i.thumbnail(output_size)		

	i.save(pic_path) 	#saves the new umage in our database ,i.e, the profile_pics folder
	#PS: it doesn't set it as the new profile pic
	return pic_file_name

@app.route("/account", methods=['GET', 'POST'])
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
		return redirect(url_for('account'))

	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email

	image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data, content=form.content.data, author=current_user)	#Post class object created
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html',title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")		#'<>' lets you place the variable(its value) in url 
#also int specifies that we are expecting an integer
def post(post_id):
	post=Post.query.get_or_404(post_id)			#get_or_404 method which tells either the post exsist or 404 page not found
	return render_template('post.html', title=post.title, post=post)	 

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post=Post.query.get_or_404(post_id)	
	if post.author!= current_user:
		abort(403)		#403 is a HTTP response for a forbidden route
	form=PostForm()

	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
		
	elif request.method=='GET':
		form.title.data=post.title
		form.content.data=post.content

	return render_template('create_post.html',title='Edit Post', form=form, legend='Edit Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)	
	if post.author!= current_user:
		abort(403)
	
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):								#this is to get all the posts created by a particular user, triggered when you click on the 'username' hyperlink
	page=request.args.get('page', 1, type=int)		
	user=User.query.filter_by(username=username).first_or_404()			#get the username, first username from query or 404 error	
	posts=Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)
		#above 3 lines are actually a single code of line, its a query broken up by using '\' bcoz query can be too long 
	return render_template("user_posts.html", posts=posts,user=user)

def send_reset_email(user):	#the method that send email to the given id
	token=user.get_reset_token()
	msg=Message('Password Reset Request', sender='d2170499@gmail.com', recipients=[user.email])
	
	#below msg.(dot)body is written, dhyan de
	msg.body=f'''To reset your password kindly visit the following link:
{url_for('reset_password',token=token, _external=True)}

If you didn't make this request then simply ignore this email and no changes will be made. 
'''
	mail.send(msg)
#above '_external=True' => gives absolute url link instead of relative url
#also the ending ''' must be placed at the leftmost base line as providing a tab will also create tab space in the email
#also only single curly braces{} for url_for(), bcoz we don't use it with double {{}} like in Jinje in our template files

@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=RequestResetForm()

	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent to your mail id with instructions to reset password.', 'info')
		return redirect(url_for('login'))

	return render_template('reset_request.html', form=form, title='Reset Password')

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user=User.verify_reset_token(token)

	if user is None:
		flash('This is an invalid or expired request', 'warning')
		return redirect(url_for('reset_request'))

	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_password
		db.session.commit()
		flash(f'Your password has been updated! Login to continue', 'success')			#2nd argument-> bootstrap class
		return redirect(url_for('login'))
	return render_template('reset_password.html',form=form, title='Reset Password')
