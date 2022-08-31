import os

from flask import Flask, flash, render_template

import config
from utils import Login

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# add routes here

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
