from .database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__=  "user"
    user_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    user_mail =  db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    user_name = db.Column(db.String())
    profile_img_path = db.Column(db.String(), default ="../static/IMG/user_profile_dummy.jpg")
    user_bio = db.Column(db.String())

    def __init__(self,email,password):
        self.user_mail = email
        self.password = password
        self.user_name = email.split('@')[0]
    
    def get_id(self):
        return self.user_id
    
class Posts(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    post_image_path = db.Column(db.String())
    post_desc = db.Column(db.String())

    def __init__(self,user_id, post_image_path, post_desc):
        self.user_id = user_id
        self.post_image_path = post_image_path
        self.post_desc = post_desc

class PostLikes(db.Model):
    __tablename__ = "post_likes"
    like_id = db.Column(db.Integer(),primary_key = True, autoincrement =True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.post_id'))


class UserFollower(db.Model):
    __tablename__ = "user_follower"
    follower_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    follower_user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))

class PostComments(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.post_id'))
    comment = db.Column(db.String())


