from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, FieldList, FormField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class IngredientForm(FlaskForm):
    amount = StringField('Amount')
    ingredient = StringField('Ingredient')

class CreateRecipeForm(FlaskForm):
    recipe_name         = StringField('Recipe Name', validators=[DataRequired()])
    image               = FileField('Recipe Image')
    instruction         = TextAreaField('Instructions')
    category            = StringField('Category')
    cuisine             = StringField('Cuisine')
    ingredients         = FieldList(FormField(IngredientForm), min_entries=0)
    reference           = StringField('Reference')
    time                = StringField('Time')
    makes               = StringField('Makes')
    submit              = SubmitField('Submit')

class MealPlannerForm(FlaskForm):
    recipeCount = StringField('Recipe Count', validators=[DataRequired()])
    dinnersOnly = BooleanField('Dinner Only', default=True)
    submit      = SubmitField('Submit')