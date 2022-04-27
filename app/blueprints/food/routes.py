from . import food
from .forms import CreateRecipeForm, IngredientForm
from .models import Recipe, Ingredients
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from validators import url


def test_url(test_string):
    if url(test_string.strip()):
        return True 
    return False

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
        instructions = recipeForm.instruction.data
        time = recipeForm.time.data 
        makes = recipeForm.makes.data
        reference = recipeForm.reference.data
        image = recipeForm.image.data


        # Create new recipe 
        new_recipe = Recipe(recipe_name = recipe_title, category = recipe_category, cuisine = recipe_cuisine, instruction = instructions, time = time, makes = makes, reference = reference, user_id=current_user.id)
        # if image is present, upload to cloudinary
        if image:
            new_recipe.upload_to_cloudinary(image)

        # Grab all the ingredient forms
        for form in recipeForm.ingredients:
            amount = form.amount.data
            ingredient = form.ingredient.data
            if (amount and ingredient) or ingredient:
                new_ingredient = Ingredients(recipe_id = new_recipe.id, ingredient = ingredient, amount = amount)


        # user_id = current_user.id
        # recipe_id = new_recipe.id
        # new_my_recipe = MyRecipes(recipe_id = recipe_id, user_id = user_id)

        return redirect(url_for('food.myRecipes'))

    return render_template('createRecipe.html', title = title, recipeForm = recipeForm, ingredientForm = ingredientForm)

@food.route('/myRecipes')
@login_required
def myRecipes():
    title = "My recipes"
    recipes = current_user.my_recipes.all()

    return render_template('myRecipes.html', title=title, recipes=recipes)

@food.route('allRecipes')
def allRecipes():
    title = "All Recipes"
    recipes = Recipe.query.all()

    return render_template('allRecipes.html', title = title, recipes = recipes)

@food.route('singleRecipe/<recipe_Id>')
@login_required 
def singleRecipe(recipe_Id):
    recipe = Recipe.query.get_or_404(recipe_Id)
    title = recipe.recipe_name
    ingredients = recipe.my_ingredients.all()
    refIsUrl = ""
    if recipe.reference:
        refIsUrl = (test_url(recipe.reference))
    # print(recipe.instruction)
    instructions = recipe.instruction.split('\n')

    return render_template('singleRecipe.html', title = title, recipe = recipe, ingredients = ingredients, instructions = instructions, refIsUrl=refIsUrl)

@food.route('editRecipe/<recipe_Id>', methods=["GET", "POST"])
@login_required
def editRecipe(recipe_Id):
    recipe = Recipe.query.get_or_404(recipe_Id)
    currentIngredients = recipe.my_ingredients.all()
    title = f'Edit | {recipe.recipe_name}'
    recipeForm = CreateRecipeForm()
    ingredientForm = IngredientForm()

    # Test if the recipe author is current user, if not redirect away from page.
    if recipe.author != current_user:
        flash("You do not have edit access for this recipe.", "danger")
        return redirect(url_for('food.myRecipes'))

    if recipeForm.validate_on_submit():
        # Deleting old ingredients...
        for ingredient in currentIngredients:
            ingredient.delete()
        # "Adding new ingredietns...
        for form in recipeForm.ingredients:
            amount = form.amount.data
            ingredient = form.ingredient.data
            
            if (amount and ingredient) or ingredient:
                new_ingredient = Ingredients(recipe_id = recipe.id, ingredient = ingredient, amount = amount)

        # Updating recipe...
        recipe.update(**recipeForm.data)

        # Check if an image was provided, if it was upload it
        image = recipeForm.image.data
        if image:
            # Delete image from cloudinary if one already exists
            if recipe.image_url:
                recipe.delete_from_cloudinary()
            # Upload new image
            print("Uploading image to cloudinary...")
            recipe.upload_to_cloudinary(image)

        flash(f"{recipe.recipe_name} has been updated.", "info")
        return redirect(url_for('food.editRecipe', recipe_Id=recipe.id)) 

    return render_template('editRecipe.html', title=title, recipe=recipe, recipeForm=recipeForm, ingredientForm=ingredientForm, ingredients=currentIngredients)

@food.route('deleteRecipe/<recipe_Id>')
@login_required
def deleteRecipe(recipe_Id):
    recipe = Recipe.query.get_or_404(recipe_Id)
    ingredients = recipe.my_ingredients.all()

    # Check if recipe author is current user, if not redirect away.
    if recipe.author != current_user:
        flash('You do not have access to delete this post. Goodbye.', 'danger')
        return redirect(url_for('food.myRecipes'))
    else:
        # Delete ingredients
        for ingredient in ingredients:
            print('deleting ingredient')
            ingredient.delete()
        # Delete image from cloudinary
        if recipe.image_url:
            recipe.delete_from_cloudinary()

        # Delete recipe
        print('deleting recipe')
        recipe.delete()
        flash(f'{recipe.recipe_name} has been deleted.', 'success')

    return redirect(url_for('food.myRecipes'))