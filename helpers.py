from flask import Flask, request, flash
from flask_pymongo import PyMongo, pymongo
import csv
import pprint;


app = Flask(__name__)
# path for csv file 
data_file = "static/data/recipe.csv"

def get_page():
    return request.args.get('page', 1, type=int)

# pagination 
def paginate_list(query, page_number, per_page):
    array = [item for item in query]
    paginated_array = array[((page_number*per_page)-per_page):(page_number*per_page)]
    return paginated_array


# writes data on csv file 
def write_to_csv(data_file, cursor):
    with open(data_file, "w+") as outfile:
        fields = [ "dish_name", "dish_author","dish_views","dish_upvotes","dish_prep_time","dish_required_skill", "dish_origin_cuisine", "category_name"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)
            