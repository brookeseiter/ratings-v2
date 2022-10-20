"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Return homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details of a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form["email"]
    password = request.form["password"]
    # or email = request.form.get("email")

    # or user = crud.get_user_by_email(email)
    # if user: (line 54)
    if crud.get_user_by_email(email):
        flash("Cannot create account with provided email. User already exists, try again.")
    else:
        new_user = crud.create_user(email, password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created succesfully, you may log in.")
        
    return redirect('/')

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details of a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
