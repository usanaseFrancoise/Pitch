from .import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import datetime
from datetime import datetime
datetime.utcnow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):

    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),unique=True)
    email=db.Column(db.String(255),unique=True,index=True)
    pass_secure=db.Column(db.String(255))   
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String(255))
    # photoprofiles=db.relationship('PhotoProfile',backref='user',lazy="dynamic")
    pitches=db.relationship('Pitch',backref='user',lazy="dynamic")
    comment=db.relationship('Comment',backref='user',lazy="dynamic")
    upvote=db.relationship('Upvote',backref='user',lazy="dynamic")
    downvote=db.relationship('Downvote',backref='user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('you cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure=generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure,password)
    def save_u(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User{self.username}'

class Pitch(db.Model):

    __tablename__='pitches'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable = False)
    post=db.Column(db.Text(),nullable = False)
    category=db.Column(db.String(255),index=True,nullable = False)
    votes=db.Column(db.Integer)

    # time=db.Column(db.Datetime, default = datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
     
    comment=db.relationship('Comment',backref='pitch',lazy="dynamic")
    upvote=db.relationship('Upvote',backref='pitch',lazy="dynamic")
    downvote=db.relationship('Downvote',backref='pitch',lazy="dynamic")

    def save_p(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'Pitch {self.post}'

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.Text())
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def save_c(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comments=Comment.query.filter_by(pitch_id=id).all()
        return comments

    def __repr__(self):
        return f'comment{self.comment}'
class Upvote(db.Model):
    __tablename__='upvotes'

    id = db.Column(db.Integer,primary_key = True)
    
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote=Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

class Downvote(db.Model):

    __tablename__='downvotes'
    id = db.Column(db.Integer,primary_key = True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls,id):


        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    def save_category(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_categories(cls):
        categories = Category.query.all()
        return categories