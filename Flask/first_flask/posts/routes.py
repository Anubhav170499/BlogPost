from flask import render_template,url_for,flash,redirect,request,abort,Blueprint				#url_for used to locate our files
from flask_login import current_user, login_required
from first_flask import db
from first_flask.models import Post
from first_flask.posts.forms import PostForm


posts=Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data, content=form.content.data, author=current_user)	#Post class object created
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html',title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")		#'<>' lets you place the variable(its value) in url 
#also int specifies that we are expecting an integer
def post(post_id):
	post=Post.query.get_or_404(post_id)			#get_or_404 method which tells either the post exsist or 404 page not found
	return render_template('post.html', title=post.title, post=post)	 

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
		return redirect(url_for('posts.post', post_id=post.id))
		
	elif request.method=='GET':
		form.title.data=post.title
		form.content.data=post.content

	return render_template('create_post.html',title='Edit Post', form=form, legend='Edit Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)	
	if post.author!= current_user:
		abort(403)
	
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))