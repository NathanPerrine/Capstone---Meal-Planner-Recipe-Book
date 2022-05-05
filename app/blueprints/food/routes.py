from . import food
from .forms import CreateRecipeForm, IngredientForm, MealPlannerForm, SearchForm, PantryForm
from .models import Recipe, Ingredients, MyMealPlan, MyPantry
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from validators import url
import random
from app import db


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

@food.route('allRecipes', methods=['GET', 'POST'])
def allRecipes():
    title = "All Recipes"
    recipes = Recipe.query.all()
    searchForm = SearchForm()

    if searchForm.validate_on_submit():
        searchTerm = searchForm.search.data
        recipes = Recipe.query.filter( (Recipe.recipe_name.ilike(f'%{searchTerm}%')) | (Recipe.category.ilike(f'%{searchTerm}%')) | (Recipe.cuisine.ilike(f'%{searchTerm}%')) ).all()

    return render_template('allRecipes.html', title = title, recipes = recipes, searchForm = searchForm)

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
        # Delete recipe
        recipe.delete()
        flash(f'{recipe.recipe_name} has been deleted.', 'success')

    return redirect(url_for('food.myRecipes'))

@food.route('mealPlanner', methods=['GET', 'POST'])
@login_required
def mealPlanner():
    title = "Meal Planner"

    plannerForm = MealPlannerForm()
    mealPlan = current_user.my_mealplan.all()
    meals = [Recipe.query.filter(Recipe.id == mealPlan.recipe_id).all()[0] for mealPlan in current_user.my_mealplan.all()]

    recipe_ingredients = [meal.my_ingredients.all() for meal in meals]
    
    if plannerForm.validate_on_submit():
        recipes = Recipe.query.all()
        days = plannerForm.recipeCount.data
        
        try:
            days = int(days)
        except ValueError:
            flash('Numbers 0-7 only please.', 'warning')
            return redirect(url_for('food.mealPlanner'))

        if days < 0 or days > 7:
            flash("Please choose a number 0 to 7.", 'warning')
            return redirect(url_for('food.mealPlanner'))

        if days > len(recipes):
            flash("Sorry, we don't have that many recipes yet :(", 'warning')
            return redirect(url_for('food.mealPlanner'))
        
        # Delete current meal plan if all tests pass.
        for plan in mealPlan:
            plan.delete()

        # Generate new meal plan.
        meals = random.sample(recipes, days)
        for meal in meals:
            newMealPlan = MyMealPlan(recipe_id = meal.id, user_id = current_user.id)

        flash('Meal Plan Created!', 'success')
        return redirect(url_for('food.mealPlanner'))

        
    return render_template('mealPlanner.html', title=title, plannerForm=plannerForm, meals=meals, recipe_ingredients=recipe_ingredients)


@food.route('/pantry', methods=['GET', 'POST'])
@login_required
def pantry():
    title = "Pantry"
    user_pantry = current_user.my_pantry.all()
    pantryForm = PantryForm()

    if pantryForm.validate_on_submit():
        print('here')
        for form in pantryForm.pantryItem:
            amount = form.amount.data
            ingredient = form.ingredient.data

            if ingredient:
                newPantryItem = MyPantry(user_id = current_user.id, pantryItem = ingredient, pantryAmount = amount)
            
        return redirect(url_for('food.pantry'))
            

    return render_template('pantry.html', title=title, pantryForm=pantryForm, user_pantry=user_pantry)

@food.route('/deletePantryItem/<pantry_Id>')
@login_required
def deletePantryItem(pantry_Id):
    pantryItem = MyPantry.query.get_or_404(pantry_Id)

    if pantryItem.mypantry != current_user:
        flash('You do not have access to delete this pantry entry. Goodbye.', 'danger')
        return redirect(url_for('food.pantry'))

    pantryItem.delete()
    
    return redirect(url_for('food.pantry'))