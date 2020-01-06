from flask import Blueprint, request, render_template
from first_flask.models import Post

main=Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	#return "Hellooooooooooooo, World!"			//could have returned multiple lines of html code but better use separate file
	#posts=Post.query.all()
	
	page=request.args.get('page', 1, type=int)			#returns current page, default vale, type check constraint->int
	posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
	return render_template("Home.html", posts=posts)

@main.route("/about")
def about():
	return render_template("about.html",title="Flask ka About page")

