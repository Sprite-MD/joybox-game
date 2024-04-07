import sqlite3
from flask import Flask, request, jsonify, g, render_template, redirect, url_for, flash
import hashlib

DATABASE =  'database.db'
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def hello_world():
    return "hello"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/box")
def box():
# You can initialize the counter value and total value here
    counter_value = 0
    total_value = 0
    speedCost = 10
    
    # Render the counter.html template, passing the counter and total values
    return render_template('box.html', counter=counter_value, total=total_value, speedUpCost=speedCost)

if __name__ == "__main__":
    app.run(debug=True)
