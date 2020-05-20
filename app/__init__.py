from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fhsizcgawmcohp:f240afe37480d5b883831cc0d278751ac6694957f97bb2ffb0ebe8c61f49eac8@ec2-54-86-170-8.compute-1.amazonaws.com:5432/daq3blumsb2lna"   #this is what will give acess to the database
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
