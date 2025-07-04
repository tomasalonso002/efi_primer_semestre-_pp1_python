from datetime import datetime

from app import db

from flask_login import UserMixin


class User(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(256), nullable = False, unique = False)
    is_active = db.Column(db.Boolean, default=True)
    def __str__(self):
        return self.name
    
class Post(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    content = db.Column(db.Text, nullable= False)
    date_time = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    autor = db.relationship(
        "User",
        backref = db.backref("posts", lazy=True)
    )
    def __str__(self):
        return self.title
    
class Comment(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    text_comment = db.Column(db.Text, nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable= False)
    autor = db.relationship(
        "User",
        backref = db.backref("comments", lazy=True)
    )
    
    def __str__(self):
        return self.text_comment
    




    