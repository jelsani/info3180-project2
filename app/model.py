from . import db 

#Creates posts database
class posts(db.Model):
    __tablename__="posts" 
    
    id = db.Column(db.Integer, primary_key=True) 
    user_id=db.Column(db.Integer)
    photo=db.Column(db.String(80))
    caption=db.Column(db.String(140)) 
    created_on=db.Column(db.Date)
    
    def __init__(self,user_id,photo,caption,created_on):
        self.user_id=user_id
        self.photo=photo 
        self.caption=caption 
        self.created_on=created_on
    
#Creates users database
class users(db.Model):
    __tablename__="users"
    
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    password=db.Column(db.String(200))
    firstname=db.Column(db.String(80))
    lastname=db.Column(db.String(80))
    email=db.Column(db.String(80))
    location=db.Column(db.String(80))
    biography=db.Column(db.String(2000)) 
    profile_picture=db.Column(db.String(100)) 
    joined_on=db.Column(db.Date) 
    
    def __init__(self, username,password,firstname, lastname, email, location, biography, profile_picture,joined_on):
        self.username= username
        self.password= password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email 
        self.location = location 
        self.biography = biography 
        self.profile_picture = profile_picture 
        self.joined_on=joined_on
    
    def is_authenticated(self): 
        return True 
    
    def is_active(self):
        return True 
    
    def is_anonymous(self):
        return False 
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id) 
    
    def __repr__(self):
        return '<User %r>' % (self.username)

#Creates likes database
class likes(db.Model):
    __tablename__="likes" 
    
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer)
    post_id=db.Column(db.Integer) 
    
    def __init__(self,user_id,post_id):
        self.user_id=user_id
        self.post_id=post_id   

#Creates followers database
class Followers(db.Model):
    __tablename__="followers" 
    
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    follower_id=db.Column(db.Integer)
     
    def __init__(self,user_id,follower_id):
        self.user_id=user_id
        self.follower_id=follower_id