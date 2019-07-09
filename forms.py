from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange


class AddRecipeForm(FlaskForm):
    dish_name = StringField('Name',
                            validators=[DataRequired(), Length(min=3, max=100)])
    dish_author = StringField('Author',
                           validators=[DataRequired(), Length(min=3, max=30)])
    dish_origin_cuisine = StringField('Country Of Origin',
                                      validators=[DataRequired(), Length(min=2, max=10)])
    dish_prep_time = IntegerField('Estimated Preparation time (in minutes)',
                                  validators=[DataRequired(), NumberRange(0,999)])
    dish_ingredients = StringField('Ingredients',
                                      validators=[DataRequired(), Length(min=2)])
    dish_preparation_steps = StringField('Recommended Steps',
                                      validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Add Recipe')
    
class EditRecipeForm(FlaskForm):
    dish_name = StringField('Name',
                            validators=[DataRequired(), Length(min=3, max=100)])
    dish_author = StringField('Author',
                           validators=[DataRequired(), Length(min=3, max=30)])
    dish_origin_cuisine = StringField('Country Of Origin',
                                      validators=[DataRequired(), Length(min=2, max=10)])
    dish_prep_time = IntegerField('Estimated Preparation time (in minutes)',
                                  validators=[DataRequired(), NumberRange(0,999)])
    dish_ingredients = StringField('Ingredients',
                                      validators=[DataRequired(), Length(min=2)])
    dish_preparation_steps = StringField('Recommended Steps',
                                      validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Update Recipe')