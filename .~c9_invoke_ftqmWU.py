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
 

 
app = Flask(__name__)

 #dish_upvotes,dish_views
@app.route('/donut_pie_chart/')
def donut_pie_chart():
    
    df =  pd.read_csv('static/data/recipe.csv')
    df = df.groupby('category_name')["dish_upvotes"].sum()
    df
    categories=df.groupby('category_name')
    
   # views_data = df["category_name"]
    pie_color = ("red", "green", "orange", "cyan", "blue")
    fig, ax = plt.subplots()
    ax.pie(df, labels=categories,colors = pie_color, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    inner_circle = plt.Circle((0,0),0.70,fc='white')
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
    
@app.route('/')
def index():
    return render_template("charts.html")
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)