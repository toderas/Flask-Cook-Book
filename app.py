import os
from helpers import *
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from werkzeug import secure_filename
from flask_paginate import Pagination

data_file = "static/data/recipe.csv"

UPLOAD_FOLDER = './/static/receipe-pictures/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config["MONGO_DBNAME"] = 'cook-book'
app.config["MONGO_URI"] = 'mongodb+srv://tode:1Martie1998@myfirstcluster-dxyoc.mongodb.net/cook-book?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route("/")

    
@app.route("/recipes")
def recipes():
    page = get_page()
    recipes = mongo.db.recipes.find().sort('upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')
    recipe_list = paginate_list(recipes, page, 6)
    return render_template("recipes.html", recipes=recipe_list,
                           pagination=pagination)
                           
@app.route("/top_ten")
def top_ten():
     recipes = mongo.db.recipes.find().sort('upvotes', pymongo.DESCENDING).limit(10)
     return render_template("recipes.html", recipes=recipes)
                          
             
             
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
    upload_file()
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))
    
    
@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc":
                                                               {'dish_views': 1}})
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
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        file = request.files['dish_photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

@app.route('/show_chart')
def show_chart():
    cursor = mongo.db.recipes.find({}, {'_id': 0, 
                                        "dish_name": 1, "dish_author": 1,
                                        "dish_prep_time": 1, "dish_origin_cuisine": 1,
                                        "dish_upvotes": 1, "category_name": 1,
                                        "country": 1, "dish_views": 1, "dish_required_skill": 1})
    total_recipes = cursor.count()
    write_to_csv(data_file, cursor)
    return render_template("charts.html", total_recipes=total_recipes)
           
           
     
@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc":
                                                               {'dish_upvotes': 1}})
    return redirect(url_for('show_recipe', recipe_id=recipe_id))



#if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)










# For Heroku Deployment

if __name__ == '__main__':
     app.run(host=os.environ.get('IP'),
             port=int(os.environ.get('PORT')),
             debug=True)
