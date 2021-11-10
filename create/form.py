from flask.templating import render_template_string

from flask_wtf import FlaskForm

from wtforms.fields.core import BooleanField, IntegerField
from wtforms import StringField, SubmitField,BooleanField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import length,DataRequired,Email,EqualTo,ValidationError,InputRequired
from create.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
     username=StringField('Username',validators=[DataRequired(),length(min=4,max=21)],render_kw={'placeholder':'username'})
   
     email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})
   
     password=PasswordField('Password',validators=[DataRequired()],render_kw={'placeholder':'password'})
     
     comfirm_password=PasswordField('Comfirlm password',validators=[DataRequired(),EqualTo('password')],render_kw={'placeholder':'comfirm password'})
     newsletter =BooleanField('newsletter')
    

     submit=SubmitField('Register')
     
     def validate_username(self,username):
            existing_username=User.query.filter_by(username=username.data).first()
            if existing_username:
                raise ValidationError("user alrady exits please use another username")
     
     def validate_email(self,email):
            existing_email=User.query.filter_by(email=email.data).first()
            if existing_email:
                raise ValidationError("The email is taken")
         


class LoginForm(FlaskForm):
    
     email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})
     password=PasswordField('Password',validators=[DataRequired()],render_kw={'placeholder':'password'})
    
     remeber =BooleanField('Remember')
     submit=SubmitField('Login')
     




class UpdateAccountForm(FlaskForm):
     username=StringField('Username',validators=[DataRequired(),length(min=4,max=21)],render_kw={'placeholder':'username'})
   
     email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})
     picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
     submit=SubmitField('Update')
     
     def validate_username(self,username):
         if username.data != current_user.username:
            existing_username=User.query.filter_by(username=username.data).first()
            if existing_username:
                raise ValidationError("user alrady exits please use another username")
     
     def validate_email(self,email):
         if email.data != current_user.email:
            existing_email=User.query.filter_by(email=email.data).first()
            if existing_email:
                raise ValidationError("The email is taken")
         
class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Post')