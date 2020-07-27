# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, session
from flask import render_template, request, url_for
from flask_pymongo import PyMongo
import requests
import os
import bcrypt
from datetime import datetime

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
# MONGO_USER = os.environ['MONGO_USER']
# MONGO_PW = os.environ['MONGO_PW']
app.config['MONGO_URI'] = 'mongo-uri'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', time = datetime.now())


# CONNECT TO DB, ADD DATA

@app.route('/register')
def register():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""


@app.route('/login')
def login():
    
    return ""


@app.route('/logout')
def logout():
    return ""