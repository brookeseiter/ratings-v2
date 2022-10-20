"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title = movie.get('title')
    overview = movie.get('overview')
    poster_path = movie.get('poster_path')

    release_date = movie.get('release_date')
    format = "%Y-%m-%d"
    release_date = datetime.strptime(release_date, format)
    #or just: release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)

    random_movie = choice(movies_in_db)
    random_score = randint(1, 5)

    rating = crud.create_rating(user, random_movie, random_score)

    model.db.session.add(user, rating)

model.db.session.commit()
    #db_movie only for movies and not user/ratings bc we're randomly
    #generating these and the movies come in the json file


# alt for loop:
#    for movie in movie_data:
#     title, overview, poster_path = (
#         movie["title"],
#         movie["overview"],
#         movie["poster_path"],
#     )