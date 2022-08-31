import sys
from flask import Flask, Response, render_template, request, redirect, url_for, make_response
from app import *
MARK_TOKEN = 'Mark is Awesome.' #not required, used to test importing.


#WARNING: Only Yishun, Sembawang, and Ang Mo Kio have valid coordinates on the client, so the top 3 must be one of these towns.

MAP_DICT = {
"YISHUN":12401,
"ANG MO KIO":11933,
"SERANGOON":1255,
"TOA PAYOH":1303,
"BISHAN":5504,
"SIMPANG":9311,
"SUNGEI KADUT":2350,
"BUKIT PANJANG":9265,
"CHOA CHU KANG":6321,
"TENGAH":3259,
"JURONG WEST":9742,
"WESTERN WATER CATCHMENT":3251,
"JURONG EAST":4522,
"CLEMENTI":4570,
"BUKIT TIMAH":4329,
"TANGLIN":7624,
"CENTRAL AREA":3265,
"KALLANG":3880,
"MARINE PARADE":3363,
"BEDOK":3531,
"TAMPINES":3643,
"CHANGI":8242,
"MANDAI":3412,
"NOVENA":8953,
"LIM CHU KANG":1232,
"SEMBAWANG":10322,
"WOODLANDS":8554,
"PAYA LEBAR":6532,
"HOUGANG":4302,
"PASIR RIS":2003,
"SENGKANG":7991,
"PUNGGOL":5002,
"SELETAR":1054,
"BUKIT BATOK":5521,
"TUAS":3002,
"GEYLANG":6969,
"QUEENSTOWN":8871,
"BUKIT MERAH":3419,
"CENTRAL WATER CATCHMENT":920,
"WESTERN ISLANDS":2300,
"NORTH-EASTERN ISLANDS":1022,
"SOUTHERN ISLANDS":2355,

}

@app.route('/map', methods=['GET'])
def map():
    if request.method=='GET':
        print('getting map',file=sys.stderr)
        MapJsVars = ''
        for i in MAP_DICT.keys():
            MapJsVars += f'"{i}": {MAP_DICT.get(i)},'
        winners=sorted(MAP_DICT, key=MAP_DICT.get, reverse=True)[:3]
        return render_template('map.html',MapJsVars=MapJsVars,winners=winners)



