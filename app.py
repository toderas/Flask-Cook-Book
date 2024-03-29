import os
import csv
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
from helpers import *
from flask import Flask, render_template, redirect, request, url_for, flash, send_file, make_response, send_from_directory
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_paginate import Pagination
from forms import *
plt.style.use('ggplot')


UPLOAD_FOLDER = '../static/receipe-pictures/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)


app.secret_key = "super secret key"


app.config["MONGO_DBNAME"] = os.environ.get('dbname')
app.config["MONGO_URI"] = os.environ.get('db_uri')


mongo = PyMongo(app)


# retrieves recipes from db and displays 10 items per page
@app.route('/')
@app.route("/recipes")
def recipes():
    page = get_page()
    recipes = mongo.db.recipes.find().sort('dish_upvotes', pymongo.DESCENDING)
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Recipes")


# retrieves most voted 10 items in db
@app.route("/top_ten")
def top_ten():
    recipes = mongo.db.recipes.find().sort('dish_upvotes', pymongo.DESCENDING).limit(10)
    return render_template("top-ten.html", recipes=recipes, title="Top 10 recipes")


# retrieves items based on criteria (aperitif starter main etc)
@app.route("/aperitif")
def aperitif():
    page = get_page()
    recipes = mongo.db.recipes.find({"$and": [{"category_name": 'Aperitif'},
                                    {"category_name": {'$exists': True}}]})
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Aperitifs")


@app.route("/starter")
def starter():
    page = get_page()
    recipes = mongo.db.recipes.find({"$and": [{"category_name": 'Starter'},
                                    {"category_name": {'$exists': True}}]})
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Starters")


@app.route("/intermediate")
def intermediate():
    page = get_page()
    recipes = mongo.db.recipes.find({"$and": [{"category_name": 'Intermediate'},
                                    {"category_name": {'$exists': True}}]})
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Intermediate")


@app.route("/main")
def main():
    page = get_page()
    recipes = mongo.db.recipes.find({"$and": [{"category_name": 'Main'},
                                    {"category_name": {'$exists': True}}]})
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Mains")


@app.route("/dessert")
def dessert():
    page = get_page()
    recipes = mongo.db.recipes.find({"$and": [{"category_name": 'Dessert'},
                                    {"category_name": {'$exists': True}}]})
    pagination = Pagination(page=page, per_page=9, total=recipes.count(),
                            record_name='recipes', css_framework='bootstrap4')
    recipe_list = paginate_list(recipes, page, 9)
    return render_template("recipes.html", recipes=recipe_list, pagination=pagination, title="Dessert")


@app.route('/addrecipe', methods=['GET', 'POST'])
def addrecipe():
    form = AddRecipeForm()
    if request.method == 'POST' and form.validate_on_submit():
        if 'file' not in request.files:
            flash('Recipe added with no photo')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Recipe added with no photo', 'danger')
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join('static/receipe-pictures/', filename))
        flash(f'Recipe  created for {form.dish_name.data}!', 'success')
        recipes = mongo.db.recipes
        value = {
                'dish_name': request.form.get('dish_name'),
                'dish_author': request.form.get('dish_author'),
                'dish_required_skill': request.form.get('dish_required_skill'),
                'dish_prep_time': request.form.get('dish_prep_time'),
                'dish_origin_cuisine': request.form.get('dish_origin_cuisine'),
                'dish_ingredients': request.form.get('dish_ingredients'),
                'dish_preparation_steps': request.form.get('dish_preparation_steps'),
                'category_name': request.form.get('category_name'),
                'dish_photo': request.files['file'].filename,
                }
        recipes.insert(value)
        return redirect(url_for('recipes', form=form))
    return render_template("addrecipe.html",
                           categories=mongo.db.categories.find(),
                           skills=mongo.db.skills.find(), form=form, title="New Recipe")


# retrieves item from database and displays all its details (it also ads one to number of views)
@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {'dish_views': 1}})
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes = mongo.db.recipes.find(the_recipe)
    return render_template('showrecipe.html', recipe=the_recipe,
                           recipes=all_recipes)


