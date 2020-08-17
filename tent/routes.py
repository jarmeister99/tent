from tent import app
from tent.grabber import access_api
from flask import url_for, redirect


@app.route('/')
def index():
    return '<h1>Hello world!</h1>'


@app.route('/fill_db')
@app.route('/fill_db/')
def fill_db():
    test = access_api(limit=5)
    return redirect(url_for('index'))
