from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, zar

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["zar"] = zar

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

# Get the current day to be used in retriving the current month for the user
today = date.today()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """ User Homepage """
    if request.method == "GET":
        user_id = session["user_id"]

        # Get the year and month to display the user data
        current_date = str(today.year) + '-' + str(today.month)
        tips_date = current_date + '%'
        user_dates = db.execute("SELECT date FROM income WHERE user_id = ? and date != ?", user_id, current_date)

        # Retrive the values for the user income, tips and expenses for the month
        income = db.execute("SELECT total AS total_income FROM income WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_income"]
        tips = db.execute("SELECT SUM(total) as total_tips FROM tips WHERE user_id = ? AND date LIKE ?", user_id, tips_date)[0]["total_tips"]
        expenses = db.execute("SELECT SUM(total) AS total_expense FROM expenses WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_expense"]

        # Retrive the individual expense values as a dictionary
        all_expenses = db.execute("SELECT housing, food, transport, childcare, health, insurance, utilities, savings, personal, entertainment, misc FROM expenses WHERE user_id = ? AND date = ? ORDER BY date", user_id, current_date)

        return render_template("index.html", user_dates=user_dates, current_date=current_date, income=income, expenses=expenses, tips=tips, all_expenses=all_expenses)
    else:
        # The following section will update the selected expense to update
        user_id = session["user_id"]
        current_date = request.form.get("date_selected")
        tips_date = current_date + '%'
        user_dates = db.execute("SELECT date FROM income WHERE user_id = ? and date != ?", user_id, current_date)

        # The view will retrive the data of a specified month, if it does exsist
        if request.form["submit"] == "view":

            income = db.execute("SELECT total AS total_income FROM income WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_income"]
            tips = db.execute("SELECT SUM(total) as total_tips FROM tips WHERE user_id = ? AND date LIKE ?", user_id, tips_date)[0]["total_tips"]
            expenses = db.execute("SELECT SUM(total) AS total_expense FROM expenses WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_expense"]

            all_expenses = db.execute("SELECT housing, food, transport, childcare, health, insurance, utilities, savings, personal, entertainment, misc FROM expenses WHERE user_id = ? AND date = ? ORDER BY date", user_id, current_date)

            return render_template("index.html", user_dates=user_dates, current_date=current_date, income=income, expenses=expenses, tips=tips, all_expenses=all_expenses)

        # All of the below sections do basically the same function, it updates the specific expense.
        # This section was a lot of the same code reused and I will definitly be coming back to improve this.
        elif request.form["submit"] == "housing":

            # Retrieve the current value in the database
            current_housing = db.execute("SELECT housing FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["housing"]

            # Ensure the user entered a value
            try:
                update_value = float(request.form.get("update_housing"))
            except:
                return apology("No value entered to update")

            # Retrieve the total amount in expenses
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            # If the value entered is less than the current value, meaning the user is saving some money, deduct the difference from the total expenses
            if current_housing > update_value:
                difference = current_housing - update_value
                total -= difference
            # Otherwise the difference needs to be added to total expenses
            else:
                difference = update_value - current_housing
                total += difference

            # Update the database with the new values for the expense and for the total expenses
            db.execute("UPDATE expenses SET housing = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "food":
            current_food = db.execute("SELECT food FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["food"]
            try:
                update_value = float(request.form.get("update_food"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_food > update_value:
                difference = current_food - update_value
                total -= difference
            else:
                difference = update_value - current_food
                total += difference

            db.execute("UPDATE expenses SET food = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "transport":
            current_transport = db.execute("SELECT transport FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["transport"]
            try:
                update_value = float(request.form.get("update_transport"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_transport > update_value:
                difference = current_transport - update_value
                total -= difference
            else:
                difference = update_value - current_transport
                total += difference

            db.execute("UPDATE expenses SET transport = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "childcare":
            current_childcare = db.execute("SELECT childcare FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["childcare"]
            try:
                update_value = float(request.form.get("update_childcare"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_childcare > update_value:
                difference = current_childcare - update_value
                total -= difference
            else:
                difference = update_value - current_childcare
                total += difference

            db.execute("UPDATE expenses SET childcare = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "health":
            current_health = db.execute("SELECT health FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["health"]
            try:
                update_value = float(request.form.get("update_health"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_health > update_value:
                difference = current_health - update_value
                total -= difference
            else:
                difference = update_value - current_health
                total += difference

            db.execute("UPDATE expenses SET health = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "insurance":
            current_insurance = db.execute("SELECT insurance FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["insurance"]
            try:
                update_value = float(request.form.get("update_insurance"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_insurance > update_value:
                difference = current_insurance - update_value
                total -= difference
            else:
                difference = update_value - current_insurance
                total += difference

            db.execute("UPDATE expenses SET insurance = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "utilities":
            current_utilities = db.execute("SELECT utilities FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["utilities"]
            try:
                update_value = float(request.form.get("update_utilities"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_utilities > update_value:
                difference = current_utilities - update_value
                total -= difference
            else:
                difference = update_value - current_utilities
                total += difference

            db.execute("UPDATE expenses SET utilities = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "savings":
            current_savings = db.execute("SELECT savings FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["savings"]
            try:
                update_value = float(request.form.get("update_savings"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_savings > update_value:
                difference = current_savings - update_value
                total -= difference
            else:
                difference = update_value - current_savings
                total += difference

            db.execute("UPDATE expenses SET savings = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "personal":
            current_personal = db.execute("SELECT personal FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["personal"]
            try:
                update_value = float(request.form.get("update_personal"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_personal > update_value:
                difference = current_personal - update_value
                total -= difference
            else:
                difference = update_value - current_personal
                total += difference

            db.execute("UPDATE expenses SET personal = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "entertainment":
            current_entertainment = db.execute("SELECT entertainment FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["entertainment"]
            try:
                update_value = float(request.form.get("update_entertainment"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_entertainment > update_value:
                difference = current_entertainment - update_value
                total -= difference
            else:
                difference = update_value - current_entertainment
                total += difference

            db.execute("UPDATE expenses SET entertainment = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        elif request.form["submit"] == "misc":
            current_misc = db.execute("SELECT misc FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["misc"]
            try:
                update_value = float(request.form.get("update_misc"))
            except:
                return apology("No value entered to update")
            total = db.execute("SELECT total FROM expenses WHERE user_id = ? AND date = ?", user_id, current_date)[0]["total"]

            if current_misc > update_value:
                difference = current_misc - update_value
                total -= difference
            else:
                difference = update_value - current_misc
                total += difference

            db.execute("UPDATE expenses SET misc = ? WHERE user_id = ? AND date = ?", update_value, user_id, current_date)
            db.execute("UPDATE expenses SET total = ? WHERE user_id = ? AND date =?", total, user_id, current_date)

        # After all the elif blocks, retrive the data again to refresh the index page with updated values
        tips_date = current_date + '%'
        user_dates = db.execute("SELECT date FROM income WHERE user_id = ? and date != ?", user_id, current_date)

        income = db.execute("SELECT total AS total_income FROM income WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_income"]
        tips = db.execute("SELECT SUM(total) as total_tips FROM tips WHERE user_id = ? AND date LIKE ?", user_id, tips_date)[0]["total_tips"]
        expenses = db.execute("SELECT SUM(total) AS total_expense FROM expenses WHERE date = ? AND user_id = ?", current_date, user_id)[0]["total_expense"]

        all_expenses = db.execute("SELECT housing, food, transport, childcare, health, insurance, utilities, savings, personal, entertainment, misc FROM expenses WHERE user_id = ? AND date = ? ORDER BY date", user_id, current_date)

        flash("Expense Updated")

        return render_template("index.html", user_dates=user_dates, current_date=current_date, income=income, expenses=expenses, tips=tips, all_expenses=all_expenses)



@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Capture details entered
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check that the user completed the username, password and confirmation fields
        if not username:
            return apology("Enter a username")
        if not password:
            return apology("Enter a password")
        if not confirmation:
            return apology("Confirm password")

        # Check that the password and confrimation matches
        if password != confirmation:
            return apology("Passwords do not match")

        # Hash the password for insertion
        pwd_hash = generate_password_hash(password)

        # Try inserting username otherwise username already exsists
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pwd_hash)
        except:
            return apology("Username already exsists")

        flash("Registration Successful!")

        # Allow the session to store the user logged in
        session["user_id"] = new_user

        return redirect("/income")


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """ Enter Monthly Income """
    if request.method == "GET":
        return render_template("income.html")
    else:
        user_id = session["user_id"]
        # Get the date selected by the user
        try:
            date = request.form.get("date")
        except:
            return apology("Enter Date")
        # Get the number of hours worked for the month
        try:
            hours_worked = float(request.form.get("hours"))
        except:
            return apology("Please enter total number of hours worked")
        # Get the rate of pay
        try:
            hourly_rate = float(request.form.get("rate"))
        except:
            return apology("Please enter your hourly pay rate")

        # Calculate the total wage for the month
        wage = hours_worked * hourly_rate

        # If the user does not include other forms of income, set default to Zero
        try:
            other = float(request.form.get("other"))
        except:
            other = 0.00

        # Calculate total income
        total = wage + other

        # Attempt to enter values into database, if it already exsists, error will be displayed
        try:
            db.execute("INSERT INTO income (user_id, wage, other, total, date) VALUES (?, ?, ?, ?, ?)", user_id, wage, other, total, date)
        except:
            return apology("Income for the month and year already exsists")

        flash("Income Saved")

        return redirect("/tips")


@app.route("/tips", methods=["GET", "POST"]) # https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
@login_required
def tips():
    """ Add tip amounts to income """
    if request.method == "GET":
        return render_template("tips.html")
    else:
        # If the user enters data and wants to continue, the expenses page will be rendered
        if request.form["action"] == "continue":
            user_id = session["user_id"]
            date = request.form.get("date")

            # Ensure the user enters at least one value
            if not request.form.get("cash") and not request.form.get("card"):
                return apology("One or both values needs to be entered to save today's tips")

            # If either value is not entered, it will default to zero
            try:
                cash = float(request.form.get("cash"))
            except:
                cash = 0.00

            try:
                card = float(request.form.get("card"))
            except:
                card = 0.00

            # Calculate total tips for the day
            total = cash + card

            # Attempt to enter values into the specified day, if it exsists, error will be displayed
            try:
                db.execute("INSERT INTO tips (user_id, cash, card, total, date) VALUES (?, ?, ?, ?, ?)", user_id, cash, card, total, date)
            except:
                return apology("Tips for today already saved")

            flash("Tips for today saved")

            return redirect("/expenses")

        # If the user wishes to add another day, the data is saved and the page refreshes
        elif request.form["action"] == "add":
            user_id = session["user_id"]
            date = request.form.get("date")

            if not request.form.get("cash") and not request.form.get("card"):
                return apology("One or both values needs to be entered to save today's tips")

            try:
                cash = float(request.form.get("cash"))
            except:
                cash = 0.00

            try:
                card = float(request.form.get("card"))
            except:
                card = 0.00

            total = cash + card

            try:
                db.execute("INSERT INTO tips (user_id, cash, card, total, date) VALUES (?, ?, ?, ?, ?)", user_id, cash, card, total, date)
            except:
                return apology("Tips for today already saved")

            flash("Tips for today saved")

            return redirect("/tips")



@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    """ Enter Monthly Expenses """
    if request.method == "GET":
        expenses = ["Housing", "Food", "Transport", "Childcare", "Healthcare", "Insurance", "Utilities", "Savings", "Personal", "Entertainment", "Miscellaneous"]
        return render_template("expenses.html", expenses=expenses)
    else:
        user_id = session["user_id"]
        date = request.form.get("date")

        # If the user does not enter a value for one or more expenses, the value defaults to zero
        try:
            housing = float(request.form.get("Housing"))
        except:
            housing = 0.00
        try:
            food = float(request.form.get("Food"))
        except:
            food = 0.00
        try:
            transport = float(request.form.get("Transport"))
        except:
            transport = 0.00
        try:
            child = float(request.form.get("Childcare"))
        except:
            child = 0.00
        try:
            health = float(request.form.get("Healthcare"))
        except:
            health = 0.00
        try:
            insurance = float(request.form.get("Insurance"))
        except:
            insurance = 0.00
        try:
            utilities = float(request.form.get("Utilities"))
        except:
            utilities = 0.00
        try:
            savings = float(request.form.get("Savings"))
        except:
            savings = 0.00
        try:
            personal = float(request.form.get("Personal"))
        except:
            personal = 0.00
        try:
            entertainment = float(request.form.get("Entertainment"))
        except:
            entertainment = 0.00
        try:
            misc = float(request.form.get("Miscellaneous"))
        except:
            misc = 0.00

        # Calculate the total of all values entered
        total = housing + food + transport + child + health + insurance + utilities + savings + personal + entertainment + misc

        # Ensure the user entered at least one value
        if housing == 0.00 and food == 0.00 and transport == 0.00 and child == 0.00 and health == 0.00 and insurance == 0.00 and utilities == 0.00 and savings == 0.00 and personal == 0.00 and entertainment == 0.00 and misc == 0.00:
            return apology("One or more expenses needs to be completed")

        # attempt to enter data into database, if it exsists, an error will be displayed
        try:
            db.execute("INSERT INTO expenses (user_id, housing, food, transport, childcare, health, insurance, utilities, savings, personal, entertainment, misc, total, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        user_id, housing, food, transport, child, health, insurance, utilities, savings, personal, entertainment, misc, total, date)
        except:
            return apology("Expenses for month already done")

        flash("Expenses Saved")

        return redirect("/")