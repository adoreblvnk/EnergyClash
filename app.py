import os
from functools import wraps
import hashlib
from flask import Flask, flash, redirect, render_template, request, session, url_for
import sqlite3 as sql
import config
from utils import OCR, Database

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_PATH'] = config.UPLOAD_PATH
ALLOWED_EMAILS=['peter@gmail.com','paul@gmail.com']

if config.ENV == "live":
    os.system("sqlite3 database/energyclash.db < database/energyclash.sql")



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
def contact():
    return render_template("contact.html")


# add routes here
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password = hashlib.md5(bytes(password,'utf-8')).hexdigest()
        if Database().validate(name, password):
            session["logged_in"] = True
            session["name"] = name
            flash("Successfully logged into EnergyClash", "success")
            return redirect("/")
        flash("Incorrect login credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form["name"]
        if name.lower() not in ALLOWED_EMAILS:
            return redirect('/')
        password = request.form["password"]
        password=hashlib.md5(bytes(password,'utf-8')).hexdigest()
        district = request.form["district"]
        try:
            Database().insert_user(name, password, district)
            session["logged_in"] = True
            session["name"] = name
            flash("Thank you for signing up for EnergyClash", "success")
            return redirect("/")
        except Exception as e:
            print(e)
            flash("Error while creating new user", "danger")
    return render_template("register.html")


@app.route("/prizes")
def prizes():
    return render_template("prizes.html")


@app.route("/upload_bill", methods=("GET", "POST"))
@logged_in
def upload_bill():
    if request.method == "POST":
        power_bill = request.files["power_bill"]
        os.makedirs(app.config["UPLOAD_PATH"], exist_ok=True)
        power_bill_path = os.path.join(app.config["UPLOAD_PATH"], power_bill.filename)
        power_bill.save(power_bill_path)
        tesseract_data = OCR().tesseract_output(power_bill_path)
        text_slice = OCR().extract_text(tesseract_data)
        kwh = OCR().extract_power_consumption(text_slice)
        session["kwh"] = kwh
        img_output_path = OCR().draw_boxes(power_bill_path, tesseract_data)
        if kwh and img_output_path:
            data = {
                "kwh": kwh,
                "img_output_path": img_output_path
            }
            return render_template("upload_bill.html", data=data)
    return render_template("upload_bill.html")



conn = sql.connect(config.DB_PATH)
cur = conn.cursor()
cur.execute("SELECT season, data FROM powerdata")
pdr = cur.fetchall()
conn.close()

POWER_DICT = eval(pdr[0][1])


@app.route("/power_consumption")
@logged_in
def power_consumption():
    if session.get("kwh"):
        data = {"kwh": session["kwh"]}
        return render_template("power_consumption.html", data=data, power_dict=POWER_DICT)
    return render_template("power_consumption.html", power_dict=POWER_DICT)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


from Mark_Features import *


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
