import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import config
from utils import Login

app = Flask(__name__)
app.secret_key = os.urandom(24)


# checks if user is logged in.
def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            flash("Login to view this page", "warning")
            return redirect(url_for("login"))
    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/hosting")
def hosting():
    return render_template("hosting.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/blog-details")
def blog_details():
    return render_template("blog-details.html")


@app.route("/contact")
@logged_in
def contact():
    return render_template("contact.html")


# add routes here
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if Login().validate(name, password):
            session["logged_in"] = True
            flash("Successfully logged into EnergyClash", "success")
            return redirect("/")
        flash("Incorrect login credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        try:
            Login().insert_user(name, password)
            session["logged_in"] = True
            flash("Thank you for signing up for EnergyClash", "success")
            return redirect("/")
        except Exception as e:
            print(e)
            flash("Error while creating new user", "danger")
    return render_template("register.html")


@app.route("/prizes")
def prizes():
    return render_template("prizes.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
