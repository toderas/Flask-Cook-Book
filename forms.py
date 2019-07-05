from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class AddRecipeForm(FlaskForm):
    dish_author = StringField('Author',
                           validators=[DataRequired(), Length(min=10, max=20)])
    dish_prep_time = IntegerField('Prep Time',
                        validators=[DataRequired(), Length(min=1, max=3)])
    
    submit = SubmitField('Add Recipe')
