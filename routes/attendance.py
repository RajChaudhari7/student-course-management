from flask import Blueprint, render_template, request, redirect, flash
from MySQLdb.cursors import DictCursor
from utils.db import mysql
from utils.decorators import admin_required

attendance = Blueprint("attendance", __name__)

@attendance.route("/admin/attendance")
@admin_required
def attendance_page():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            id,
            full_name,
            department,
            semester
        FROM students
        ORDER BY full_name
    """)

    students = cur.fetchall()

    return render_template(
        "admin/attendance.html",
        students=students
    )

@attendance.route("/admin/attendance", methods=["POST"])
@admin_required
def save_attendance():

    cur = mysql.connection.cursor()

    date = request.form["date"]

    for key in request.form:

        if key.startswith("student_"):

            student_id = key.split("_")[1]

            status = request.form[key]

            cur.execute("""
                INSERT INTO attendance
                (
                    student_id,
                    attendance_date,
                    status
                )
                VALUES(%s,%s,%s)
            """,(
                student_id,
                date,
                status
            ))

    mysql.connection.commit()

    flash("Attendance saved successfully.","success")

    return redirect("/admin/attendance")

