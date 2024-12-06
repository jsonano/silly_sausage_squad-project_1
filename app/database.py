import sqlite3

db_filename = "apis.db"

def create_db():
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    # USER LOGIN TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL
    );
    ''')

    # API REQUEST/RESPONSE TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS apis (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_name TEXT NOT NULL,
        request TEXT NOT NULL,
        response TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES logins(id) ON DELETE CASCADE
    );
    ''')
    db.commit()
    db.close()

def add_user(username, password_hash):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    try:
        c.execute("INSERT INTO logins (username, password_hash) VALUES (?, ?)", (username, password_hash))
    except:
        print("Username already exists.")
    db.commit()
    db.close()

def return_user(user):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    try:
        c.execute("SELECT * FROM logins WHERE username=:username", {"username": user})
        user_info = c.fetchone()
    except:
        print("Username does not exist.")
        user_info = None
    db.close()
    return user_info
    
def add_api_request(api_name, request, response):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    try:
        c.execute("INSERT INTO apis (api_name, request, response) VALUES (?, ?, ?)", (api_name, request, response))
    except:
        print("Error adding API request.")
    db.commit()
    db.close()
    
def return_api_request(api_name): # not functional
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    try:
        c.execute("SELECT * FROM apis WHERE api_name=:api_name", {"api_name": api_name})
        info = c.fetchone()
        print(info)
        db.commit()
    except:
        print("API request does not exist.")
    db.close()


def testing():
    create_db()
    add_user("admin", "password")
    add_user("jason", "chao")
    add_user("alex", "luo")
    return_user("admin")
    return_user("jason")
    return_user("alex")
    return_user("error")
    add_api_request("weather", "GET", "Sunny")
    add_api_request("weather", "POST", "Rainy")
    add_api_request("weather", "GET", "Cloudy")
    return_api_request("weather")
    
# testing()