import os
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app=Flask(__name__)

app.config["MONGO_DBNAME"] = 'cook-book'
app.config["MONGO_URI"] = 'mongodb+srv://tode:1Martie1998@myfirstcluster-dxyoc.mongodb.net/cook-book?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route("/")
#@app.route("/home")
#def home():
   # return render_template("home.html")
    
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



@app.route('/addrecipe')
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
    
    

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    get_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    get_details = mongo.db.recipes.find(get_recipe)
    get_categories =  mongo.db.categories.find()
    get_skills = mongo.db.skills.find()
    return render_template('editrecipe.html', recipe=get_recipe,
                            recipes=get_details,
                           categories=get_categories,
                           skills=get_skills)
                           
                           
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'dish_name':request.form.get('dish_name'),
        'dish_author':request.form.get('dish_author'),
        'dish_required_skill': request.form.get('dish_required_skill'),
        'dish_prep_time': request.form.get('dish_prep_time'),
        'dish_origin_cuisine':request.form.get('dish_origin_cuisine'),
        'dish_ingredients':request.form.get('dish_ingredients'),
        'dish_preparation_steps':request.form.get('dish_preparation_steps'),
        'category_name':request.form.get('category_name'),
    })
    return redirect(url_for('recipes'))
    

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))





if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)

