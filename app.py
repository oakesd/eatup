import os
import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, session, url_for, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address

# Configuration for Flask app
app = Flask(__name__, template_folder="./templates")
app.debug = True

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/eatup.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '0-Tv)zlbq1t,{6^I~:%By!<8=C\'2&sF2gD:$2V>+qM-u*;uVJg!$`Vdw-&a\'Y[,'

# Instantiate CSRF
csrf = CSRFProtect()

# Instantiate SQLAlchemy
db = SQLAlchemy(app)

# Instantiate Bcrypt
bcrypt = Bcrypt(app)

# Instantiate LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize CSRF app
csrf.init_app(app)

#to limit login attempts
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
  )


# Data models

# User class required for flask_login; mapped to user table in eatup.db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    created = db.Column(db.Text)


# Mapped to recipes table in eatup.db
class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    cuisine_id = db.Column(db.Integer)
    diet_id = db.Column(db.Integer)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    wait_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    image_path = db.Column(db.Text)
    created = db.Column(db.Text)


# Mapped to recipe_list view in eatup.db
class RecipeList(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    cuisine_id = db.Column(db.Integer)
    cuisine = db.Column(db.Text)
    diet_id = db.Column(db.Integer)
    diet = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    wait_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    image_path = db.Column(db.Text)


# Mapped to last_five view in eatup.db
class LastFive(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.Text)
    diet = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    wait_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    image_path = db.Column(db.Text)


# Mapped to cuisines table in eatup.db
class CuisineList(db.Model):
    cuisine_id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.Text)


# Mapped to diets table in eatup.db
class DietList(db.Model):
    diet_id = db.Column(db.Integer, primary_key=True)
    diet = db.Column(db.Text)


# Helper Methods
def format(data):
    """
    extracts number from the string passed as parameter
    """
    data = str(data).replace("<", "").replace(">", "")
    num = [int(x) for x in data.split() if x.isdigit()]
    return num[0]


def handle_upload(data):
    """
    saves the uploaded image to the local storage and returns a formatted image path
    """
    # Code to handle picture upload
    assets_dir = os.path.join(os.path.dirname(app.instance_path), 'static/img')
    filename = secure_filename(data.filename)
    data.save(os.path.join(assets_dir, filename))
    image_path = "img/" + filename
    return image_path


def get_diets():
    return DietList.query.all()


def get_cuisines():
    return CuisineList.query.all()


# function to get user by id
@login_manager.user_loader
def load_user(user_id):
    '''to load user'''
    return User.query.get(int(user_id))


@app.route("/")
def home():
    """
    home function for site
    """
    #session = db.create_scoped_session(options = {'bind': 'recipedb'})
    l5 = LastFive.query.all()
    return render_template('index.html', recent=l5)


@app.route("/recipe_upload", methods=['get', 'post'])
@login_required
def recipe_upload():
    """
    recipe function for site
    """
    # Import Recipe Submission Form
    from recipe_submit_form import RecipeSubmitFrom

    # Initialize form
    form = RecipeSubmitFrom()

    # Check to see if the recipe already exists
    does_recipe_exist = db.session.query(Recipes.recipe_id).filter_by(
        title=form.recipe_name.data).scalar() is not None

    if form.validate_on_submit():
        # Validate the recipe submission form
        recipe_name = form.recipe_name.data
        cuisine_type = form.cuisine_type.data
        diet_type = form.diet_type.data
        prep_time = form.prep_time.data
        cook_time = form.cook_time.data
        wait_time = form.wait_time.data
        servings = form.servings.data
        img_upload = form.image_upload.data
        desc = form.desc.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data

        new_recipe = Recipes(
            title=recipe_name,
            cuisine_id=format(diet_type),
            diet_id=format(cuisine_type),
            description=desc,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            wait_time=wait_time,
            servings=servings
        )

        # Save new recipe to the DB - uncomment when you're ready to save to DB after changes have been reviewed by Team Lead
        try:
            if does_recipe_exist is False:
                # Add image only if new recipe doesn't exist
                new_recipe.image_path = handle_upload(img_upload)
                db.session.add(new_recipe)
                db.session.commit()
                print("\nData received. Now redirecting ...")
                flash("Recipe was added successfully!", "success")
                return redirect(url_for('recipe_upload'))
            else:
                flash("Recipe with this name already exists!!", "error")
                return render_template('recipe_upload.html', form=form)
        except:
            flash("Internal Error!", "error")

    if not form.validate_on_submit() and bool(form.errors):
        flash(form.errors, "error")
    return render_template('recipe_upload.html', form=form)


@app.route("/recipe_list", methods=['GET', 'POST'])
def recipe_list():
    """
    recipe list for site
    """
    from recipe_filter_form import RecipeFilterForm

    form = RecipeFilterForm()

    if request.method == 'GET':
        recipeList = RecipeList.query.all()
    else:
        cuisine = request.form.get('cuisine_type', 0)
        diet = request.form.get('diet_type', 0)

        if (cuisine != '0' and diet == '0'):
            recipeList = RecipeList.query.filter(RecipeList.cuisine_id == cuisine).all()
        elif (cuisine == '0' and diet != '0'):
            recipeList = RecipeList.query.filter(RecipeList.diet_id == diet).all()
        elif (cuisine != '0' and diet != '0'):
            recipeList = RecipeList.query.filter(RecipeList.cuisine_id == cuisine, RecipeList.diet_id == diet).all()
        else:
            recipeList = RecipeList.query.all()

    sub_list = [recipeList[x:x+3] for x in range(0, len(recipeList), 3)]
    return render_template('recipe_list.html', form=form, list=sub_list)


@app.route("/recipe")
def recipe():
    """
    Recipe page
    """
    id = request.args.get('recipe_id', None)
    recipe_record = RecipeList.query.get(id)
    ingredient_list = str(recipe_record.ingredients).split(',')

    return render_template('recipe.html',
                           recipe=recipe_record,
                           ingredients=ingredient_list)


# URL "/login" to be handled by login() route handler
@app.route("/signin", methods=['get', 'post'])
@limiter.limit("100/day;10/hour;3/minute")
def login():
    """
    To login to website and see other pages
    """

    # Import Recipe Submission Form
    from forms import LoginForm

    # Init log in form
    form = LoginForm()

    # Redirects user to home page if already signed in.
    if current_user.is_authenticated:
        return redirect(url_for('recipe_upload'))

    error = None

    # Log failed attempts with ip address, date and time
    ip_address = request.environ['REMOTE_ADDR']
    now = datetime.datetime.now()
    time_stamp = now.strftime("%m-%d-%Y  %H:%M")

    # if request.method == "POST":
    if form.validate_on_submit():
        # Validate log in form
        username = form.username.data
        password = form.password.data

        # Query database to check that username exists and store in variable user
        user = User.query.filter_by(username=username).first()

        # Checks user exists and that there password is verified in database
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You are now logged in!!', 'success')
            return redirect(url_for('recipe_upload'))

        error = 'Login Unsuccessful. Check username and password'

        # Log failed attempts with ip address, date and time
        ip_address = request.environ['REMOTE_ADDR']
        now = datetime.datetime.now()
        now = now.strftime("%m-%d-%Y  %H:%M")

        # Updating list to log failed attempts
        with open('failed_log.txt', mode='a') as failed_log:
            failed_log.write(username + '   ' + ip_address + '   ' + time_stamp + '\n')
        flash(error, "error")
        return render_template('login.html', form=form)

    return render_template('login.html', form=form, error=error)


@app.route("/logout")
def logout():
    '''logout user'''
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
