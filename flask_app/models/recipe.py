from flask import flash
from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    schema = "recipe_users_schema"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_thirty = data['under_thirty']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = user.User.get_by_id({"id": data["user_id"]})

    #CREATE
    @classmethod
    def create(cls, data):
        query = """INSERT INTO recipes(user_id, name, description, instruction, date_made, created_at, updated_at)
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instruction)s, CURDATE(), NOW(), NOW());
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    # Read ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.schema).query_db(query)

        recipe_objs = []

        for row in results:
            recipe_objs.append(cls(row))
        return recipe_objs

    # READ ONE 
    @classmethod
    def read_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])

    # UPDATE
    @classmethod
    def update(cls, data):
        query = """ UPDATE recipes SET name = %(name)s, description = %(description)s, 
        instruction = %(instruction)s, updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    # DELETE 
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)

    # VALIDATOR
    @staticmethod
    def validator(post_data):
        is_valid = True

        if len(post_data['name']) < 2:
            flash("name must be atleast 2 characters ")
            is_valid = False
        if len(post_data['description']) < 10:
            flash("description should be atleast 10 characters")
            is_valid = False 
        if len(post_data['instruction']) < 10:
            flash("instruction should be atleast 10 characters")
            is_valid = False 
        return is_valid