from .database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__=  "user"
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_mail =  db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    profile_img_path = db.Column(db.String(), default ="../static/IMG/user_profile_dummy.jpg")

    def __init__(self,email,password):
        self.user_mail = email
        self.password = password
    
    def get_id(self):
        return self.user_id
