#Cook book

This project focuses on helping users in finding a cooking recipe and gives them the ability to present their recipes


I have written this project in HTML, CSS, Python (3), and I have used Bootstrap for scalability and design.

# TECH USED

HTML    - HTML has been used to create markup

CSS    - CSS has been used to style my content

Python  - Python3 has been used in writing the project's logic and functionality including but not limited to (matplotlib- for displaying statistical charts, NumPy for support with csv data, 
      pprint:- pprint: does not have an active role in the final version of this project yet I found it very helpful throughout the development process [see more here: https://docs.python.org/3.6/library/pprint.html],
      )

Flask (and its components)   - the project relies on flask framework and its components ( pandas- to export data from DB to CSV file, wtforfm - for form validation, paginate- for pagination, 
                  flask_pymongo- to connect flask and MongoDB  ) 
MongoDB - MongoDB has been used to store and serve data as necessary

BOOTSTRAP    - Bootstrap has been used for responsiveness and help style elements 

GIT / GITHUB     - used for version control and code backup 

Heroku - Used For Deployment 


#Validators
- pep8 for python code indentation the code passes with no errors
- css code passes trough w3schools jigsaw with no errors 
-html code does not pass trough validator due to jinja   
# UX

This Website is for anyone searching for recipes and/or are looking to showcase their culinary skills

As a Visitor looking for recipes:
     - I would like to have a self-explaining initial contact with the webpage 
    - I would like to see products arranged based on relevance
    - I would like to be able to control what items are displayed
    - I would like some brief characteristics of the item before to help me decide if the item is worth visiting 
    - I would like to see all available characteristics of a certain item upon the decision to do so 
    - I would like a page for best-rated items 
    - I would like to be able to provide feedback for recipes I like 

As a visitor looking to showcase my recipes
    - I would like a clear easy to follow the process to allow me to add a new recipe
    - I would like to upload a photo of my recipe
    - I would like to highlight the main characteristics of my recipe
    - in case I make a mistake or I come up with a better version of the current recipe I would like to be able to make alterations to the original item 
    - I would also like to be able to remove a recipe from the website 


# Features

    This Web Application currently offers the following features 
- a home page displaying recipes based on their feedback(likes)
- controls allowing the user to navigate through the website 
- filtering system allowing users to choose what category they would like to see 
- one page for top 10 recipes based on their feedback (likes)
- possibility of adding a new recipe 
- possibility of modifying an existing recipe
- possibility of removing an existing recipe 
- feedback functionality (likes and views)
- statistics page providing a graphical representation of data 
- pagination - only 9 results are displayed per page 
- wireframe of the project can be found in static/wireframes/




# Features Left To Implement
-user authentication 
- file update 
-user restrictions (only the person who uploaded the recipe  will be able to edit or delete it)
-feedback - only 1 like and/or view per user 
-prevent likes and views from resetting to 0 when changes are made to the recipe 



# TESTING

- Extensive testing has been carried out at the time of implementation for each new piece of functionality
- testing has been carried out on all major browsers and some mobile devices
- usability test has been carried out by friends and family 
- the website renders accordingly on all screen sizes down to 360px

# Individual Feature Testing 
- CREATE READ UPDATE DELETE (CRUD) - works as intended without displaying any errors or warnings 
- Filtering based on items feedback works as intended with no errors 
-feedback functionality works as intended (yet some alterations will be made)
- pagination works as intended displaying clear visual clues helping the user to navigate through pages 
- filtering recipes based on their attributes (category) works as intended not showing any errors 
- layout - the website looks as intended bot on desktop and mobile devices 
- statistics work as intended using the latest data available 


# UI

Design of his website has been made to provide end-user with an intuitive easy to follow  process of inserting displaying modifying or removing 
recipes from database 

 
    
# Deployment
The code's version control has been handled by git and backed up by GitHub 
The project has been deployed on Heroku following documentation and adding necessary modifications to the code (configuration variables)
############
The deployed version of this code can be found  at (https://flask-cook-book.herokuapp.com/)
-The repository can be found on GitHub at (https://github.com/toderas/Flask-Cook-Book)
############



##### Acknowledgements ####

I have received inspiration from Corey Schafer and its flask blog tutorial (https://www.youtube.com/watch?v=MwZwr5Tvyxo)
Stack Overflow for code related issues 
Fiends And Family for usability tests 
Antonija Simic (Mentor) for her continuous support and patience throughout this project!
