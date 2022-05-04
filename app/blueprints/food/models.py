from flask_login import user_logged_in, user_unauthorized
from app import db
import os 
import cloudinary
import cloudinary.uploader 
import cloudinary.api

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

class Recipe(db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    recipe_name     = db.Column(db.String(50), nullable = False)
    image_url       = db.Column(db.String(100), nullable = True)
    category        = db.Column(db.String(50), nullable = True)
    cuisine         = db.Column(db.String(50))
    instruction     = db.Column(db.Text(), nullable = True)
    reference       = db.Column(db.String(100), nullable = True)
    time            = db.Column(db.String(35), nullable = True)
    makes           = db.Column(db.String(50), nullable = True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    my_ingredients  = db.relationship('Ingredients', cascade="all, delete-orphan", backref = 'ingredients', lazy='dynamic')
    my_plans        = db.relationship('MyMealPlan', cascade="all, delete-orphan", backref='my_plans', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit() 

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'recipe_name', 'category', 'cuisine', 'instruction', 'reference', 'time', 'makes'}:
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        if self.image_url:
            self.delete_from_cloudinary()
        db.session.delete(self)
        db.session.commit()

    def upload_to_cloudinary(self, file_to_upload):
        image_info = cloudinary.uploader.upload(file_to_upload)
        self.image_url = image_info.get('url')
        db.session.commit()
    
    def delete_from_cloudinary(self):
        p_id = self.image_url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(p_id)
        db.session.commit()

    def __repr__(self):
        return f"<Recipe | {self.recipe_name}>"
    def __str__(self):
        return self.recipe_name


class Ingredients(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    recipe_id   = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient  = db.Column(db.String(), nullable = False)
    amount      = db.Column(db.String(), nullable = True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class MyMealPlan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class MyPantry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pantryItem = db.Column(db.String(50), nullable = False)
    pantryAmount = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit