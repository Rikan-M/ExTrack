from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),nullable=False)
    email=db.Column(db.String(120),nullable=True,unique=True)
    password_hash=db.Column(db.String(128))
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    expanses=db.relationship('Expanse',backref='author',lazy='dynamic')
    categories=db.relationship('Category',backref='user',lazy='dynamic')
    budgets=db.relationship('Budget',backref='user',lazy='dynamic')

    def set_password(self,password):
        self.password_hash= generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),nullable=False)
    description=db.Column(db.String(200))


    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))


    expanses=db.relationship('Expanse',backref='expanse_category',lazy='dynamic')
    budgets=db.relationship('Budget',backref='budget_category',lazy='dynamic')

    __table_args__=(db.UniqueConstraint('user_id','name',name='unique_category_user'),)
    def __repr__(self):
        return f'<Category {self.name}>'

class Expanse(db.Model):
    __tablename__='expanses'
    id=db.Column(db.Integer,primary_key=True)
    amount=db.Column(db.Float,nullable=False)
    title=db.Column(db.String(50))
    date=db.Column(db.Date,index=True,nullable=False,default=datetime.utcnow)
    created_on=db.Column(db.DateTime, default=datetime.utcnow)
    updated_on=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    Category_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)

    payment_method=db.Column(db.String(50),default="Not Given")
    location=db.Column(db.String(100),default="Not Given")
    receipt_filename=db.Column(db.String(100),default="Not Given")

    def __repr__(self):
        return f'<Expense {self.amount} on {self.date}>'
    
class Budget(db.Model):
    __tablename__ = 'budgets'
    id=db.Column(db.Integer,primary_key=True)
    amount=db.Column(db.Float,nullable=False)
    period=db.Column(db.String(20),nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date=db.Column(db.Date)


    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    category_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)

    def __repr__(self):
        return f'<Budget {self.amount} for {self.period}>'
    

class Feedback(db.Model):
    __tablename__='feedback'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),nullable=False)
    feedback=db.Column(db.String(500),nullable=False)
    star=db.Column(db.Integer(),default=0)