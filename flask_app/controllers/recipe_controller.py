from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import users_controller

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
        logged_in_user = User.get_by_id({"id": session['uuid']}), all_recipes = Recipe.get_all()
    )

@app.route("/recipes/new")
def new_recipe():
    return render_template("recipes/new_recipe.html")


@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    return render_template("/recipes/edit_recipe.html", recipe = Recipe.read_one({"id": recipe_id}))



@app.route("/recipes/create", methods =["POST"])
def create_recipe():
    if not Recipe.validator(request.form):
        return redirect("/recipes/new")
    recipe_data = {
        **request.form,
        "user_id": session['uuid']
        }
    print(recipe_data)
    Recipe.create(recipe_data)
    return redirect("/dashboard")


@app.route("/recipes/update/<int:recipe_id>", methods =["POST"])
def update_recipe(recipe_id):
    if not Recipe.validator(request.form):
        return redirect("/recipes/new")
    recipe_data = {
        **request.form,
        "id": recipe_id
    }
    Recipe.update(recipe_data)
    return redirect("/dashboard")

@app.route("/recipes/<int:recipe_id>")
def display_recipe(recipe_id):
    return render_template("recipes/display_recipe.html", 
    logged_in_user = User.get_by_id({"id": session['uuid']}),
    one_recipe = Recipe.read_one({"id": recipe_id})
    )


@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    Recipe.delete({"id": recipe_id})

    return redirect("/dashboard")