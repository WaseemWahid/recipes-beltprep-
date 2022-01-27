
from flask import flash
from flask_bcrypt import Bcrypt
import re 

from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)

class User:
    schema = "recipe_users_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Create
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        user_id = connectToMySQL(cls.schema).query_db(query,data)
        return user_id

    # Read all
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.schema).query_db(query)
        users = []
        for row in results:
            users.append( cls(row) )
        return users

    # Read One by EMAIL
    @classmethod
    def get_by_email(cls, data):
        query= "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    # Read One by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])


    # UPDATE
    @classmethod
    def update(cls, data):
        query = """UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, updated_at = NOW() 
                WHERE id = %(id)s"""


        return connectToMySQL(cls.schema).query_db(query, data)
        #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        connectToMySQL(cls.schema).query_db(query, data)

    # VALIDATION 
    @staticmethod
    def register_validate(post_data):
        is_valid = True
        if len(post_data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(post_data["last_name"]) < 2:
            flash("Last name must be at least 2 characters.")
            # Email check make sure email has necessary characters and also check to see if email has been used before
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')    
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Invalid Email address.")
            is_valid = False
            # Email check to see if it has been used before 
        elif User.get_by_email({"email": post_data['email']}):
            flash("Email already in use")
            is_valid = False
        if len(post_data['password']) < 8:
            flash("Password must be atleast 8 characters.")
            is_valid = False
        elif post_data['password'] != post_data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False 

        return is_valid
    # Validation for login 
    @staticmethod
    def login_validate(post_data):
        user = User.get_by_email({"email": post_data['email']})
        #if user email is incorrect flash invalid credentials
        if not user:
            flash("Invalid Credentials")
            return False
        # if password is incorrect flash invalid password
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("invalid Password")
            return False 
        return True