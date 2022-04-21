from . import food
from .forms import CreateRecipeForm, IngredientForm
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user


@food.route('/createRecipe', methods=['GET', 'POST'])
@login_required
def createRecipe():
    title = 'Create a Recipe'
    recipeForm = CreateRecipeForm()
    ingredientForm = IngredientForm()

    if recipeForm.validate_on_submit():
        recipe_title = recipeForm.recipe_name.data
        recipe_category = recipeForm.category.data
        recipe_cuisine = recipeForm.cuisine.data

        print(recipe_title, recipe_category, recipe_cuisine)
        for form in recipeForm.ingredients:
            if form.amount.data and form.ingredient.data:
                print(form.amount.data, form.ingredient.data)
        # print(recipeForm.ingredients)

        return redirect(url_for('food.myRecipes'))


    return render_template('createRecipe.html', title = title, recipeForm = recipeForm, ingredientForm = ingredientForm)
    




@food.route('/myRecipes')
@login_required
def myRecipes():
    title = "My recipes"


    return render_template('myRecipes.html')