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
import model

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
    if request.method == "GET":
        return render_template('index.html')
    else:
        # store the form data as variables
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        # connect to mongo users collection
        users = mongo.db.users
        # do a query for the user in the collection
        query = list(users.find({"username": username}))
        # check if the query returned anything : does the username exist?
        if len(query) > 0:
            # return redirect('/')
            session["error"] = "username not available. Already exists"
            return "<a href='/'>redirect</a>"
        else:
            if password == request.form["confirm"]: 
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                users.insert({"username": username, "password": password, "email": email})
                session["username"] = username
                return redirect(url_for("login"))
                #return "<a href='/login'>login page</a>"
            else: 
                session["error"] = "passwords do not match"
                return redirect('/')
                #return "<a href='/'>redirect</a>"

#HTML PAGE ROUTES
@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html", time=datetime.now())


@app.route('/logon',  methods = ["POST", "GET"])
def logon():
    users = mongo.db.users 
    username = request.form["username"]
    password = request.form["password"]
    # do a query for the user in the collection
    query = list(users.find({"username": username}))
    if len(query) > 0:
        user_pw = list(users.find({"username": username}))[0]["password"]
        if bcrypt.checkpw(password.encode("utf-8"), user_pw):
            # return redirect(url_for("profile"))
            return "<a href='/profile'>Profile</a>"
        else: 
            session["error"] = "incorrect password"
            return redirect('/')
    session["error"] = "invalid username"
    # return redirect('/')
    return "<a href='/'>Go Home</a>"


@app.route('/logout')
def logout():
    return ""

@app.route("/savings", methods = ["POST", "GET"])
def saving():
    income = request.form["income"] 
    goal = request.form["goal"]
    age = request.form["age"]
    return render_template("profile.html", response = model.calc_saving(income,goal,age), time=datetime.now())