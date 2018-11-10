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
db = SQL("sqlite:///finance.db")

# Create a function that returns a dictionary of all shares available and the current balance
def current_shares():
    # Create dictionary
    info_dict = dict()
    # Get information from database
    rows = db.execute("SELECT symbol, number_of_shares, price FROM transactions WHERE id = :id", id = session["user_id"])
    # Update dictionary
    for dictionary in rows:
        if dictionary["symbol"] in info_dict:

            info_dict[dictionary["symbol"]] += dictionary["number_of_shares"]
        else:
            info_dict[dictionary["symbol"]] = dictionary["number_of_shares"]

    return info_dict


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # create list that stores all information to be displayed in index
    index_list = []
    # get the current balance of shares for user
    current_dict = current_shares()

    for (key, value) in current_dict.items():
        if value == 0:
            continue
        minor_list = []
        quote = lookup(key)
        minor_list.append(key)
        name = quote.get("name")
        minor_list.append(name)
        shares = value
        minor_list.append(value)
        price = quote.get("price")
        minor_list.append(price)
        total = float(value * price)
        minor_list.append(total)
        index_list.append(minor_list)
    cash = float(db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"])
    return render_template("index.html", index_list=index_list, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Call function to create a dictionary of current information
        symbol_dict = current_shares()
        # Get symbol user chose
        symbol = request.form.get("symbol").upper()
        # Get amount of shares user wants to buy
        shares = request.form.get("shares")
        if shares == "":
            return apology("Please input number of shares", 400)
        # Check if user can afford shares
        quote = lookup(symbol)
        if (quote == None):
            return apology("Stock symbol doesn't exist", 400)
        price = quote["price"]
        # Calculate cost of shares to be purchased
        number = float(shares)
        cost = number * price
        result = db.execute("SELECT cash FROM users WHERE id= :id", id=session["user_id"])
        # Check if user can afford shares
        if cost > result[0]["cash"]:
            return apology("You have insuficient funds to purchase", 400)
        else:
            db.execute("UPDATE users SET cash = (cash - :cost) WHERE id= :id", id = session["user_id"] , cost=cost)
            db.execute("INSERT INTO transactions (id , username, symbol, number_of_shares, price, transaction_time)"\
                       "VALUES(:id, :u, :s, :n, :p, date('now'))",
                       id=session["user_id"], u=session["username"], s=quote.get("symbol"), n=number, p=price)
            # Update symbol dictionary after transaction
            if symbol in symbol_dict:
                symbol_dict[symbol] += number
            else:
                symbol_dict[symbol] = number
            flash("BOUGHT")
            return redirect("/")

    else:
        return render_template("buy.html")


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


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "POST":
        return apology("TODO", 400)
    else:

       rows = db.execute("SELECT symbol, number_of_shares, price, transaction_time FROM transactions WHERE id = :id", id=session["user_id"])

    return render_template("history.html", rows=rows)
    #return apology("TODO")


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
        if len(rows) != 1:
            return apology("No blanks")

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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Get symbol from form submitted
        symbol = request.form.get("symbol").upper()
        # Check if string "symbol" is empty:
        if symbol == "":
            return apology("please provide a valid symbol", 400)
        # Get dictionary of current price of shares
        quotation = lookup(symbol)
        # Check if symbol is valid by checking if quotation is empty
        if quotation == None:
            return apology("The symbol doesn't exist", 400)
        # Show user current price
        return render_template("quoted.html", quotation=quotation)
    # User has reached route via GET
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Call to function that creates dictionary of current shares of user
    symbol_dict = current_shares()
    if request.method == "POST":
        # Get symbol to be sold from form
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please choose a symbol", 400)
        # Get amount of shares to be sold from form
        shares = request.form.get("shares")
        # Lookup current price of shares to be sold
        quote = lookup(symbol)
        price = quote.get("price")
        # Calculate how much cash will come from the sale of shares
        number = int(shares)
        sale = number*price
        # Get number of shares currently available for given symbol
        result = symbol_dict[symbol]
        # Check if user has sufficient shares to sell
        if number > result:
            return apology("You do not have enough shares to sell", 400)
        else:
            # Update cash to reflect transaction
            db.execute("UPDATE users SET cash = (cash + :sale) WHERE id= :id", id=session["user_id"], sale=sale)
            # Record transaction in database
            db.execute("INSERT INTO transactions (id , username, symbol, number_of_shares, price, transaction_time)"\
                       "VALUES(:id, :u, :s, :n, :p, date('now'))",
                       id=session["user_id"], u=session["username"], s=quote.get("symbol"), n=(-1*number), p=price)
            # Update symbol dictionary of current shares
            symbol_dict[symbol] = result - number
            # Inform user they successfully sold at homepage
            flash("SOLD!")
            return redirect("/")
    # If user arrives at route via GET
    else:
        # Get information of the current shares user has ability to sell
        current_dict = current_shares()
        # Create list of available shares for user to sell and only append it if the value of shares in dictionary is greater than zero
        available = []
        for (key, value) in current_dict.items():
            if value > 0:
                available.append(key)
    # Allow user to sell
    return render_template("sell.html", available=available)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to account"""
    if request.method =="POST":
        # Get amount of cash user wants to add
        cash = request.form.get("addcash")
        # Check if user did not leave amount row blank
        if cash =="":
            return apology("Amount cannot be empty", 400)
        # Convert amount user wants to sell from a string to a float amount
        cash1 = float(cash)
        # Add cash amount to current cash balance into database
        db.execute("UPDATE users SET cash = (cash + :cash) WHERE id=:id", cash = cash1, id = session["user_id"])
        # Inform user of successful addition and take them to homepage
        flash("ADDED!")
        return redirect("/")
    else:
        return render_template("addcash.html")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

