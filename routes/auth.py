from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import mysql
from utils.auth import verify_password

auth = Blueprint("auth", __name__)

# ---------------- HOME ---------------- #

@auth.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN PAGE ---------------- #

@auth.route("/login")
def login():
    return render_template("login.html")


# ---------------- LOGIN ---------------- #

@auth.route("/login", methods=["POST"])
def login_post():

    email = request.form["email"]
    password = request.form["password"]

    cur = mysql.connection.cursor()

    # ---------- Check Admin ----------
    cur.execute(
        "SELECT * FROM admins WHERE email=%s",
        (email,)
    )

    admin = cur.fetchone()

    if admin:

        if verify_password(password, admin[3]):

            session.clear()
            session["admin"] = admin[0]
            session["admin_name"] = admin[1]

            flash("Welcome Admin!", "success")

            return redirect("/admin/dashboard")

    # ---------- Check Student ----------
    cur.execute(
        "SELECT * FROM students WHERE email=%s",
        (email,)
    )

    student = cur.fetchone()

    if student:

        if verify_password(password, student[6]):

            session.clear()
            session["student"] = student[0]
            session["student_name"] = student[1]

            flash("Login Successful", "success")

            return redirect("/student/dashboard")

    flash("Invalid Email or Password", "danger")

    return redirect("/login")


# ---------------- LOGOUT ---------------- #

@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect("/login")