from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://eimnxofbvorepj:952d68e415cb3b7b99fa2daa4cf8f53baa21b487f1f3f9136591f11de3fdd857@ec2-54-197-234-117.compute-1.amazonaws.com:5432/d600bhkqukpv3e"   #this is what will give acess to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True   #added just to suppress a warning 
app.config['UPLOAD_FOLDER']="./app/static/uploads"   #profile pictures are stored here
app.config['PHOTOS']="./app/static/photos"     #posted images are stored here

db = SQLAlchemy(app)
#login mangement 
login_maneger=LoginManager() 
login_maneger.init_app(app)
login_maneger.login_view='login'


app.config.from_object(__name__) 

from app import views 
