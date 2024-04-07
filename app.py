import sqlite3
from flask import Flask, g

DATABASE =  'database.db'
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/create_table')
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS example (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL)''')
    db.commit()
    return 'Table created successfully'

@app.route('/insert_data')
def insert_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO example (name) VALUES ('John')")
    db.commit()
    return 'Data inserted successfully'

@app.route('/select_data')
def select_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM example")
    data = cursor.fetchall()
    return str(data)


if __name__ == "__main__":
    app.run(debug=True)
    init_db()
