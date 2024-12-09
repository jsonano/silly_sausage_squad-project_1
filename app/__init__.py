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
import urllib.request
import json

from database import create_db, add_user, login_user, return_user, add_api_request, return_api_request
from api_handler import get_api_data, run_api_program


db_filename = "apis.db"

# Auto-generated secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

create_db()


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_user()
    return redirect(url_for('home'))

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

@app.route('/profile')
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    user_requests = return_api_request(username)

    return render_template("profile.html", username=username, requests=user_requests)

@app.route('/apiresults', methods=["GET", "POST"])
def apiresults():
    return render_template("apiresults.html")

@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
