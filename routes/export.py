from flask import (Blueprint,render_template,send_file,request)
from MySQLdb.cursors import DictCursor

from utils.db import mysql

from utils.decorators import admin_required

from utils.exports.excel_export import export_to_excel
from utils.exports.pdf_export import export_to_pdf

import os

export = Blueprint("export",__name__)

@export.route("/admin/export/students/excel")
@admin_required
def students_excel():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""

        SELECT

            id,

            full_name,

            email,

            phone,

            department,

            semester

        FROM students

    """)

    students = cur.fetchall()

    headers = [

        "ID",

        "Name",

        "Email",

        "Phone",

        "Department",

        "Semester"

    ]

    rows = []

    for s in students:

        rows.append([

            s["id"],

            s["full_name"],

            s["email"],

            s["phone"],

            s["department"],

            s["semester"]

        ])

    filename = os.path.join(

        "static",

        "exports",

        "students.xlsx"

    )

    export_to_excel(

        filename,

        "Student Report",

        headers,

        rows

    )

    return send_file(

        filename,

        as_attachment=True

    )

@export.route("/admin/export/students/pdf")
@admin_required
def students_pdf():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""

        SELECT

            id,

            full_name,

            email,

            phone,

            department,

            semester

        FROM students

    """)

    students = cur.fetchall()

    headers = [

        "ID",

        "Name",

        "Email",

        "Phone",

        "Department",

        "Semester"

    ]

    rows = []

    for s in students:

        rows.append([

            s["id"],

            s["full_name"],

            s["email"],

            s["phone"],

            s["department"],

            s["semester"]

        ])

    filename = os.path.join(

        "static",

        "exports",

        "students.pdf"

    )

    export_to_pdf(

        filename,

        "Student Report",

        headers,

        rows

    )

    return send_file(

        filename,

        as_attachment=True

    )

@export.route("/admin/export/courses/excel")
@admin_required
def courses_excel():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            id,
            course_name,
            course_code,
            credits
        FROM courses
        ORDER BY course_name
    """)

    courses = cur.fetchall()

    headers = [
        "ID",
        "Course Name",
        "Course Code",
        "Credits"
    ]

    rows = []

    for course in courses:

        rows.append([
            course["id"],
            course["course_name"],
            course["course_code"],
            course["credits"]
        ])

    filename = os.path.join(
        "static",
        "exports",
        "courses.xlsx"
    )

    export_to_excel(
        filename,
        "Course Report",
        headers,
        rows
    )

    return send_file(
        filename,
        as_attachment=True
    )

@export.route("/admin/export/courses/pdf")
@admin_required
def courses_pdf():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            id,
            course_name,
            course_code,
            credits
        FROM courses
        ORDER BY course_name
    """)

    courses = cur.fetchall()

    headers = [
        "ID",
        "Course Name",
        "Course Code",
        "Credits"
    ]

    rows = []

    for course in courses:

        rows.append([
            course["id"],
            course["course_name"],
            course["course_code"],
            course["credits"]
        ])

    filename = os.path.join(
        "static",
        "exports",
        "courses.pdf"
    )

    export_to_pdf(
        filename,
        "Course Report",
        headers,
        rows
    )

    return send_file(
        filename,
        as_attachment=True
    )

@export.route("/admin/export/attendance")
@admin_required
def attendance_export_page():

    return render_template(
        "admin/attendance_export.html"
    )

@export.route("/admin/export/attendance/excel")
@admin_required
def attendance_excel():

    date = request.args.get("date")

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""

        SELECT

            students.full_name,

            students.department,

            students.semester,

            attendance.attendance_date,

            attendance.status

        FROM attendance

        JOIN students

        ON attendance.student_id = students.id

        WHERE attendance.attendance_date=%s

        ORDER BY students.full_name

    """,(date,))

    records = cur.fetchall()

    headers = [

        "Student",

        "Department",

        "Semester",

        "Date",

        "Status"

    ]

    rows = []

    for row in records:

        rows.append([

            row["full_name"],

            row["department"],

            row["semester"],

            str(row["attendance_date"]),

            row["status"]

        ])

    filename = os.path.join(

        "static",

        "exports",

        f"attendance_{date}.xlsx"

    )

    export_to_excel(

        filename,

        "Attendance Report",

        headers,

        rows

    )

    return send_file(

        filename,

        as_attachment=True
    )

@export.route("/admin/export/attendance/pdf")
@admin_required
def attendance_pdf():

    date = request.args.get("date")

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""

        SELECT

            students.full_name,

            students.department,

            students.semester,

            attendance.attendance_date,

            attendance.status

        FROM attendance

        JOIN students

        ON attendance.student_id = students.id

        WHERE attendance.attendance_date=%s

        ORDER BY students.full_name

    """,(date,))

    records = cur.fetchall()

    headers = [

        "Student",

        "Department",

        "Semester",

        "Date",

        "Status"

    ]

    rows = []

    for row in records:

        rows.append([

            row["full_name"],

            row["department"],

            row["semester"],

            str(row["attendance_date"]),

            row["status"]

        ])

    filename = os.path.join(

        "static",

        "exports",

        f"attendance_{date}.pdf"

    )

    export_to_pdf(

        filename,

         "Attendance Report",

        headers,

        rows

    )

    return send_file(

        filename,

        as_attachment=True
    )

@export.route("/admin/export/marks/excel")
@admin_required
def marks_excel():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            students.full_name,
            courses.course_name,
            marks.marks,
            marks.grade
        FROM marks
        JOIN students
            ON marks.student_id = students.id
        JOIN courses
            ON marks.course_id = courses.id
        ORDER BY students.full_name
    """)

    records = cur.fetchall()

    headers = [
        "Student Name",
        "Course",
        "Marks",
        "Grade"
    ]

    rows = []

    for row in records:
        rows.append([
            row["full_name"],
            row["course_name"],
            row["marks"],
            row["grade"]
        ])

    filename = os.path.join(
        "static",
        "exports",
        "marks.xlsx"
    )

    export_to_excel(
        filename,
        "Marks Report",
        headers,
        rows
    )

    return send_file(
        filename,
        as_attachment=True
    )

@export.route("/admin/export/marks/pdf")
@admin_required
def marks_pdf():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            students.full_name,
            courses.course_name,
            marks.marks,
            marks.grade
        FROM marks
        JOIN students
            ON marks.student_id = students.id
        JOIN courses
            ON marks.course_id = courses.id
        ORDER BY students.full_name
    """)

    records = cur.fetchall()

    headers = [
        "Student Name",
        "Course",
        "Marks",
        "Grade"
    ]

    rows = []

    for row in records:
        rows.append([
            row["full_name"],
            row["course_name"],
            row["marks"],
            row["grade"]
        ])

    filename = os.path.join(
        "static",
        "exports",
        "marks.pdf"
    )

    export_to_pdf(
        filename,
        "Marks Report",
        headers,
        rows
    )

    return send_file(
        filename,
        as_attachment=True
    )