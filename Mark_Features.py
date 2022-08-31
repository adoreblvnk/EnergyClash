import sys
from flask import Flask, Response, render_template, request, redirect, url_for, make_response
from app import *
MARK_TOKEN = 'Mark is Awesome.' #not required, used to test importing.

MAP_DICT = {
    "YISHUN":10,
    "SEMBAWANG":50,
    "BISHAN":20,

}

@app.route('/map', methods=['GET'])
def map():
    if request.method=='GET':
        print('getting map',file=sys.stderr)
        MapJsVars = ''
        for i in MAP_DICT.keys():
            MapJsVars += f'"{i}": {MAP_DICT.get(i)},'
        return render_template('map.html',MapJsVars=MapJsVars)



