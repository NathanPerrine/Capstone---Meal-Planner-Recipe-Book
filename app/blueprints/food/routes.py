from . import food
from .forms import CreateRecipeForm, IngredientForm
from .models import Recipe, Ingredients, MyRecipes
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
        new_recipe = Recipe(recipe_name = recipe_title, category = recipe_category, cuisine = recipe_cuisine, instruction = instructions, time = time, makes = makes, reference = reference)
        # if image is present, upload to cloudinary
        if image:
            new_recipe.upload_to_cloudinary(image)

        # Grab all the ingredient forms
        for form in recipeForm.ingredients:
            amount = form.amount.data
            ingredient = form.ingredient.data
            if (amount and ingredient) or ingredient:
                new_ingredient = Ingredients(recipe_id = new_recipe.id, ingredient = ingredient, amount = amount)


        user_id = current_user.id
        recipe_id = new_recipe.id
        new_my_recipe = MyRecipes(recipe_id = recipe_id, user_id = user_id)

        return redirect(url_for('food.myRecipes'))

    return render_template('createRecipe.html', title = title, recipeForm = recipeForm, ingredientForm = ingredientForm)

@food.route('/myRecipes')
@login_required
def myRecipes():
    title = "My recipes"
    # print(current_user.my_recipes.all()[0].recipe_id)
    recipes = [Recipe.query.filter(Recipe.id == recipe.recipe_id).all()[0] for recipe in current_user.my_recipes.all()]
    # print(recipes)
    # print(recipes[0].my_ingredients.all())

    return render_template('myRecipes.html', title=title, recipes=recipes)

@food.route('allRecipes')
def allRecipes():
    title = "All Recipes"
    recipes = Recipe.query.all()
    print(recipes)

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
    print(recipe)
    # print(recipe.instruction)
    instructions = recipe.instruction.split('\n')
    print(instructions)

    return render_template('singleRecipe.html', title = title, recipe = recipe, ingredients = ingredients, instructions = instructions, refIsUrl=refIsUrl)

@food.route('editRecipe/<recipe_Id>', methods=["GET", "POST"])
@login_required
def editRecipe(recipe_Id):
    recipe = Recipe.query.get_or_404(recipe_Id)
    currentIngredients = recipe.my_ingredients.all()

    title = f'Edit | {recipe.recipe_name}'
    
    recipeForm = CreateRecipeForm()
    ingredientForm = IngredientForm()

    if recipeForm.validate_on_submit():
        print("Deleting old ingredients...")
        for ingredient in currentIngredients:
            ingredient.delete()
        print("Adding new ingredietns...")
        for form in recipeForm.ingredients:
            amount = form.amount.data
            ingredient = form.ingredient.data
            
            if (amount and ingredient) or ingredient:
                new_ingredient = Ingredients(recipe_id = recipe.id, ingredient = ingredient, amount = amount)
        
        print("Updating recipe...")
        recipe.update(**recipeForm.data)

        flash(f"{recipe.recipe_name} has been updated.", "warning")
        return redirect(url_for('food.editRecipe', recipe_Id=recipe.id)) 


    return render_template('editRecipe.html', title=title, recipe=recipe, recipeForm=recipeForm, ingredientForm=ingredientForm, ingredients=currentIngredients)