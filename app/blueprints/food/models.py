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
    image           = db.Column(db.String(50), nullable = False)
    category        = db.Column(db.String(50), nullable = False)
    cuisine         = db.Column(db.String(50))
    instruction     = db.Column(db.String(), nullable = False)
    my_ingredients  = db.relationship('Ingredients', backref = 'ingredients', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit() 

    def upload_to_cloudinary(self, file_to_upload):
        image_info = cloudinary.uploader.upload(file_to_upload)
        self.image_url = image_info.get('url')
        db.session.commit()

    def __repr__(self):
        return f"<Recipe | {self.name}>"
    def __str__(self):
        return self.name

        
class Ingredients(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    recipe_id   = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient  = db.Column(db.String(), nullable = False)
    amount      = db.Column(db.String(), nullable = True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()