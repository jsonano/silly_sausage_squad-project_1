import sqlite3

db = sqlite3.connect("apis")
c = db.cursor()

def create_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS logins (
        user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
    );
    ''')
    
    c.execute('''
        CREATE TABLE apis (
        request_id INTEGER PRIMARY KEY AUTO_INCREMENT,  
        foreign key(user_id) REFERENCES logins(user_id),
        api_name TEXT NOT NULL,
        request TEXT NOT NULL,
        response TEXT NOT NULL,
    );
    ''')

def add_user(username, password_hash):
    c.execute("INSERT INTO logins (username, password_hash) VALUES (?, ?)", (username, password_hash))
    db.commit()

db.close()
