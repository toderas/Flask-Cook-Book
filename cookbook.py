import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)

app.config["MONGO_DBNAME"] = 'cook-book'
app.config["MONGO_URI"] = 'mongodb+srv://tode:1Martie1998@myfirstcluster-dxyoc.mongodb.net/cook-book?retryWrites=true&w=majority'

mongo = PyMongo(app)



@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)