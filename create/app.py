from re import M
from flask import Flask,render_template,request,session,redirect,url_for,flash,abort,send_from_directory
from create import app,db
from werkzeug.utils import secure_filename
from create.models import Images,Event,Contact,User,Worker,Specialization,Post
from create.form import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
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

# files location and admin setup

UPLOAD_FOLDER='create/static/uploads/'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']= 16 * 1024 * 1024
bcrypt=Bcrypt(app)
app.config['SECRET_KEY']='d8827d6ff69e5fc8d4792ba4'

admin=Admin(app)
class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            abort(422)
      

    def not_auth(self):
        return " you are not authorized to use the admin dashboard "


admin.add_view(Controller(User,db.session))
admin.add_view(ModelView(Post,db.session))
admin.add_view(ModelView(Event,db.session))
admin.add_view(ModelView(Images,db.session))
admin.add_view(ModelView(Contact,db.session))
admin.add_view(ModelView(Worker,db.session))
admin.add_view(ModelView(Specialization,db.session))



ALLOWED_EXTENSIONS=set(['png','jpg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() is ALLOWED_EXTENSIONS

# end


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
                login_user(user)
                next_page=request.args.get('next')
                flash('User login successful')
                return redirect(url_for('index'))
            else:
                if form.errors != {}:
                    for err_msg in form.errors.values():
                        print(f'error:{err_msg}')
                flash("Login Unsuccessful.Please check email and password",'Failed')

    return render_template('nautilus/login.html',form=form)
# registration
@app.route('/register',methods=['GET','POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    form=RegistrationForm()
    if form.validate_on_submit():     
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username=form.username.data
        newsletter=form.newsletter.data
        print(username)
        email=form.email.data
        new_user=User(username=username,password=hashed_password,email=email)
        db.session.add(new_user)
        db.session.commit()  
        if form.errors != {} :
            for err_msg in form.errors.values():
                print(f'There was an error with creating a user:{err_msg}')

        flash(f'Account created for {form.username.data}','success')
    
        return redirect(url_for('index'))
    

    return render_template('nautilus/register.html',form=form)
    


# logout
@app.route('/logout',methods=['GET','POST'])
def logout():   
    logout_user()
    return redirect(url_for('index'))


# save and protect user image upload
def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# user account
@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        
        db.session.commit()
        flash('your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email   
    return render_template('nautilus/account.html',title='Account',image_file=current_user.image_file,form=form)

# home page
@app.route('/',methods=['GET','POST'])
def index():
    show={}
    events=Event.query.order_by(Event.id).first()
    show={
        'date':events.date,
        'programme':events.programe,
        'image':events.name
    }
    workers=Worker.query.all()
    specialization=Specialization.query.all()   
    return render_template('nautilus/index.html',worker=workers,event=show,specialization=specialization)

# contact page
@app.route('/contacts',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        full_name=request.form.get('Name',None)
        email=request.form.get('Email',None)
        if current_user.is_authenticated:
            full_name=current_user.username
            email=current_user.email
        timeline=request.form.get('Timeline',None)
        budget=request.form.get('Budget',None)
        help1=request.form.get('help1',None)
        help2=request.form.get('help2',None)
        help3=request.form.get('help3',None)
        help4=request.form.get('help4',None)
        information=request.form.get('Text-Area',None)
        if help1 or help2 or help3:
            helps=[help1,help2,help3]
        if help4:
            helps=[help1,help2,help3]   
        if request.method == 'POST':
            contact=Contact(full_name=full_name,email=email,timeline=timeline,budget=budget,help=helps,information=information)
            db.session.add(contact)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('nautilus/contact.html')

# event page
@app.route('/events',methods=['GET','POST'])
def event():
    event=Event.query.all()
    upcoming_events=[]
    pasts_events=[]
    for events in event:
        now=datetime.now()  
        upcoming_count=0
        past_count=0
        if events.date > now:
            upcoming_count += 1
            upcoming_events.append({
            'id':events.id,
            'programe':events.programe,
            'information':events.information,
            'address':events.address,
            'date':events.date,    
            'image':events.image
            })
        if events.date < now:
            past_count += 1
            pasts_events.append({
            'id':events.id,
            'programe':events.programe,
            'information':events.information,
            'address':events.address,
            'date':events.date,
            'image':events.image

            }) 

    return render_template('nautilus/events.html',upcoming_events=upcoming_events,past_events=pasts_events)


# more details on events
@app.route('/events/<int:event_id>',methods=['GET','POST'])
def event_detail(event_id):
    event=Event.query.get(event_id)
    now=datetime.now()
    if not event:
        abort(422)
    if event.date > now:
        resp='Upcoming Event'
    if event.date < now:
        resp="Past Event"
    pics = request.files.get('pic')
    if pics is not None:   

        name=request.form['name']
        discipline=request.form['discipline']
        speaker=request.form['speaker']
        names=secure_filename(pics.filename)
        pics.save(os.path.join(app.config['UPLOAD_FOLDER'],names)) 

        mimetype=pics.mimetype
        event_det=event.id
        img=pics.read()
        image=Images(name=name,discipline=discipline,speaker=speaker,names=names,mimetypes=mimetype,img=img,event_id=event_det)
        db.session.add(image)
        db.session.commit()
    data=db.session.query(Event).join(Images).filter(Images.event_id==event.id).first()  
    bucket={
        'information':data.information,
        'programme':data.programe,
        'image':data.image,
        'event':data.uploaad
    }
    return render_template('nautilus/event_details.html',event=event,responce=resp,data=bucket)




# team

@app.route('/team',methods=['GET','POST'])
def team():
    pic=request.files.get('pic',None)
    if pic is not None:
        name=request.form['name']
        department=request.form['department']
        info=request.form['info']
        instagram=request.form['instagram']
        link=request.form['link']
        filename=secure_filename(pic.filename)
        mimetype=pic.mimetype
        image=pic.read()
        worker=Worker(name=name,department=department,instagram=instagram,link=link,names=filename,mimetypes=mimetype,img=image,info=info)
        db.session.add(worker)
        db.session.commit()
        return 'success'
    return render_template('nautilus/workers.html')

# userpost
@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        author=current_user
        post=Post(title=title,content=content,author=author)
        db.session.add(post)
        db.session.commit()
        flash('posted')
        return redirect(url_for('account'))
    return render_template('nautilus/post.html',title='New post')
    






# admin page
@app.route('/specialization/admin',methods=['GET','POST'])
def create_soecialization():
    if request.method == "POST":
        image=request.files.get('image')
        if image:
            img=secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],img))
            topic=request.form['topic']
            description=request.form['description']
            mimetype=image.mimetype
            names=image.read()
            spec=Specialization(topic=topic,descripition=description,mimetypes=mimetype,names=names,img=img)
            db.session.add(spec)
            db.session.commit()
            return "siccess"
    return render_template('admin/specialization.html')
@app.route('/team/admin',methods=['GET','POST'])
def Team():
    if request.method == "POST":
        image=request.files.get('image')
        UPLOAD_FOLDER='create/static/team'
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

        if image:
            img=secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],img))
            name=request.form['name']
            info=request.form['info']
            department=request.form['department']
            instagram=request.form['instagram']
            link=request.form['link']
            mimetype=image.mimetype
            names=image.read()
            team=Worker(name=name,info=info,mimetypes=mimetype,names=names,img=img,department=department,instagram=instagram,link=link)
            db.session.add(team)
            db.session.commit()
            return "siccess"
    return render_template('admin/team.html')
@app.route('/event/admin',methods=['GET','POST'])
def create_event():
    if request.method == "POST":
        image=request.files.get('image')
        UPLOAD_FOLDER='create/static/uploads'
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

        if image:
            img=secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],img))
        programe=request.form['programe']
        information=request.form['information']
        date=request.form['date']
        end=request.form['ends']
        address=request.form['address']
        mimetype=image.mimetype
        names=image.read()
        event=Event(programe=programe,information=information,address=address,date=date,ends=end,mimetype=mimetype,name=names,image=img)
        db.session.add(event)
        db.session.commit()
        return "siccess"
    return render_template('admin/event.html')

# specialization details
@app.route('/spec/<spec_id>',methods=['GET'])
def spec_details(spec_id):
    spec=Specialization.query.get(spec_id)
    if not spec:
        abort(422)
    return render_template('nautilus/spec_details.html',spec=spec)



# about page
@app.route('/about')
def about():
    return render_template('nautilus/about.html')






