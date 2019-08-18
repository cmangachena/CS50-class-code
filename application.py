import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///eventsinfo.db")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # get username
    check = request.args.get("username")
    # check if username is available
    if len(check) == 0 or db.execute("SELECT * FROM users WHERE username = :check", check=check):
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/")
def index():
    """Show all categories of events"""
    if request.method == "GET":
        #
        category = ["Study Abroad", "Research", "Internships", "Volunteer Work", "Activities in Boston", "Club Events", "Campus Parties", "Other"]
        return render_template("index.html", category=category)

@app.route("/search", methods=["POST"])
def search():
    #
    q=request.form.get("q")
    if not q:
        return apology("No blanks please")
    #
    q= q.lower()
    results=db.execute(f"SELECT * FROM events WHERE event_name LIKE '%{q}%' OR event_category LIKE '%{q}%' OR event_description LIKE '%{q}%'")
    if not results:
        return apology(" No items match your search, Try using a different key-word")
    return render_template("results.html", results=results)


@app.route("/newevent", methods=["GET", "POST"])
@login_required
def newevent():
    """Post New Events"""
    if request.method == "POST":
        # Collect event information
        event_category = request.form.get("event_category")
        event_name = request.form.get("event_name")
        event_location = request.form.get("event_location")
        event_date = request.form.get("event_date")
        event_time = request.form.get("event_time")
        event_description = request.form.get("event_description")
        # Check if any of the fields are blank
        if not event_category or not event_name or not event_location or not event_date or not event_time or not event_description:
            return apology("Please fill in all fields")
        # Store information about new event into database.
        db.execute("INSERT INTO events (id , username, event_name, event_category, event_location, event_date, event_time, event_description)"\
                       "VALUES(:id, :u, :n, :c, :l, :date, :t, :description)",
                      id=session["user_id"], u=session["username"], n=event_name, c=event_category, l=event_location, date=event_date, t=event_time, description=event_description)
        return redirect("/")
    # When admin wants to post newevent
    else:
        return render_template("newevent.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of events posted"""
    rows = db.execute("SELECT event_name, event_category, event_location, event_date, event_time, event_description FROM events WHERE id = :id", id=session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("Must provide username", 403)
        if username == db.execute("SELECT * FROM users WHERE username=:username", username=username):
            return apology("Chosen username is unavailable. Please choose a different name", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct
        if not rows:
            return apology("Username not found. Please make sure you have registered first.")

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get username from submitted form
        username = request.form.get("username").lower()
        #create a list of illegal SQL characters
        illegal_chars = ["0", ";", ",", "\"", "\b", "\n", "\r", "\t", "\\", "%", "_"]
        #create a for loop to check if username contains illegal characters:
        for ch in illegal_chars:
            if ch in username:
                return apology("Username contains illegal characters. Please choose a different username", 400)
        # Check if username is not blank
        if not username:
            return apology("Username cannot be empty", 400)
        # Check if username is available
        if db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return apology("Username is unavailable. Please choose a different username", 400)
        # Get password and confirmation from form submitted
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Check if password is blank or if confirmation is blank
        if not password or not confirmation:
            return apology("Password/Confirmation cannot be empty", 400)
        # Check if confirmation matches password
        if password != confirmation:
            return apology("Password and Confirmation do not match", 400)
        # Convert password to has
        password_hash = generate_password_hash(password)
        # Input user data into database
        final = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password_hash)", username=username, password_hash=password_hash)
        # Remember which user has registered and log them in
        session["user_id"] = final
        session["username"] = username
        # Inform user that they have registered
        flash("REGISTERED!!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/study_abroad", methods=["GET", "POST"])
def study_abroad():
    if request.method=="GET":
        # Create a variable called category
        category = "study_abroad"
        # Get all events from database in the study abroad category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category= :category", category=category)
        print()
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/research", methods=["GET", "POST"])
def research():
    if request.method=="GET":
        # Create a variable called category
        category = "research"
        # Get all events from database in the research category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)


@app.route("/internship", methods=["GET", "POST"])
def internship():
    if request.method=="GET":
        # Create a variable called category
        category = "internship"
        # Get all events from database in the internship category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method=="GET":
        # Create a variable called category
        category = "volunteer"
        # Get all events from database in the volunteer category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/boston", methods=["GET", "POST"])
def boston():
    if request.method=="GET":
        # Create a variable called category
        category = "boston"
        # Get all events from database in the boston category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/clubs", methods=["GET", "POST"])
def clubs():
    if request.method=="GET":
        # Create a variable called category
        category = "clubs"
        # Get all events from database in the clubs category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/campus", methods=["GET", "POST"])
def campus():
    if request.method=="GET":
        # Create a variable called category
        category = "campus"
        # Get all events from database in the campus category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/other", methods=["GET", "POST"])
def other():
    if request.method=="GET":
        # Create a variable called category
        category = "other"
        # Get all events from database in the other category
        ordered_events = db.execute("SELECT * FROM events WHERE event_category = :category", category=category)
        return render_template("events.html", ordered_events=ordered_events)
    else:
        return redirect("/")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method=="GET":
        # Collect all reviews from the reviews table
        reviews = db.execute("SELECT * FROM reviews")
        return render_template("feedback.html", reviews=reviews)

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    # Display form for user to fill and leave a review
    if request.method=="GET":
        return render_template("review.html")
    else:
        # Collect data from the user's input on the form
        event_category = request.form.get("event_category")
        event_name = request.form.get("event_name")
        event_location = request.form.get("event_location")
        event_date = request.form.get("event_date")
        review = request.form.get("review")
        # Check if user did not leave any fields blank.
        if not event_category or not event_name or not event_location or not event_date:
            return apology("Please provide all information about the event you want to review.")
        # Check if the event user wants to review actually occurred.
        event = db.execute("SELECT event_name FROM events WHERE event_name = :event_name", event_name=event_name)
        if not event:
            return apology("You are trying to review an event that never occurred!")
        # Record user's review.
        db.execute("INSERT INTO reviews (event_category, event_name, event_location, event_date, review) VALUES(:c, :n , :l, :d, :r)",
                  c=event_category, n=event_name,  l=event_location, d=event_date, r=review )
        reviews = db.execute("SELECT * FROM reviews")
        return render_template("feedback.html", reviews=reviews)

@app.route("/events", methods=["GET"])
def events():
    # List of all categories
    categories = ["study_abroad", "research", "internship", "volunteer", "boston", "clubs", "campus", "other"]
    ordered_events = []
    # Collect all events from database from all categories in order and display in allevents page.
    for i in categories:
        category = i
        rows = db.execute("SELECT * FROM events WHERE event_category= :category", category=category)
        ordered_events.append(rows)
    return render_template("allevents.html", ordered_events=ordered_events)

