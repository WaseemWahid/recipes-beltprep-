from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re

from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import recipe_controller
from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)

# INDEX
@app.route("/")
def index():
	if "uuid" in session:
		return redirect("/dashboard")

	return render_template("index.html")

#USERS ROUTE
@app.route("/users")
def display_users():
	if "uuid" not in session:
		return redirect("/")

	return render_template("dashboard.html", all_users = User.get_all(), user = User.get_by_id({"id":session['uuid']}))

#REGISTER ROUTE 
@app.route("/register", methods = ["POST"])
def register():
	if not User.register_validate(request.form):
		return redirect("/")
	# HASH PASSWORD
	hash_slinging_slasher = bcrypt.generate_password_hash(request.form["password"])
	print(hash_slinging_slasher)
	user_data = {
		**request.form,
		"password": hash_slinging_slasher
	    }
	user_id = User.create(user_data)
	session["uuid"] = user_id
	return redirect('/dashboard')

# LOGIN ROUTE 
@app.route("/login", methods=["POST"])
def login():
	# CHECK TO SEE IF LOGIN IN VALIDATED
	if not User.login_validate(request.form):
		return redirect("/")
	# CREATE A SESSION FOR THE USER LOGIN
	user = User.get_by_email({"email": request.form['email']})
	session["uuid"] = user.id
	return redirect("/dashboard")

#LOGOUT ROUTE 
@app.route("/logout")
def logout():
	session.clear()
	
	return redirect("/")