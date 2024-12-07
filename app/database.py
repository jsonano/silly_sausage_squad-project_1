from flask import request, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Database path setup
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'apis.db')

# connext to database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So I can access dictionary items using their column name instead of indexing
    return conn

def create_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # USER LOGIN TABLE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')

    # API REQUEST/RESPONSE TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS apis (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_name TEXT NOT NULL,
        request DEFAULT NULL,
        response TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES logins(id) ON DELETE CASCADE
    );
    ''')
    conn.commit()
    conn.close()

def add_user(user, password):
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
        pw_hash = generate_password_hash(password)
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Insert new user into the database
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (user, pw_hash,))
            conn.commit()
            # flash('Registration successful!', 'success')
        # except sqlite3.IntegrityError:
        #     flash('Username already exists!', 'error')
        finally:
            conn.close()
            
# def login_user():
#      if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = get_db_connection()
#         cur = conn.cursor()
#         # Retrieve hashed password for the given username
#         cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
#         user_password_hash = cur.fetchone()
#         conn.close()

#         # Checks hashed user password against database
#         if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
#             session['username'] = username
#             flash('Login successful!', 'success')
#         else:
#             flash('Invalid username or password!', 'error')

def return_user(user):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE username=?", (user,))
        user_info = cur.fetchone()
    except:
        print("Username does not exist.")
        user_info = None
    finally:
        conn.close()
        return user_info
    
def add_api_request(username, api_name, request, response):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO apis (api_name, request, response, user_id) VALUES (?, ?, ?, ?)", (api_name, request, response, user_id))
    conn.commit()
    conn.close()
    
def return_api_request(api_name): # returns all api requests with the same name
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM apis WHERE api_name = ?", (api_name,))
        for row in cur.fetchall():
            print(row)
        print(cur.fetchall())
        conn.commit()
    except:
        print("API request does not exist.")
    conn.close()


def testing():
    create_db()
    add_user("admin", "password")
    add_user("jason", "chao")
    add_user("alex", "luo")
    print(return_user("admin")[0])
    print(return_user("jason")[0])
    print(return_user("alex")[0])
    print(return_user("error"))
    add_api_request("admin", "weather", "GET", "Sunny")
    add_api_request("admin", "weather", "POST", "Rainy")
    add_api_request("admin", "weather", "GET", "Cloudy")
    return_api_request("weather")
    
testing()