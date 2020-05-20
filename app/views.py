from app import app, db, login_maneger 
from datetime import date
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import loginform
from app.model import posts,likes,users,Followers
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename 
from werkzeug.security import generate_password_hash
from app.forms import registerform
import psycopg2 
import random 
import os   
import json 
from werkzeug.utils import secure_filename 
from flask_login import LoginManager

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, 'some-secret')

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages



@app.route('/api/users/register',methods=['POST']) 
def register(): 
    form=registerform() 
    if request.method == 'POST' : 
        username=request.form['username']
        password=(request.form['password']) 
        password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        location=request.form['location']
        biography=request.form['biography']
        profile_picture=form.profile_picture.data 
        filename=secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        join_on=date.today()
        newuser=users(username,password,firstname,lastname,email,location,biography,filename,join_on)
        db.session.add(newuser)
        db.session.commit() 
        return jsonify({"message": "New user added."}) 
    
    
    errors=form_errors(form) 
    return jsonify({"errors":errors})


@app.route('/api/auth/login',methods=['POST'])
def login():
    form=loginform 
    if request.method=='POST' :
        username=request.form['username']
        password=request.form['password']  
        
        user=users.query.filter_by(username=username).first() 
        
        if user != None and check_password_hash(user.password, password):
            login_user(user)
            print(current_user.id)
            return jsonify({"message":"You have successfully logged in!"})
        return jsonify({"message":"Invalid login information, password and/or username."})  
    
    errors=form_errors(form) 
    return jsonify({"errors":errors})

@app.route('/api/auth/logout')
@login_required 
def logout():
    logout_user()
    return jsonify({'message':"Logged out Successfully. Photogram!"}) 
    

@app.route("/api/current_user")
@login_required
def get_id():
    photos=[]
    id=current_user.id
    username=current_user.username
    location=current_user.location 
    biography=current_user.biography 
    post= posts.query.filter_by(user_id=id)
    print(post) 
    for x in post:
        pic={"pic":x.photo}
        photos.append(pic)
    print(photos)
    return jsonify({"id":id,"username":username,"location":location,"biography":biography,"firstname":current_user.firstname,"lastname":current_user.lastname,"profile_picture":current_user.profile_picture,"join_on":current_user.joined_on,"photos":photos})


@app.route("/api/userinfo/<user_id>")
@login_required 
def get_allpost(user_id): 
    info= users.query.filter_by(id=user_id) 

    for x in info:
         username=x.username
         firstname=x.firstname
         lastname=x.lastname
         location=x.location
         biography=x.biography 
         profile_picture=x.profile_picture 
         joined_on=x.joined_on
    return jsonify({"name":username,"firstname":firstname,"lastname":lastname,"location":location,"biography":biography,"profile_picture":profile_picture,"joined_on":joined_on})
    



@app.route('/api/users/user_id/posts',methods=['POST'])
@login_required 
def newpost():
    user_id=current_user.id
    form=newpost 
    if request.method=='POST': #and form.validate_on_submit():
        
        caption=request.form['caption']
        photo=request.files['photo']
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['PHOTOS'],filename))
        created_on=date.today() 
        post=posts(user_id,filename,caption,created_on)
        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Post successfully made."}) 
    
    errors=form_errors(form) 
    return jsonify({"errors":errors})
    
@login_maneger.user_loader 
def load_user(user_id):
    return users.query.get(user_id)  

@app.route('/api/users/<id>/posts')
@login_required 
def usersposts(id):
    allposts=[]
    user_posts = posts.query.filter_by(user_id=id)
    print(user_posts)
    for x in user_posts :
        dic={"pic":x.photo}
        allposts.append(dic)
    return jsonify({"posts":allposts})

@app.route('/api/post')    
@login_required 
def allposts():
    posts_=[]
    totalpost=db.session.query(posts).all()
    
    print(totalpost)
    for x in totalpost :
        total=[]
        totallikes=likes.query.filter_by(post_id=x.id)
        #print(totallikes) 
        for t in totallikes:
            total.append(t.post_id)
        alllikes=len(total)
        name = users.query.get(x.user_id).username
        pp = users.query.get(x.user_id).profile_picture
        dic={"user_id":x.user_id,"id":x.id,"caption":x.caption,"photo":x.photo,"created_on":x.created_on,"likes":alllikes,"name":name, "pp":pp}
        posts_.append(dic)
        #print(dic)
    return jsonify({"posts":posts_}) 


@app.route('/api/posts/<post_id>/like',methods=['POST']) 
@login_required 
def like(post_id): 
    user_id=current_user.id 
    newlike=likes(user_id,post_id) 
    db.session.add(newlike)
    db.session.commit() 
    totallikes= likes.query.filter_by(post_id=post_id) 
    num=[]
    print(totallikes) 
    for x in totallikes:
        num.append(x.user_id)
    num2=len(num)
    print(num2)
    return jsonify({"message":"Post liked.","likes":num2}) 

@app.route("/api/users/<user_id>/follow",methods=['POST'])
@login_required 
def follow(user_id): 
    follower_id=current_user.id 
    newfollow=Followers(user_id,follower_id) 
    db.session.add(newfollow)
    db.session.commit() 
    follow= Followers.query.filter_by(user_id=user_id) 
    num=[]
    print(follow) 
    for x in follow:
        num.append(x.user_id)
    num2=len(num)
    print(num2)
    return jsonify({"message":"You are now following.","followers":num2}) 