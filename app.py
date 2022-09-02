import hashlib
import os
import re
import sqlite3 as sql
from functools import wraps

import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, session, url_for

import config
from utils import OCR, Database

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_PATH'] = config.UPLOAD_PATH
ALLOWED_EMAILS=['peter@gmail.com','paul@gmail.com']

if config.ENV == "live":
    os.system("sqlite3 database/energyclash.db < database/energyclash.sql")

conn = sql.connect(config.DB_PATH)
cur = conn.cursor()
cur.execute("SELECT season, data FROM mapdata")
MAPDATARAW = cur.fetchall()
conn.close()

MAP_DICT = eval(MAPDATARAW[0][1])

conn = sql.connect(config.DB_PATH)
cur = conn.cursor()
cur.execute("SELECT season, data FROM powerdata")
pdr = cur.fetchall()
conn.close()

POWER_DICT = eval(pdr[0][1])


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
    session.pop("kwh", None)
    return render_template("index.html")


@app.route("/product_rec")
def product_rec():
    return render_template("product_rec.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


# add routes here
@app.route("/login", methods=("GET", "POST"))
def login():
    session.pop("kwh", None)
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password = hashlib.md5(bytes(password,'utf-8')).hexdigest()
        if Database().validate(name, password):
            session["logged_in"] = True
            session["name"] = name
            session["district"] = "ANG MO KIO"
            flash("Successfully logged into EnergyClash", "success")
            return redirect("/")
        flash("Incorrect login credentials", "danger")
    return render_template("login.html")


ACTIVE_DISTRICT = ''
@app.route("/register", methods=("GET", "POST"))
def register():
    session.pop("kwh", None)
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
            session["district"] = config.user_district
            flash("Thank you for signing up for EnergyClash", "success")
            return redirect("/")
        except Exception as e:
            flash("Error while creating new user", "danger")
    return render_template("register.html")


@app.route("/prizes")
def prizes():
    flash("Check out the <a href='/map'>GAMEMAP</a> to see how close your district is! ", "warning")
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
            MAP_DICT[session["district"]]+=round(POWER_DICT['July'] - float(kwh),2)
            return render_template("upload_bill.html", data=data)
        flash("Cannot extract electricity consumption", "warning")
    return render_template("upload_bill.html")


@app.route("/power_consumption")
@logged_in
def power_consumption():
    if session.get("kwh"):
        data = {"kwh": session["kwh"]}
        flash("Check out the <a href='/map'>GAMEMAP</a> to see how close your district is! ", "warning")
        return render_template("power_consumption.html", data=data, power_dict=POWER_DICT)
    flash("Check out <a href='/product_rec'>RECOMMENDED PRODUCTS</a> for great energy-saving appliances that reduce energy usage! ", "warning")
    return render_template("power_consumption.html", power_dict=POWER_DICT)


@app.route("/product_rec/<product>")
def product(product):
    products = {
        "refrigerators": "refrigerators",
        "computer_monitors": "computer-monitors",
        "washing_machines": "clothes-washers",
        "dehumidifiers": "dehumidifiers",
        "acs": "room-ac"
    }
    if product not in products.keys():
        return render_template("404.html"), 404
    prod = products[product]
    product_url = f"https://www.energystar.gov/most-efficient/me-certified-{prod}/results?is_most_efficient_filter=Most+Efficient"
    r = requests.get(product_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    product_elements = soup.find_all("div", {"class": "title"})

    product_details = []
    for item in soup.find_all('div', class_="field"):
        if item.a is None:
            product_details.append(item.parent.parent)
    product_details = product_details[:5]

    items = []
    for item in product_details:
        buf = item.findChildren("div", recursive=False)[1:]
        dets = []
        for i in buf:
            if "CLICK FOR PRODUCT DETAILS" in str(i):
                break
            else:
                dets.append(i)
        items.append(dets)

    if product == 'computer_monitors':
        energy_string = 'Total Energy Consumption'
    elif product == 'dehumidifiers':
        energy_string = 'Dehumidifier Efficiency (Integrated Energy Factor - L/kWh)'
    else:
        energy_string = 'Annual Energy Use (kWh/yr)'
    energy_values = []
    tmp = r.text.split('\n')
    for i in range(len(tmp)):
        if energy_string in tmp[i]:
            try:
                if product == 'acs':
                    value = re.findall(r'\d+[.\d+]*', tmp[i + 2])[0]
                else:
                    value = re.findall(r'\d+[.\d+]*',tmp[i+1])[0]
                energy_values.append(value)
            except Exception:
                continue
    energy_values = energy_values[:5]

    product_names = [re.findall(r'[a-zA-Z0-9].+[a-zA-Z0-9]',i.a.string) for i in product_elements][:5]
    energy_star_url = "https://www.energystar.gov"
    product_urls = [energy_star_url + endpoint for endpoint in re.findall(r"/productfinder/.+\d+", str(product_elements))[:5]]
    return render_template("product_list.html", label_name=energy_string,energy_values=energy_values,product=prod, product_names=product_names, product_urls=product_urls)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


from Mark_Features import *

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
