import os
from io import BytesIO
from flask import Flask, render_template, send_file, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('ggplot')
import csv
from collections import OrderedDict

 
app = Flask(__name__)

 #dish_upvotes,dish_views
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
    
    
@app.route('/')
def index():
    return render_template("charts.html")
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)