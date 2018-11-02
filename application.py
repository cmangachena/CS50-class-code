import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    firstname = request.form.get("fname")
    lastname = request.form.get("lname")
    snack = request.form.get("snack")
    quantity = request.form.get("number")
    drink = request.form.get("drink")
    error_message="Please fill in all blanks"
    if not firstname or not lastname or not quantity or not drink or not snack:
        return render_template("error.html")
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("fname"), request.form.get("lname"), request.form.get("snack"),request.form.get("number"), request.form.get("drink")))
    file.close()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    snacks_list = list(reader)
    return render_template("sheet.html", snacks=snacks_list)

