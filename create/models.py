from enum import unique
from werkzeug.exceptions import ClientDisconnected
from create import app,db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    __tablename__='user'
    __table_args__ = {'extend_existing': True}


    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(21))
    email=db.Column(db.String(112))
    image_file=db.Column(db.String(211),nullable=True,default='default.jpg')
    password=db.Column(db.String(211))
    newsletter=db.Column(db.Boolean(),default=False)
    is_admin=db.Column(db.Boolean(),default=False)
    is_staff=db.Column(db.Boolean(),default=False)
    post=db.relationship('Post',backref='author',lazy=True)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(112),nullable=True)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


class Event(db.Model):
    __tablename__='Event'
    __table_args__ = {'extend_existing': True}

    id =db.Column(db.Integer,primary_key=True)
    programe=db.Column(db.String(4577),nullable=False)
    information=db.Column(db.Text,nullable=True)
    uploaded=db.Column(db.DateTime())
    date=db.Column(db.DateTime())
    ends=db.Column(db.String(54))
    image=db.Column(db.Text,nullable=False)
    name=db.Column(db.Text,nullable=True)
    address=db.Column(db.Text,nullable=True)
    mimetype=db.Column(db.Text,nullable=False)
    uploaad=db.relationship('Images',cascade='all,delete' ,backref='event', lazy=True)


    


class Images(db.Model):
    __tablename__='image'
    __table_args__ = {'extend_existing': True}

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(333),nullable=False)
    discipline=db.Column(db.String(213),nullable=False)
    speaker=db.Column(db.String(163),nullable=False)
    img=db.Column(db.Text,nullable=False)
    names=db.Column(db.Text,nullable=False)
    mimetypes=db.Column(db.Text,nullable=False)
    event_id=db.Column(db.Integer, db.ForeignKey('Event.id'), nullable=True)   
    




class Contact(db.Model):
    __tablename__='contact'
    __table_args__ = {'extend_existing': True}

    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False)
    budget=db.Column(db.Integer)
    timeline=db.Column(db.Text)
    help=db.Column(db.Text)
    information=db.Column(db.Text)








class Worker(db.Model):
    __tablename__='worker'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(21),nullable=False)
    info=db.Column(db.Text,nullable=True)
    department=db.Column(db.String(21),nullable=False)
    instagram=db.Column(db.Text,nullable=False)
    link=db.Column(db.Text,nullable=False)
    image=db.Column(db.Text,nullable=True)
    names=db.Column(db.Text,nullable=False)
    mimetypes=db.Column(db.Text,nullable=False)


class Specialization(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    topic=db.Column(db.String(),nullable=False)
    descripition=db.Column(db.Text,nullable=False)
    img=db.Column(db.Text,nullable=False)
    names=db.Column(db.Text,nullable=False)
    mimetypes=db.Column(db.Text,nullable=False)














