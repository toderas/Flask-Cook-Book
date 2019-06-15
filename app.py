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
    return render_template("aperitif.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"dish_category": 'Aperitif'},
                    {"dish_category": {'$exists': True}}]}))
                    
@app.route("/starter")
def starter():
    return render_template("starter.html",
    recipes=mongo.db.recipes.find({
            "$and": [{"dish_category": 'Starter'},
                    {"dish_category": {'$exists': True}}]}))



@app.route("/addreceipe")
def addreceipe():
    return render_template("addreceipe.html")
    

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))
    flash('Recipe has been added', 'success')


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)

