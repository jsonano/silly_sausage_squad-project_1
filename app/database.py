import sqlite3

db = sqlite.connect("apis")
c = db.cursor()

def create_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS logins (
        user_id AUTO_INCREMENT,
        username TEXT,
        password_hash TEXT);'''
    )
    c.execute("CREATE TABLE apis (request_id AUTO_INCREMENT,  )")
