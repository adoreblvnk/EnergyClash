import sys
from flask import Flask, Response, render_template, request, redirect, url_for, make_response
from app import *
MARK_TOKEN = 'Mark is Awesome.' #not required, used to test importing.
import sqlite3 as sql

#WARNING: Only Yishun, Sembawang, and Ang Mo Kio have valid coordinates on the client, so the top 3 must be one of these towns.



conn = sql.connect(config.DB_PATH)
cur = conn.cursor()
cur.execute("SELECT season, data FROM mapdata")
MAPDATARAW = cur.fetchall()
conn.close()

MAP_DICT = eval(MAPDATARAW[0][1])

@app.route('/map', methods=['GET'])
def map():
    if request.method=='GET':
        MapJsVars = ''
        for i in MAP_DICT.keys():
            MapJsVars += f'"{i}": {MAP_DICT.get(i)},'
        winners=sorted(MAP_DICT, key=MAP_DICT.get, reverse=True)[:5]
        flash("Season 1 of EnergyClash has started! It will run to 1st June 2023.", "success")
        return render_template('map.html',MapJsVars=MapJsVars,winners=winners)



@app.route("/api_upload_markisawesome", methods=("GET", "POST"))
@logged_in
def api_upload():
    if request.method == "GET":
        session["kwh"] = 431
    MAP_DICT[session["district"]]+=431
    flash(f'Debug 431 kW/H for {session["district"]}', "warning")
    return render_template("index.html")
