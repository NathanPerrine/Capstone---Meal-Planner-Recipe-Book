from app import db, login
from flask_login import UserMixin 
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email    = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    my_recipes = db.relationship('Recipe', backref = 'author', lazy='dynamic')
    my_mealplan = db.relationship('MyMealPlan', backref='mymealplan', lazy='dynamic')
    my_pantry = db.relationship('MyPantry', backref='mypantry', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def avatar(self, size):
        digest = md5(self.email.lower().strip().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=retro&s={size}'

    def change_password(self, new_password):
        self.password = generate_password_hash(new_password)
        db.session.commit()

    def __repr__(self):
        return f"<User | {self.username}>"
    def __str__(self):
        return self.username

    def check_password(self, password):
        return check_password_hash(self.password, password)