from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField 
from wtforms.validators import DataRequired


class CreateRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    image = FileField('Recipe Image')
    instruction = StringField('Instructions')
    category = StringField('Category')
    cuisine = StringField('Cuisine')
    submit = SubmitField('Add')

class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient')
    amount = StringField('Amount')
