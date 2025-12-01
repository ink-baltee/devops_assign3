from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        INSERT OR IGNORE INTO users (username, password) VALUES ('test', 'test');
        """)
app = Flask(__name__)
app.secret_key = "change_this_secret"

@app.before_first_request
def setup():
    init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT m.id, m.message, m.created_at, u.username FROM messages m LEFT JOIN users u ON m.user_id = u.id ORDER BY m.created_at DESC')
    messages = cur.fetchall()
    return render_template('index.html', messages=messages)

@app.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
        user = cur.fetchone()
        if user:
            flash('Logged in as ' + username)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit_message():
    username = request.form.get('username', 'anonymous')
    message = request.form.get('message', '').strip()
    if not message:
        flash('Message cannot be empty', 'error')
        return redirect(url_for('index'))
    db = get_db()
    # find user id (if exists)
    cur = db.execute('SELECT id FROM users WHERE username=?', (username,))
    user = cur.fetchone()
    user_id = user['id'] if user else None
    db.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
    db.commit()
    flash('Message submitted')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
