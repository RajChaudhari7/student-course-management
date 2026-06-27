from flask import Blueprint, render_template, request, redirect, flash
from MySQLdb.cursors import DictCursor

from utils.db import mysql
from utils.decorators import admin_required

marks = Blueprint("marks", __name__)

def calculate_grade(score):

    score = int(score)

    if score >= 90:
        return "A+"

    elif score >= 80:
        return "A"

    elif score >= 70:
        return "B"

    elif score >= 60:
        return "C"

    elif score >= 50:
        return "D"

    return "F"

@marks.route("/admin/marks")
@admin_required
def marks_page():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            id,
            full_name
        FROM students
        ORDER BY full_name
    """)

    students = cur.fetchall()

    cur.execute("""
        SELECT
            id,
            course_name
        FROM courses
        ORDER BY course_name
    """)

    courses = cur.fetchall()

    return render_template(
        "admin/add_marks.html",
        students=students,
        courses=courses
    )

@marks.route("/admin/marks", methods=["POST"])
@admin_required
def save_marks():

    student_id = request.form["student_id"]

    course_id = request.form["course_id"]

    marks_value = request.form["marks"]

    grade = calculate_grade(marks_value)

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO marks
        (
            student_id,
            course_id,
            marks,
            grade
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
    """,
    (
        student_id,
        course_id,
        marks_value,
        grade
    ))

    mysql.connection.commit()

    flash("Marks added successfully.", "success")

    return redirect("/admin/marks")

@marks.route("/admin/marks/list")
@admin_required
def marks_list():

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            marks.id,
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

    return render_template(
        "admin/marks_list.html",
        records=records
    )

@marks.route("/admin/marks/edit/<int:id>", methods=["GET","POST"])
@admin_required
def edit_marks(id):

    cur = mysql.connection.cursor(DictCursor)

    if request.method == "POST":

        score = request.form["marks"]

        grade = calculate_grade(score)

        cur.execute("""
            UPDATE marks
            SET
                marks=%s,
                grade=%s
            WHERE id=%s
        """,
        (
            score,
            grade,
            id
        ))

        mysql.connection.commit()

        flash("Marks updated successfully.","success")

        return redirect("/admin/marks/list")

    cur.execute("SELECT * FROM marks WHERE id=%s",(id,))

    mark = cur.fetchone()

    return render_template(
        "admin/edit_marks.html",
        mark=mark
    )

@marks.route("/admin/marks/delete/<int:id>")
@admin_required
def delete_marks(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM marks WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    flash("Marks deleted successfully.","success")

    return redirect("/admin/marks/list")