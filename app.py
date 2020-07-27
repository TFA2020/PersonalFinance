# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, session
from flask import render_template, request, url_for
from flask_pymongo import PyMongo
import requests
import os
import bcrypt
from datetime import datetime
from flask import redirect

# -- Initialization section --
app = Flask(__name__)

app.secret_key = os.urandom(32)

# name of database
app.config['MONGO_DBNAME'] = 'finance'

# URI of database

MONGO_USER = os.environ['MONGO_USER']
MONGO_PW = os.environ['MONGO_PW']
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_USER}:{MONGO_PW}@cluster0.0jbv6.mongodb.net/finance?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', time = datetime.now())


# CONNECT TO DB, ADD DATA

@app.route('/register', methods = ["POST", "GET"])
def register():
    # connect to the database
    users = mongo.db.users
    # insert new data
    if request.method == "GET":
        return render_template('index.html')
    else:
        # store the username as a variable
        username = request.form["username"]
        password = request.form["password"]
        first = request.form["fname"]
        last = request.form["lname"]
        # print(username)
        # connect to mongo users collection
        users = mongo.db.users
        # do a query for the user in the collection
        query = list(users.find({"username": username}))
        print(query)
        print(len(query))
        # check if the query returned anything we will return "you already have an account"
        if len(query) > 0:
            return "You already have an account. Try logging in"
        else:
            if password == request.form["confirm"]: 
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                users.insert({"username": username, "password": password, "first_name": first, "last_name": last})
                session["name"] = username
                return "congrats! you have logged in"
            else: 
                return "passwords do not match"


@app.route('/login',  methods = ["POST", "GET"])
def login():
    users = mongo.db.users 
    username = request.form["username"]
    password = request.form["password"]
    # print(username)
    # do a query for the user in the collection
    query = list(users.find({"username": username}))
    print(query)
    print(len(query))
    if len(query)>0:
        user_pw = list(users.find({"username": username}))[0]["password"]
        if bcrypt.checkpw(password.encode("utf-8"), user_pw):
            return redirect(url_for("profile"))
        else: 
            return "incorrect password"
    return "username not found"


@app.route('/logout')
def logout():
    return ""

@app.route('/profile')
def profile():
    return render_template("profile.html")
