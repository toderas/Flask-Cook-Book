import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app=Flask(__name__)

app.config["MONGO_DBNAME"] = 'cook-book'
app.config["MONGO_URI"] = 'mongodb+srv://tode:1Martie1998@myfirstcluster-dxyoc.mongodb.net/cook-book?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
    
@app.route("/recipes")
def recipes():
    return render_template("recipes.html",
             recipes=mongo.db.recipes.find())
             
             
@app.route("/aperitif")
def aperitif():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Aperitif'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/starter")
def starter():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Starter'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/intermediate")
def intermediate():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Intermediate'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/main")
def main():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Main'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/dessert")
def dessert():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Dessert'},
                    {"category_name": {'$exists': True}}]}))



@app.route("/addrecipe")
def addrecipe():
    return render_template("addrecipe.html",
                           categories=mongo.db.categories.find(),
                           skills=mongo.db.skills.find())
    

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))
    
    
@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes =  mongo.db.recipes.find(the_recipe)
    return render_template('showrecipe.html', recipe=the_recipe,
                           recipes=all_recipes)
    
    



if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)

