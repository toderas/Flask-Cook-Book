from flask import Flask, request
from flask_pymongo import PyMongo, pymongo
import csv

app = Flask(__name__)




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
        fields = ["dish_name", "dish_author", "dish_prep_time", "dish_origin_cuisine","dish_upvotes", "category_name", "country", "dish_views", "dish_required_skill"]
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for x in cursor:
            writer.writerow(x)