from flask import request, flash, session
import sqlite3
import os
import json
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
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    ''')

    # API REQUEST/RESPONSE TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS apis (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_request TEXT,
        request_type TEXT,
        response TEXT,
        user_id INTEGER,
        img_file BLOB DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES logins(id) ON DELETE CASCADE
    );
    ''')
    # requests are not required, only used if user inputs an image URL
    # API response will be a dictionary containing all three APIs responses
    conn.commit()
    conn.close()

def add_user(user, password):
    create_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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

# Logs in user if username and password match
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        # Retrieve hashed password for the given username
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user_password_hash = cur.fetchone()
        conn.close()

        # Checks hashed user password against database
        if user_password_hash and check_password_hash(user_password_hash['password_hash'], password):
            session['username'] = username
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password!', 'error')

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

def add_api_request(username, user_request, request_type, response, img_file_bytes=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cur.fetchone()[0]
    # if img_file_bytes == None:
    #     cur.execute("INSERT INTO apis (user_request, request_type, response, user_id) VALUES (?, ?, ?, ?)", (user_request, request_type, response, user_id))
    # else:
    cur.execute("INSERT INTO apis (user_request, request_type, response, user_id, img_file) VALUES (?, ?, ?, ?, ?)", (user_request, request_type, response, user_id, img_file_bytes))
    conn.commit()
    conn.close()

def return_api_request(username): # returns all api requests under the same user
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cur.fetchone()[0]
        #user = cur.fetchone()
        #if not user:
        #     return []
        #user_id = user["user_id"]
        cur.execute("SELECT * FROM apis WHERE user_id = ?", (user_id,))
        #requests = cur.fetchall()
        #return requests
    #except Exception as e:
        #print("Error Fetching API Requests:", e)
        #return []
    #finally:
         #conn.close()

        conn.commit()
        
        requests = []
        for row in cur.fetchall():
            row_info = []
            row_info.append(row[2])             # 0 
            response_dict = json.loads(row[3])
            row_info.append(response_dict["unsplash"]) # 1
            row_info.append(response_dict["clarifai"]) # 2
            row_info.append(response_dict["pixabay"])  # 3
            if (row[5] != None):
                row_info.append(row[5])         # 4
            else:
                row_info.append(None)
            requests.append(row_info)
            # print(row_info)
        return requests
    except:
        print("API request does not exist.")
    finally:
        conn.close()
