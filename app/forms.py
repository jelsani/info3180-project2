from flask import render_template, request, redirect, url_for, flash 
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FileField, PasswordField
from wtforms.validators import DataRequired, Email  

class registerform(FlaskForm):
    username=StringField("username",validators=[DataRequired() ]) 
    password=StringField("password",validators=[DataRequired()]) 
    firstname=StringField("firstname",validators=[DataRequired()]) 
    lastname=StringField("lastname",validators=[DataRequired()]) 
    email=StringField('email',validators=[DataRequired(),Email()]) 
    Location=StringField('location',validators=[DataRequired()]) 
    biography=TextAreaField('biography',validators=[DataRequired()]) 
    profile_picture=FileField('profile_picture',validators=[FileRequired(),FileAllowed(['jpg','png','Images only!'])])


class loginform(FlaskForm): 
    username=StringField('username',validators=[DataRequired()]) 
    password=PasswordField("password",validators=[DataRequired()])
  
    
class newpost(FlaskForm):
    photo=FileField("photo",validators=[FileRequired(),FileAllowed(['jpg','png','Images only'])])
    caption=TextAreaField("caption",validators=[DataRequired()])