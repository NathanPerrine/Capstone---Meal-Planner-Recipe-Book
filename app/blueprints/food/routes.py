from . import food
from .forms import CreateRecipeForm, IngredientForm
from flask import render_template
from flask_login import login_required, current_user


@food.route('/createRecipe', methods=['GET', 'POST'])
@login_required
def createRecipe():
    title = 'Create a Recipe'
    recipeForm = CreateRecipeForm()
    ingredientForm = IngredientForm()


    return render_template('createRecipe.html', title = title, recipeForm = recipeForm, ingredientForm = ingredientForm)
    