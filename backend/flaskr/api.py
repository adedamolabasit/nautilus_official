import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flaskr import app,db
from flaskr.models import Contact,Newsletter
EVENT_PER_PAGE=8

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response


def paginated(request,query):

    page=request.args.get('page',1,type=int)
    pg=page -1
    start=pg *EVENT_PER_PAGE
    end=start * EVENT_PER_PAGE
    queries=query[start:end]
    outcome=[out.format() for out in queries]
    return outcome



@app.route('/contacts',methods=['GET'])
def contact_get():
    try:
        contact=Contact.query.order_by(Contact.id).all()
        return jsonify({
            'success':True,
            'contact':paginated(request,contact),
            'number of ined up contact':len(paginated(request,contact))
        })
    except Exception as err:
        if '404' in str(err):
            abort(404)
        else:
            abort(422)


@app.route('/contacts',methods=['POST'])
def contact_create():

    
        body=request.get_json()

        name=body.get('name',None)
        email=body.get('email',None)
        subject=body.get('subject',None)
        message=body.get('message',None)
        contact=Contact(name=name,email=email,subject=subject,message=message)
        contact.insert()

        con=[conn.id for conn in  Contact.query.order_by(Contact.id).all()]

        return jsonify({
            'success':True,
            
        })

 
@app.route('/newsletters',methods=['GET'])
def newsletter_get():
    try:
        newsletter=[news.email for news in Newsletter.query.order_by(Newsletter.id).all() ]
        return jsonify({
            'success':True,
            'email':newsletter,
            'subscribers mail':len(newsletter)
        })
    except Exception as err:
        if '404' in str(err):
            abort(404)
        else:
            abort(422)


@app.route('/newsletters',methods=['POST'])
def newsletter_create(): 
        body=request.get_json()
        email=body.get('email',None)
        newsemail=Newsletter.query.filter_by(email=email).first()
        if newsemail:
            abort(411)
        
        newsletter=Newsletter(email=email)
        db.session.add(newsletter)
        db.session.commit()
        
        return jsonify({
            'success':True,
            
        })

 





# error handler

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
@app.errorhandler(411)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 411,
        "message": "you are  already a subscriber"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "message": "unprocessable"
        }),422

@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500
