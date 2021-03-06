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


# -------------------------------------------------------------------- CONFIG #
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# ----------------------------------- HOME PAGE, MOVIE PAGE AND LEAVE REVIEWS #
# Main page
@app.route("/")
@app.route("/get_movies")
def get_movies():
    movies = mongo.db.movies.find()

    return render_template("movies.html", movies=movies)


# Displays movie. Shows and leaves reviews
@app.route("/display_movie/<movie_id>", methods=["GET", "POST"])
def display_movie(movie_id):

    # Displays information about that movie
    movie_element = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})

    # movie id doesn't exist, show 404 error
    if not movie_element:
        return render_template("404.html")

    if movie_element:
        reviews = list(mongo.db.reviews.find(
            {"movie_name": movie_element}))

    # Leaves a review about that movie
    if request.method == "POST":

        # Only users can add reviews
        if not session.get("user"):
            return render_template("404.html")

        new_review = {
            "movie_name": movie_element,
            "user_review": request.form.get("user_review"),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(new_review)
        flash("Review Successfully Added")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("display_movie.html", movie_id=movie_id,
                           reviews=reviews, movie=movie)


# --------------------------------------------------- EDIT AND DELETE REVIEWS #

# Edit existing review
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):

    # Only users can edit reviews
    if not session.get("user"):
        return render_template("404.html")

    if request.method == "POST":
        update = {
            "$set": {"user_review": request.form.get("user_review")}
            }
        mongo.db.reviews.update_one({"_id": ObjectId(review_id)}, update)
        flash("Review Successfully Updated")
        return redirect(url_for("profile", username=session['user']))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("edit_review.html", review=review)


# Delete existing review
@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review has been deleted")
    return redirect(url_for("get_movies"))


# -------------------------------------------------------------------- SEARCH #

# SEARCH FOR MOVIES
@app.route("/search_movie", methods=["GET", "POST"])
def search_movie():
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("search_movie.html", movies=movies)


# ------------------------------------------------ REGISTER, LOGIN AND LOGOUT #

# Register
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


# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
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


# User's profile and display user's reviews
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Only users can acces profile
    if not session.get("user"):
        return render_template("404.html")

    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    reviews = list(mongo.db.reviews.find(
        {"created_by": session["user"]}))

    if session["user"]:
        return render_template("profile.html", username=username,
                               reviews=reviews)

    return redirect(url_for("login"))


# Log out
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    # where to redirect after logout (to login again or main page?)
    return redirect(url_for("login"))


# ------------------------------------------- ADMIN: ADD, EDIT, DELETE MOVIES #

# Add a new movie to database
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    # Only admin can add movies
    if not session.get("user") == "admin":
        return render_template("404.html")

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


# Edit existing movie
@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    # Only admin can edit movies
    if not session.get("user") == "admin":
        return render_template("404.html")

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
            "created_by": session["user"],
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, submit)
        flash("Movie Successfully Updated")
        return redirect(url_for("get_movies"))

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("edit_movie.html", movie=movie)


# Delete movie
@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Successfully Deleted")
    return redirect(url_for("get_movies"))


# ------------------------------------------------------------ ERROR HANDLERS #
@app.errorhandler(404)
def not_found(e):
    return render_template("error_handlers/404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error_handlers/500.html"), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template("error_handlers/403.html"), 403


# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
