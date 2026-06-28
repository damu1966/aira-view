import os
import requests
from flask import Flask, render_template, jsonify, redirect

app = Flask(__name__)

ADMIN = 'https://airafoads.pythonanywhere.com'

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/map-info')
def map_info():
    try:
        r = requests.get(f'{ADMIN}/api/map-info', timeout=5)
        return jsonify(r.json())
    except:
        return jsonify({'width': 1241, 'height': 1754})

@app.route('/api/data')
def get_data():
    plots  = requests.get(f'{ADMIN}/api/plots',  timeout=15).json()
    owners = requests.get(f'{ADMIN}/api/owners', timeout=15).json()
    return jsonify({'plots': plots, 'owners': owners})

@app.route('/static/uploads/<path:fn>')
def serve_upload(fn):
    return redirect(f'{ADMIN}/static/uploads/{fn}')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