# retrievs item from database and populates form for editing followed by inserting new values into db
@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    form = EditRecipeForm()
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find()
    skills = mongo.db.skills.find()
    if request.method == 'POST' and form.validate_on_submit():
        flash(f' {form.dish_name.data} Has Been Succesfully Updated', 'success')
        value = {
                'dish_name': request.form.get('dish_name'),
                'dish_author': request.form.get('dish_author'),
                'dish_required_skill': request.form.get('dish_required_skill'),
                'dish_prep_time': request.form.get('dish_prep_time'),
                'dish_origin_cuisine': request.form.get('dish_origin_cuisine'),
                'dish_ingredients': request.form.get('dish_ingredients'),
                'dish_preparation_steps': request.form.get('dish_preparation_steps'),
                'category_name': request.form.get('dish_category_name'),
                'dish_photo': request.form.get('dish_photo'),
                }
        recipes = mongo.db.recipes
        recipes.update({'_id': ObjectId(recipe_id)}, value)
        return redirect(url_for('recipes', form=form, value=value))
    form.dish_name.data = recipe["dish_name"]
    form.dish_author.data = recipe["dish_author"]
    form.dish_prep_time.data = recipe["dish_prep_time"]
    form.dish_origin_cuisine.data = recipe["dish_origin_cuisine"]
    form.dish_ingredients.data = recipe["dish_ingredients"]
    form.dish_preparation_steps.data = recipe["dish_preparation_steps"]
    form.category_name.data = recipe["category_name"]
    form.dish_required_skill.data = recipe["dish_required_skill"]
    form.dish_photo.data = recipe["dish_photo"]
    return render_template('editrecipe.html', form=form, recipe=recipe,
                           categories=categories,
                           skills=skills, title="Edit Recipe")


# removes item from database and image from filesistem
@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    file = recipe["dish_photo"]
    if file != '':
        os.remove((os.path.join('static/receipe-pictures/', file)))
        flash(f'Recipe has been Removed', 'danger')
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))


# sends data to csv file and returns page with charts
@app.route('/show_chart')
def show_chart():
    cursor = mongo.db.recipes.find({}, {'_id': 0,
                                        "dish_name": 1, "dish_author": 1, "dish_views": 1, "dish_upvotes": 1,
                                        "dish_prep_time": 1, "dish_required_skill": 1,
                                        "dish_origin_cuisine": 1, "category_name": 1
                                        })
    total_recipes = cursor.count()
    write_to_csv(data_file, cursor)
    return render_template("charts.html", total_recipes=total_recipes, title="Statistics")


# creates pie chart with data from csv
@app.route('/donut_pie_chart_views/')
def donut_pie_chart_views():
    df = pd.read_csv('static/data/recipe.csv')
    ds = df.groupby("category_name")['dish_views'].sum()
    categories = ["Aperitif", "Dessert", "Intermediate", "Main", "Starter"]
    pie_color = ("red", "green", "orange", "cyan", "blue")
    fig, ax = plt.subplots()
    ax.pie(ds, labels=categories, colors=pie_color, autopct='%1.1f%%', startangle=90, pctdistance=0.55)
    inner_circle = plt.Circle((0, 0), 0)
    fig = plt.gcf()
    fig.gca().add_artist(inner_circle)
    ax.axis('equal')
    ax.set_title("Views Per Category\n", fontsize=24)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/donut_pie_chart_likes/')
def donut_pie_chart_likes():
    df = pd.read_csv('static/data/recipe.csv')
    ds = df.groupby("category_name")['dish_upvotes'].sum()
    categories = ["Aperitif", "Dessert", "Intermediate", "Main", "Starter"]
    pie_color = ("red", "green", "orange", "cyan", "blue")
    fig, ax = plt.subplots()
    ax.pie(ds, labels=categories, colors=pie_color, autopct='%1.1f%%', startangle=90, pctdistance=0.55)
    inner_circle = plt.Circle((0, 0), 0)
    fig = plt.gcf()
    fig.gca().add_artist(inner_circle)
    ax.axis('equal')
    ax.set_title("Likes Per Category\n", fontsize=24)
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


# upvote functionality
@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$inc":
                                                               {'dish_upvotes': 1}})
    return redirect(url_for('show_recipe', recipe_id=recipe_id))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False)
