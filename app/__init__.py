# Stanley Hoo, Alex Luo, Leon Huang, Jason Chao
# sIlLySaUsAgEsQuAD
# SoftDev
# P01: ArRESTed Development
# 2024-12-5
# Time spent: 12

# Imports
import os
import sqlite3
import urllib.request
import json

from flask import Flask, request, render_template, redirect, url_for, flash, session

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
            flash('Username already taken, choose another one', 'error')
            return render_template("register.html")

        add_user(username, password)

        session["username"] = username
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route('/profile')
def profile():
    if "username" not in session:
        flash("Login to view your profile!", 'error')
        return redirect(url_for("login"))

    username = session["username"]
    user_requests = return_api_request(username)

    return render_template("profile.html", username=username, requests=user_requests)

@app.route('/api_requests', methods=["GET", "POST"])
def api_requests():
    if request.method == 'POST':
        return get_api_data()
    return render_template("api_requests.html")

@app.route('/logout', methods=["POST"])
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

@app.route('/get_api_data', methods=["GET", "POST"])
def get_api_data():
    if False:
        return 1
#     if "username" not in session:
#         flash('Login to use API requests!', 'error')
#         return redirect(url_for("api_requests"))
    else:
        # Gets the input
        input_option = request.form.get('input_option')
        image_file = request.files.get('image_file')
        image_url = request.form.get('image_url')
        selected_url = request.form.get('selected_image')
        search_query = request.form.get('search_query')
        # Different calls for each input
        if input_option == 'random':
            url, description, videos = run_api_program()
            return render_template("api_results.html", url=url, description=description, videos=videos)
        elif input_option == 'upload':
            if image_file:
                print(image_file)
                file_content = image_file.read() 
                url, description, videos = run_api_program(image_file=image_file)
                return render_template("api_results.html", url=url, description=description, videos=videos)
            else:
                flash('Upload an image!', 'error')
                return render_template("api_requests.html")
        elif input_option == 'url':
            if image_url:
                url, description, videos = run_api_program(user_image_url=image_url)
                return render_template("api_results.html", url=url, description=description, videos=videos)
            else:
                flash('Enter an url!', 'error')
                return render_template("api_requests.html")
        elif selected_url:
                url, description, videos = run_api_program(user_image_url=selected_url)
                return render_template("api_results.html", url=url, description=description, videos=videos)
        else:
            if search_query:
                img_urls = run_api_program(search_request=search_query)
#                 print(img_urls)
                return render_template("api_requests.html", img_urls=img_urls)
            else:
                flash('Enter a description!', 'error')
                return render_template("api_requests.html")


if __name__ == "__main__":
    app.run(debug=True)
