import os
from helpers import *
from chart import *
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_paginate import Pagination
import pprint;
from forms import *



app = Flask(__name__)


app.secret_key = "super secret key"

app.config["MONGO_DBNAME"] = 'cook-book'
app.config["MONGO_URI"] = 'mongodb+srv://tode:1Martie1998@myfirstcluster-dxyoc.mongodb.net/cook-book?retryWrites=true'

mongo = PyMongo(app)


@app.route("/")

    
@app.route("/recipes")
def recipes():
    page = get_page()
    recipes = mongo.db.recipes.find().sort('dish_upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')
    recipe_list = paginate_list(recipes, page, 10)
    return render_template("recipes.html", recipes=recipe_list,
                           pagination=pagination)
                           
@app.route("/top_ten")
def top_ten():
    recipes = mongo.db.recipes.find().sort('dish_upvotes', pymongo.DESCENDING).limit(10)
    return render_template("top-ten.html", recipes=recipes)
                          
             
             
@app.route("/aperitif")
def aperitif():
    
    return render_template("filtered.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Aperitif'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/starter")
def starter():
    return render_template("filtered.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Starter'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/intermediate")
def intermediate():
    return render_template("filtered.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Intermediate'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/main")
def main():
    return render_template("filtered.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Main'},
                    {"category_name": {'$exists': True}}]}))
                    
@app.route("/dessert")
def dessert():
    return render_template("filtered.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"category_name": 'Dessert'},
                    {"category_name": {'$exists': True}}]}))



@app.route('/addrecipe', methods=['GET','POST'])
def addrecipe():
    form = AddRecipeForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash (f'Recipe  created for {form.dish_name.data}!', 'success')
        recipes = mongo.db.recipes
        recipes.insert_one(request.form.to_dict())
        return redirect(url_for('recipes', form=form))
   
    return render_template("addrecipe.html",
                           categories=mongo.db.categories.find(),
                           skills=mongo.db.skills.find(),title='New Recipe', form=form)
    
    
    
@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc":
                                                               {'dish_views': 1}})
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes =  mongo.db.recipes.find(the_recipe)
    return render_template('showrecipe.html', recipe=the_recipe,
                           recipes=all_recipes)
    
    

@app.route('/edit_recipe/<recipe_id>', methods=['GET','POST'])
def edit_recipe(recipe_id):
    form = EditRecipeForm()
    recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories =  mongo.db.categories.find()
    skills = mongo.db.skills.find()
    if request.method == 'POST' and form.validate_on_submit():
        flash (f' {form.dish_name.data} Has Been Succesfully Updated', 'success')
        value = {
        'dish_name':request.form.get('dish_name'),
        'dish_author':request.form.get('dish_author'),
        'dish_required_skill': request.form.get('dish_required_skill'),
        'dish_prep_time': request.form.get('dish_prep_time'),
        'dish_origin_cuisine':request.form.get('dish_origin_cuisine'),
        'dish_ingredients':request.form.get('dish_ingredients'),
        'dish_preparation_steps':request.form.get('dish_preparation_steps'),
        'category_name':request.form.get('category_name'),
        }
        recipes = mongo.db.recipes
        recipes.update( {'_id': ObjectId(recipe_id)},value)
        return redirect(url_for('recipes', form=form,value=value))
    form.dish_name.data = recipe["dish_name"]
    form.dish_author.data = recipe["dish_author"]
    form.dish_prep_time.data = recipe["dish_prep_time"]
    form.dish_origin_cuisine.data = recipe["dish_origin_cuisine"]
    form.dish_ingredients.data = recipe["dish_ingredients"]
    form.dish_preparation_steps.data = recipe["dish_preparation_steps"]
    return render_template('editrecipe.html',form=form, recipe=recipe,
                           categories=categories,
                           skills=skills)
                           

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    flash (f'Recipe has been Removed','danger')
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))
    
    
@app.route('/show_chart')
def show_chart():
    cursor = mongo.db.recipes.find({}, {'_id': 0, 
                                        "dish_name": 1, "dish_author": 1,"dish_views": 1,"dish_upvotes": 1,"dish_prep_time": 1,"dish_required_skill": 1,
                                         "dish_origin_cuisine": 1, "category_name": 1,
                                         })
    total_recipes = cursor.count()
    write_to_csv(data_file, cursor)
    return render_template("charts.html", total_recipes=total_recipes, title="Statistics" )

@app.route('/donut_pie_chart_views/')
def donut_pie_chart_views():
    df =  pd.read_csv('static/data/recipe.csv')
    ds = df.groupby("category_name")['dish_views'].sum()
    #categories=df.groupby("category_name")['category_name'].sum()
    categories = ["Aperitif","Dessert","Intermediate","Main","Starter"]
    
    pie_color = ("red", "green", "orange", "cyan", "blue")
    fig, ax = plt.subplots()
    ax.pie(ds, labels=categories,colors = pie_color, autopct='%1.1f%%', startangle=90, pctdistance=0.55)
    inner_circle = plt.Circle((0,0),0)
    fig = plt.gcf()
    fig.gca().add_artist(inner_circle)
    ax.axis('equal')  
    ax.set_title("Views Per Category\n",fontsize=24)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
    
@app.route('/donut_pie_chart_likes/')
def donut_pie_chart_likes():
    df =  pd.read_csv('static/data/recipe.csv')
    ds = df.groupby("category_name")['dish_upvotes'].sum()
    #categories=df.groupby("category_name")['category_name'].sum()
    categories = ["Aperitif","Dessert","Intermediate","Main","Starter"]
    
    pie_color = ("red", "green", "orange", "cyan", "blue")
    fig, ax = plt.subplots()
    ax.pie(ds, labels=categories,colors = pie_color, autopct='%1.1f%%', startangle=90, pctdistance=0.55)
    inner_circle = plt.Circle((0,0),0)
    fig = plt.gcf()
    fig.gca().add_artist(inner_circle)
    ax.axis('equal')  
    ax.set_title("Likes Per Category\n",fontsize=24)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
           
           
     
@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc":
                                                               {'dish_upvotes': 1}})
    return redirect(url_for('show_recipe', recipe_id=recipe_id))



if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)










# For Heroku Deployment

#if __name__ == '__main__':
  #   app.run(host=os.environ.get('IP'),
     #        port=int(os.environ.get('PORT')),
     #        debug=True)
