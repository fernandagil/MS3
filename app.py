import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_movies")
def get_movies():
    movies = mongo.db.movies.find()

    return render_template("movies.html", movies=movies)


@app.route("/display_movie/<movie_id>", methods=["GET", "POST"])
def display_movie(movie_id):

    # Display information about that movie
    movie_element = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})

    if movie_element["movie_name"]:
        reviews = list(mongo.db.reviews.find(
            {"movie_name": movie_element["movie_name"]}))

    # Leave a review about that movie
    if request.method == "POST":
        new_review = {
            "movie_name": movie_element,
            "user_review": request.form.get("user_review"),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(new_review)
        flash("Review Successfully Added")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("display_movie.html", movie_id=movie_id, reviews=reviews, movie=movie) #does this just reload movie page with new review??


@app.route("/search_movie", methods=["GET", "POST"])
def search_movie():
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("search_movie.html", movies=movies)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    # where to redirect after logout (to login again or main page?)
    return redirect(url_for("get_movies")) 


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie = {
            "movie_name": request.form.get("movie_name"),
            "year": request.form.get("year"),
            "genre": request.form.get("genre"),
            "director": request.form.get("director"),
            "main_cast": request.form.get("main_cast"),
            "trailer": request.form.get("trailer"),
            "movie_img_link": request.form.get("movie_img_link"),
            "synopsis": request.form.get("synopsis"),
            "created_by": session["user"],
        }
        mongo.db.movies.insert_one(movie)
        flash("Movie Successfully Added")
        return redirect(url_for("get_movies"))

    return render_template("add_movie.html")


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
        submit = {
            "movie_name": request.form.get("movie_name"),
            "year": request.form.get("year"),
            "genre": request.form.get("genre"),
            "director": request.form.get("director"),
            "main_cast": request.form.get("main_cast"),
            "trailer": request.form.get("trailer"),
            "movie_img_link": request.form.get("movie_img_link"),
            "synopsis": request.form.get("synopsis"),
            "watchlist": request.form.get("watchlist"),
            "review": request.form.get("review"),
            "created_by": session["user"],
            # "created_when": session["date"] ???
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, submit)
        flash("Movie Successfully Updated")
        return redirect(url_for("get_movies"))

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("edit_movie.html", movie=movie)


@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Successfully Deleted")
    return redirect(url_for("get_movies"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
