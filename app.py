import os, requests, re, itertools
from functools import wraps
import hashlib
from flask import Flask, flash, redirect, render_template, request, session, url_for
from bs4 import BeautifulSoup

import config
from utils import OCR, Database

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_PATH'] = config.UPLOAD_PATH
ALLOWED_EMAILS=['peter@gmail.com','paul@gmail.com']


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


@app.route("/product_rec")
def product_rec():
    return render_template("product_rec.html")


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


@app.route("/power_consumption")
def power_consumption():
    if session.get("kwh"):
        data = {"kwh": session["kwh"]}
        return render_template("power_consumption.html", data=data)
    return render_template("power_consumption.html")

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
    # product_details = re.findall(r'<div class=\"label\">(.|\n)+<div class=\"value\">.+>',r.text)
    # with open('blob.txt', 'w', errors='ignore') as f: f.write(r.text)

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

    labels_tmp = []
    values_tmp = []
    for item in items:
        for divs in item:
            labels_tmp.append(divs.find_all('div', {'class':'label'}))
            values_tmp.append(divs.find_all('div', {'class':'value'}))
    labels = []
    values = []
    for i in labels_tmp:
        if i:
            tmp = []
            for a in i:
                res = re.findall(r'>(.*?)<',str(a))[0]
                tmp.append(res)
            labels.append(tmp)

    for i in values_tmp:
        if i:
            tmp = []
            for a in i:
                res = a.string
                print(res)
                # res = re.findall(r'>(.*?)<',str(a))[0]
                tmp.append(res)
            values.append(tmp)
    labels = list(itertools.chain.from_iterable(labels))
    values = list(itertools.chain.from_iterable(values))
    print(labels)
    print(values)

    # print([label.string for label in labels])
    # print([value.string for value in values])

    # details_label = [i.find_all("div", {"class":"label"}) for i in product_details]
    # details_value = [i.find_all("div", {"class":"value"}) for i in product_details]
    # print(details_label)
    # detail_value = [i.string for i in details_value]
    # print(detail_value)
    product_names = [re.findall(r'[a-zA-Z0-9].+[a-zA-Z0-9]',i.a.string) for i in product_elements][:5]
    energy_star_url = "https://www.energystar.gov"
    product_urls = [energy_star_url + endpoint for endpoint in re.findall(r"/productfinder/.+\d+", str(product_elements))[:5]]
    # product_ids = re.findall(r"\d+", str(results))
    return render_template("product_list.html", product=prod, product_names=product_names, product_urls=product_urls)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


from Mark_Features import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8880, debug=True)
