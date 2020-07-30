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

app.secret_key = "personal-finance-planner-deployment"

# name of database
app.config['MONGO_DBNAME'] = 'finance'

# URI of database
MONGO_USER = os.environ['MONGO_USER']
MONGO_PW = os.environ['MONGO_PW']
MONGO_CLUSTER = os.environ['MONGO_CLUSTER']
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_USER}:{MONGO_PW}@{MONGO_CLUSTER}.mongodb.net/finance?retryWrites=true&w=majority'
mongo = PyMongo(app)

# connect to mongo - users collection
users = mongo.db.users

# -- Routes section --

# No Authentication - Access to all


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.now())


@app.route("/login")
def login():
    return render_template("login.html", time=datetime.now())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/AccessDenied')
def AccessDenied():
    return "You do not have the permission to visit the page specified."


# AUTHENTICATION PROCESS

@app.route('/register', methods=["POST", "GET"])
def register():
    session["error"] = None
    if request.method == "GET":
        return redirect('/')
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
            session["error"] = "username not available. Already exists"
            return redirect('/')

        if password == request.form["confirm"]: 
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            users.insert({"username": username, "password": password, "email": email, "expense":{}, "total_expense" : 0, "submit": False})
            session["username"] = username
            return redirect(url_for("login"))

        session["error"] = "passwords do not match"
        return redirect('/')


@app.route('/sign_in',  methods=["POST", "GET"])
def sign_in():
    session["error"] = None
    if request.method == "POST":
        users = mongo.db.users
        username = request.form["username"]
        password = request.form["password"]
        # do a query for the user in the collection
        query = list(users.find({"username": username}))
        if len(query) > 0:
            user_pw = list(users.find({"username": username}))[0]["password"]
            if bcrypt.checkpw(password.encode("utf-8"), user_pw):
                session["username"] = username
                return redirect(url_for("profile"))
            else: 
                session["error"] = "incorrect password"
                return redirect(url_for('login'))
        session["error"] = "invalid username"
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


# USER FEATURES

@app.route('/profile')
def profile():
    # the code will run through properly if the user is logged in. 
    # using TRY and EXCEPT to create gated pages.
    try:
        user = list(users.find({"username": session["username"]}))[0]
        if user["submit"]:
            income = user["income"]
            goal = user["Savings Goal"]
            result = user["response"]
            balance = user["Current Saving Balance"]
            time = user["time"]
            expenses = user["total_expense"]
            saving_response = {
                "income": income,
                "goal": goal,
                "result": result,
                "balance": balance,
                "time": time,
                "expenses": expenses
            }
            # print(saving_response)
            return render_template("profile.html", response=saving_response, time=datetime.now())
        else:
            return render_template("profile.html", time=datetime.now())
    except KeyError:
        return redirect(url_for('AccessDenied'))


@app.route("/calculator")
def calculator():
    try:
        username = session["username"]
        return render_template("calculator.html", time=datetime.now())
    except KeyError:
        return redirect(url_for('AccessDenied'))


@app.route("/expenses_form")
def expenses_form():
    try:
        username = session["username"]
        return render_template("expenses-form.html", time=datetime.now())
    except KeyError:
        return redirect(url_for('AccessDenied'))


@app.route("/expenses_table")
def expenses_table():
    try:
        # find user based on username
        user = users.find({"username": session["username"]})
        user = list(user)[0]
        # retrieve data from mongo
        expense = user["expense"]
        total = user["total_expense"]
        # separate expense dictionary into two lists
        items = list(expense.keys())
        prices = list(expense.values())
        # print(prices, items)
        return render_template("expenses-table.html", prices=prices, items=items, total_expense= total, time=datetime.now())
    except KeyError:
        return redirect(url_for('AccessDenied'))


@app.route("/savings", methods=["POST", "GET"])
def savings():
    if request.method == "POST":
        # print(dict(request.form))
        users = mongo.db.users
        user = list(users.find({"username": session["username"]}))[0]
        expenses = user["total_expense"]
        # retrieve form data
        income = request.form["income"]
        goal = request.form["goal"]
        time = request.form["time"]
        balance = request.form["balance"]
        # include is either "YES" or "NO"
        include = request.form['includeExpense']
        if include == "YES":
            response = model.calc_saving(income, goal, time, balance, expenses)
        else:
            response = model.calc_saving(income, goal, time, balance)

        myquery = {"username": session['username']}
        changes = [
            {"$set": {"income": income}},
            {"$set": {"time": time}},
            {"$set": {"response": response}},
            {"$set": {"Current Saving Balance": balance}},
            {"$set": {"Savings Goal": goal}},
            {"$set": {"submit": True}}
        ]
        for change in changes:
            users.update_one(myquery, change)
        return redirect(url_for('profile'))
    else:
        return redirect('/')


@app.route("/for_expenses", methods=["POST", "GET"])
def for_expenses():
    if request.method == "POST":
        response = list(dict(request.form).values())
        items = {}
        # https://repl.it/repls/LastDimpledOrganization
        for i in range(0, len(response), 2):
            # the form data is stored in the order of {"item", price, "item", price etc ...}
            # get item
            item = response[i]
            # get next value stored in list, which is the item's price
            price = float(response[i+1])
            # store into items dictionary {item : price}
            items[item] = price
        myquery = {"username": session['username']}
        newItems = {"$set": {"expense": items}}
        newExpenseTotal = {"$set": {"total_expense": round(sum(items.values()), 2)}}
        users.update_one(myquery, newItems)
        users.update_one(myquery, newExpenseTotal)
        return redirect(url_for('expense_table'))
    else:
        return redirect('/')


# https://stackoverflow.com/questions/25290044/how-can-you-make-a-page-not-found-feature-using-flask