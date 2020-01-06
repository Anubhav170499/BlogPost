import secrets
import os
from PIL import Image 			#Pillow package(pip installed) used to scale and resize images
from flask import url_for, current_app				#url_for used to locate our files
from flask_mail import Message
from first_flask import mail



def set_profile_pic(form_pic):
	random_hex=secrets.token_hex(8)				#a random name to be generated
	_,file_ext=os.path.splitext(form_pic.filename)		
	#here '_' is just an unused varialbe,in place of file_name to be taken out of the pic submitted by user
	pic_file_name=random_hex + file_ext	
	pic_path=os.path.join(current_app.root_path, 'static/profile_pics', pic_file_name)
	
	output_size=(125,125)			#resized to 125X125 pixels
	i=Image.open(form_pic)			#open form_pic
	i.thumbnail(output_size)		

	i.save(pic_path) 	#saves the new umage in our database ,i.e, the profile_pics folder
	#PS: it doesn't set it as the new profile pic
	return pic_file_name

def send_reset_email(user):	#the method that send email to the given id
	token=user.get_reset_token()
	msg=Message('Password Reset Request', sender=os.environ.get('FLASK_EMAIL'), recipients=[user.email])
	
	#below msg.(dot)body is written, dhyan de
	msg.body=f'''To reset your password kindly visit the following link:
{url_for('users.reset_password',token=token, _external=True)}

If you didn't make this request then simply ignore this email and no changes will be made. 
'''
	mail.send(msg)
#above '_external=True' => gives absolute url link instead of relative url
#also the ending ''' must be placed at the leftmost base line as providing a tab will also create tab space in the email
#also only single curly braces{} for url_for(), bcoz we don't use it with double {{}} like in Jinje in our template files
