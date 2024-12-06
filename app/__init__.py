# Stanley Hoo, Alex Luo, Leon Huang, Jason Chao
# sIlLySaUsAgEsQuAD
# SoftDev
# P01: ArRESTed Development
# 2024-12-5
# Time spent: 12

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import sqlite3
from database import create_db, add_user, return_user
<<<<<<< HEAD
from api_handler import get_api_data, run_api_program
=======
>>>>>>> 5d4a7bb9327476865df91e249c63a829fca0b9cc


db_filename = "apis.db"

# Auto-generated secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

create_db()


@app.route('/')
def home():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    return redirect(url_for("login"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = return_user(username)

        if user and user[2] == password:  # Match plaintext password
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error_message="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = return_user(username)

        if existing_user:
            error_message = "User already in database"
            return render_template("register.html", error_message=error_message)

        add_user(username, password)

        session["username"] = username
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route('/apiresults')
def apiresults():
    return render_template("apiresults.html")

@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
