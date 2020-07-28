# ---- YOUR APP STARTS HERE ----
# -- Import section --
import bcrypt
from datetime import datetime
from flask import Flask
from flask import redirect, render_template, request
from flask import session
from flask import url_for
from flask_pymongo import PyMongo
import model
import requests
import os

# -- Initialization section --
app = Flask(__name__)

app.secret_key = os.urandom(32)

# name of database
app.config['MONGO_DBNAME'] = 'finance'

# URI of database
MONGO_USER = os.environ['MONGO_USER']
MONGO_PW = os.environ['MONGO_PW']
MONGO_CLUSTER = os.environ['MONGO_CLUSTER']
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_USER}:{MONGO_PW}@{MONGO_CLUSTER}.mongodb.net/finance?retryWrites=true&w=majority'
mongo = PyMongo(app)

# -- Routes section --
# HTML PAGE ROUTES


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.now())


@app.route("/login")
def login():
    return render_template("login.html", time=datetime.now())


@app.route('/profile')
def profile():
    return render_template("profile.html", time=datetime.now())


# CONNECT TO DB, ADD DATA

@app.route('/register', methods=["POST", "GET"])
def register():
    session["error"] = None
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
            return "<a href='/'>redirect to main</a>"
            # return redirect('/')
        if password == request.form["confirm"]: 
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            users.insert({"username": username, "password": password, "email": email})
            session["username"] = username
            return "<a href='/login'>redirect to login</a>"
            # return redirect(url_for("login"))
        session["error"] = "passwords do not match"
        return "<a href='/'>redirect to main</a>"
        # return redirect('/')


@app.route('/sign_in',  methods=["POST", "GET"])
def sign_in():
    users = mongo.db.users
    username = request.form["username"]
    password = request.form["password"]
    session["error"] = None
    # do a query for the user in the collection
    query = list(users.find({"username": username}))
    if len(query) > 0:
        user_pw = list(users.find({"username": username}))[0]["password"]
        if bcrypt.checkpw(password.encode("utf-8"), user_pw):
            session["username"] = username
            return "<a href='/profile'>redirect to profile</a>"
            # return redirect(url_for("profile"))
        else: 
            session["error"] = "incorrect password"
            return "<a href='/login'>redirect to login</a>"
            # return redirect('/login')
    session["error"] = "invalid username"
    return "<a href='/login'>redirect to login</a>"
    # return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return "<a href='index'>redirect to main</a>"
    # return redirect('/')


@app.route("/savings", methods=["POST", "GET"])
def saving():
    income = request.form["income"]
    goal = request.form["goal"]
    age = request.form["age"]
    response = model.calc_saving(income, goal, age)
    return render_template("profile.html", response=response, time=datetime.now())