from re import M
from flask import Flask,render_template,request,session,redirect,url_for,flash,abort,send_from_directory
from flaskr.models import Newsletter
from flaskr.models import Contact
from flaskr import app,db,mail
from werkzeug.utils import secure_filename
from flaskr.models import User,Contact
from flaskr.forms import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm
from datetime import datetime
from functools import wraps
import json
from authlib.integrations.flask_client import OAuth
from os import environ as env
from werkzeug.exceptions import HTTPException
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
import os
from flask_admin import Admin
import secrets
from PIL import Image
from flask_admin.contrib.sqla import ModelView
import smtplib
from flask_mail import Message

# files location and admin setup
bcrypt=Bcrypt(app)
app.config['SECRET_KEY']='d8827d6ff69e5fc8d4792ba4'

admin=Admin(app)
class Controller(ModelView):
    def is_accessible(self):
        if current_user:
            return current_user.is_authenticated
        # else:
        #     abort(422)
      

    def not_auth(self):
        return " you are not authorized to use the admin dashboard "


admin.add_view(Controller(User,db.session))
admin.add_view(Controller(Contact,db.session))
admin.add_view(Controller(Newsletter,db.session))

@app.route('/')
def index():
    return render_template('naut/index.html')

# login fuction
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email ).first()

        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,form.remeber.data)
                next_page=request.args.get('next')
                flash('User login successful')
                return redirect(url_for('index'))
            else:
                if form.errors != {}:
                    for err_msg in form.errors.values():
                        print(f'error:{err_msg}')
                flash("Login Unsuccessful.Please check email and password",'Failed')

    return render_template('naut/login.html',form=form)
# registration
@app.route('/register',methods=['GET','POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    form=RegistrationForm()
    if form.validate_on_submit():     
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username=form.username.data
        email=form.email.data
        if email and hashed_password:
             user=User(username=username,password=hashed_password,email=email)
             comfirm_email(user)

             db.session.add(user)
             db.session.commit()  

             return redirect(url_for('login'))
    

    return render_template('naut/signup.html',form=form)

def comfirm_email(user):
    token=user.get_verify_email_token()
    msg = Message('Comfirm Username',
    sender='noreply@demo.com',
    recipients=[user.email])
    msg.body=f'''comfirm your email:
    {url_for('reset_token',token=token,_external=True)}
    if  you did not make this request then simply ignore this email and no changes will be made
    '''
    mail.send(msg)



# logout
@app.route('/logout',methods=['GET','POST'])
def logout():   
    logout_user()
    return redirect(url_for('index'))

def send_reset_email(user):
    token=user.get_reset_token()
    msg = Message('Password Rest Request',
    sender='noreply@demo.com',
    recipients=[user.email])
    msg.body=f'''to reset your password ,visit the following link:
    {url_for('reset_token',token=token,_external=True)}
    if  you did not make this request then simply ignore this email and no changes will be made
    '''
    mail.send(msg)





@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RequestResetForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('naut/reset_request.html',title="reset password",form=form)
@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('this is an invalid token or expired token')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():     
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user.password=hashed_password
        db.session.commit()  
        flash('Your password has changed')
        return redirect(url_for('login'))
        
    return render_template('naut/reset_token.html',title='Reset password',form=form)
    


    















