from flask import render_template, request

from app import *

MARK_TOKEN = 'Mark is Awesome.' #not required, used to test importing.

# WARNING: Only Yishun, Sembawang, and Ang Mo Kio have valid coordinates on the client, so the top 3 must be one of these towns.

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
        session["kwh"] = 431.0
    MAP_DICT[session["district"]]+=round(POWER_DICT['July'] - float(431.0),2)
    flash(f'Debug 431 kW/H for {session["district"]}', "warning")
    return render_template("index.html")
