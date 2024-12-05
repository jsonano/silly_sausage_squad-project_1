# Stanley Hoo, Jacob Lukose, Naomi Lai, Colyi Chen
# sIlLySaUsAgEsQuAD
# SoftDev
# P01: ArRESTed Development
# 2024-12-5
# Time spent: 12

# Imports
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os

# Auto-generated secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

@app.route('/')
def home():
    return 'a'

if __name__ == "__main__":
    app.run(debug=True)