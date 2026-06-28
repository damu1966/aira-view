import os
from functools import wraps
import requests
from flask import Flask, render_template, jsonify, redirect, session, request

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-prod')

ADMIN    = 'https://airafoads.pythonanywhere.com'
APP_USER = os.environ.get('APP_USERNAME', 'aira')
APP_PASS = os.environ.get('APP_PASSWORD', 'farm2024')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == APP_USER and \
           request.form.get('password') == APP_PASS:
            session['logged_in'] = True
            return redirect('/')
        error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
@login_required
def index(): return render_template('index.html')

@app.route('/api/map-info')
@login_required
def map_info():
    try:
        r = requests.get(f'{ADMIN}/api/map-info', timeout=5)
        return jsonify(r.json())
    except:
        return jsonify({'width': 1241, 'height': 1754})

@app.route('/api/data')
@login_required
def get_data():
    plots  = requests.get(f'{ADMIN}/api/plots',  timeout=15).json()
    owners = requests.get(f'{ADMIN}/api/owners', timeout=15).json()
    return jsonify({'plots': plots, 'owners': owners})

@app.route('/static/uploads/<path:fn>')
@login_required
def serve_upload(fn):
    return redirect(f'{ADMIN}/static/uploads/{fn}')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
