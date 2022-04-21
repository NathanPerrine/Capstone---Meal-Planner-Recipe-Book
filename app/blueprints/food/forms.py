from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, FieldList, FormField
from wtforms.validators import DataRequired


class IngredientForm(FlaskForm):
    amount = StringField('Amount')
    ingredient = StringField('Ingredient')

class CreateRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    image = FileField('Recipe Image')
    instruction = StringField('Instructions')
    category = StringField('Category')
    cuisine = StringField('Cuisine')
    ingredients = FieldList(FormField(IngredientForm), min_entries=0)
    submit = SubmitField('Add')