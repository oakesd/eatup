from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, IntegerField, FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, NumberRange, DataRequired
from flask_wtf.file import FileRequired, FileAllowed

from app import get_diets, get_cuisines


# Recipe Submit Form
class RecipeFilterForm(FlaskForm):

    cuisine_type = QuerySelectField(
        query_factory=get_cuisines, allow_blank=False, get_label='cuisine', label="Cuisine Type", validators=[DataRequired()])

    diet_type = QuerySelectField(
        query_factory=get_diets, allow_blank=False, get_label='diet', label="Diet Type", validators=[DataRequired()])