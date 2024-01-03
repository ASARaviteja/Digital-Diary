from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import datetime

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_NAME'] = 'MyAppSessionCookie'
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    else:

        # User reached route via POST
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If any field is left blank
        if not username:
            return apology("Username is required")

        elif not password:
            return apology("Password is required")

        elif not confirmation:
            return apology("Confirmation is required")

        # If password and confirmation password doesn't match
        elif password != confirmation:
            return apology("Password and Confirmation doesn't match")

        # Checking whether the password has numbers and has atleast 8 characters
        elif password.isalpha():
            return apology("Password should contain atleast 1 number")

        elif len(password) < 8:
            return apology("Password must be atleast 8 characters")

        # Checking whether the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return apology("Username already exists")

        # Generating a hash for the password and updating username and password to users table
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES (?,?)", username, hash)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Username is required", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Password is required", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def dashboard():

    # Rendering the dashboard template
    return render_template("dashboard.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Adding a new entry into diary"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("add.html")

    else:

        # User reached route via POST
        user_id = session["user_id"]
        text = request.form.get("text")
        date = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        # If text field is left blank
        if not text:
            return apology("Text is required")

        # Query database to check whether there are any entries on given user_id, date, month and year
        history = db.execute("SELECT * FROM diary where user_id = ? AND date = ? AND month = ? AND year = ?",
                             user_id, date, month, year)

        # If one or more entires are present on given user_id, date, month and year
        if len(history) >= 1:
            return apology("Already wrote today's diary, Update it")

        else:

            # Query database to insert the given text on given user_id, date, month and year
            db.execute("INSERT INTO diary(user_id, text, date, month, year) VALUES (?,?,?,?,?)", user_id, text, date, month, year)

            flash("Successfully saved today's diary")

            # Redirect user to home page
            return redirect("/")


@app.route("/read", methods=["GET", "POST"])
@login_required
def read():
    """Reading an entry in the diary"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("read.html")

    else:

        # User reached route via POST
        user_id = session["user_id"]
        year = request.form.get('year')
        month = request.form.get('month')
        date = request.form.get('date')

        # If any field is left blank
        if not date:
            return apology("Date is required")

        elif not month:
            return apology("Month is required")

        elif not year:
            return apology("Year is required")

        # Query database to search the text required on given user_id, date, month and year
        te = db.execute("SELECT text FROM diary WHERE user_id = ? AND date = ? AND month = ? AND year = ?", user_id, date, month, year)

        # If no diary was written on given user_id, date, month and year
        if len(te) < 1:
            return apology("No diary entry found for the specified date")

        t = te[0]['text']
        return render_template("readtext.html", text=t)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Editing an old entry in the diary"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("edit.html")

    else:

        # User reached route via POST
        user_id = session["user_id"]
        year = request.form.get('year')
        month = request.form.get('month')
        date = request.form.get('date')
        text = request.form.get('text')

        # If any field is left blank
        if not text:
            return apology("Text is required")

        elif not date:
            return apology("Date is required")

        elif not month:
            return apology("Month is required")

        elif not year:
            return apology("Year is required")

        # Query database to update the text for given user_id, date, month and year
        db.execute("UPDATE diary SET text = ? WHERE user_id = ? AND date = ? AND month = ? AND year = ?", text, user_id, date, month, year)

        flash(f"Successfully edited {date}/{month}/{year} diary")
        return render_template("dashboard.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Deleting an old entry in the diary"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("delete.html")

    else:

        # User reached route via POST
        user_id = session["user_id"]
        year = request.form.get('year')
        month = request.form.get('month')
        date = request.form.get('date')

        # If any field is left blank
        if not date:
            return apology("Date is required")

        elif not month:
            return apology("Month is required")

        elif not year:
            return apology("Year is required")

        # Query database to delete the entry for given user_id, date, month and year
        db.execute("DELETE FROM diary WHERE user_id = ? AND date = ? AND month = ? AND year = ?", user_id, date, month, year)

        flash(f"Successfully deleted {date}/{month}/{year} diary")
        return render_template("dashboard.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")