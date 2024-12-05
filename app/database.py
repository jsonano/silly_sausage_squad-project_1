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
        password_hash TEXT NOT NULL,
    );
    ''')

    # API REQUEST/RESPONSE TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS apis (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (user_id) REFERENCES logins(id),
        api_name TEXT NOT NULL,
        request TEXT NOT NULL,
        response TEXT,
    );
    ''')
    db.commit()
    db.close()

def add_user(username, password_hash):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    c.execute("INSERT INTO logins (username, password_hash) VALUES (?, ?)", (username, password_hash))
    db.commit()
    db.close()

def return_user(user):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    try:
        c.execute("SELECT * FROM logins WHERE username = :username", {"username": user})
        info = c.fetchone()
        print(info)
        db.commit()
    except:
        print("Username does not exist.")
    db.close()

create_db()
add_user("admin", "password")
return_user("admin")
