from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, IntegerField, FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, NumberRange, DataRequired
from flask_wtf.file import FileRequired, FileAllowed

from app import get_diets, get_cuisines

# Recipe Submit Form
class RecipeSubmitFrom(FlaskForm):
    recipe_name = StringField(
        label='Recipe Name', id='recipe_name',
        validators=[InputRequired(), DataRequired()])

    cuisine_type = QuerySelectField(
        query_factory=get_cuisines, allow_blank=False, get_label='cuisine', label="Cuisine Type", validators=[DataRequired()])

    diet_type = QuerySelectField(
        query_factory=get_diets, allow_blank=False, get_label='diet', label="Diet Type", validators=[DataRequired()])

    prep_time = IntegerField(
        label="Prep Time",
        validators=[DataRequired(), NumberRange(
            min=1, max=None, message='Prep time cannot be less than 1 minute')],
        description='In Minutes'
    )

    cook_time = IntegerField(
        label="Cook Time",
        validators=[DataRequired(), NumberRange(
            min=1, max=None, message='Cook time cannot be less than 1 minute')],
        description='In Minutes'
    )

    wait_time = IntegerField(
        label="Wait Time",
        validators=[DataRequired(), NumberRange(
            min=1, max=None, message='Wait time cannot be less than 1 minute')],
        description='In Minutes'
    )

    servings = IntegerField(
        label="Servings",
        validators=[DataRequired(), NumberRange(
            min=1, max=None, message='Servings cannot be less than 1')]
    )

    image_upload = FileField(
        label='Image',
        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    desc = TextAreaField(
        label="Description", id="description", validators=[DataRequired()])

    ingredients = TextAreaField(
        label="Ingredients", id="ingredients", validators=[DataRequired()])

    instructions = TextAreaField(
        label="Instructions", id="instructions", validators=[DataRequired()])
