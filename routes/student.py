from flask import Blueprint, render_template, session, request, redirect, flash,current_app
from utils.db import mysql
from utils.decorators import student_required
from utils.auth import hash_password, verify_password
import os
from werkzeug.utils import secure_filename
from flask import send_file
from utils.pdf_generator import generate_student_id
from MySQLdb.cursors import DictCursor
from utils.marksheet_generator import generate_marksheet

student = Blueprint("student", __name__)


@student.route("/student/dashboard")
@student_required
def dashboard():

    student_id = session["student"]

    cur = mysql.connection.cursor()

    # Student Details
    cur.execute("""
        SELECT
    full_name,
    email,
    phone,
    department,
    semester,
    profile_image
FROM students
WHERE id=%s
    """, (student_id,))

    profile = cur.fetchone()

    # Total Enrolled Courses
    cur.execute("""
        SELECT COUNT(*)
        FROM enrollments
        WHERE student_id=%s
    """, (student_id,))

    total_courses = cur.fetchone()[0]

    # My Courses
    cur.execute("""
        SELECT
            courses.course_name,
            courses.course_code,
            courses.credits
        FROM enrollments

        JOIN courses
        ON enrollments.course_id = courses.id

        WHERE enrollments.student_id=%s
    """, (student_id,))

    courses = cur.fetchall()

    return render_template(
        "student/dashboard.html",
        profile=profile,
        courses=courses,
        total_courses=total_courses
    )

@student.route("/student/profile", methods=["GET", "POST"])
@student_required
def profile():

    student_id = session["student"]

    cur = mysql.connection.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]
        department = request.form["department"]
        semester = request.form["semester"]
        image = request.files.get("profile_image")

        filename = None

        if image and image.filename:

            filename = secure_filename(image.filename)

        image.save(
        os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )
    )

        cur.execute("""
           UPDATE students
            SET
            full_name=%s,
            phone=%s,
            department=%s,
            semester=%s,
            profile_image=COALESCE(%s, profile_image)
            WHERE id=%s
        """, (
    full_name,
    phone,
    department,
    semester,
    filename,
    student_id
))

        mysql.connection.commit()

        flash("Profile updated successfully.", "success")

        return redirect("/student/profile")

    cur.execute("""
        SELECT
full_name,
email,
phone,
department,
semester,
profile_image
        FROM students
        WHERE id=%s
    """, (student_id,))

    profile = cur.fetchone()

    return render_template(
        "student/profile.html",
        profile=profile
    )

@student.route("/student/change-password", methods=["GET", "POST"])
@student_required
def change_password():

    student_id = session["student"]

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:

            flash("New passwords do not match.", "danger")
            return redirect("/student/change-password")

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT password
            FROM students
            WHERE id=%s
        """, (student_id,))

        result = cur.fetchone()

        if not verify_password(current_password, result[0]):

            flash("Current password is incorrect.", "danger")
            return redirect("/student/change-password")

        hashed_password = hash_password(new_password)

        cur.execute("""
            UPDATE students
            SET password=%s
            WHERE id=%s
        """, (
            hashed_password,
            student_id
        ))

        mysql.connection.commit()

        flash("Password changed successfully.", "success")

        return redirect("/student/dashboard")

    return render_template("student/change_password.html")

@student.route("/student/id-card")
@student_required
def id_card():

    student_id = session["student"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            department,
            semester,
            profile_image
        FROM students
        WHERE id=%s
    """, (student_id,))

    row = cur.fetchone()

    student = {
        "id": row[0],
        "full_name": row[1],
        "email": row[2],
        "phone": row[3],
        "department": row[4],
        "semester": row[5],
        "profile_image": row[6]
    }

    pdf = generate_student_id(student)

    return send_file(pdf, as_attachment=True)

@student.route("/student/attendance")
@student_required
def attendance():

    student_id = session["student"]

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            attendance_date,
            status
        FROM attendance
        WHERE student_id=%s
        ORDER BY attendance_date DESC
    """,(student_id,))

    records = cur.fetchall()

    return render_template(
        "student/attendance.html",
        records=records
    )

@student.route("/student/marks")
@student_required
def student_marks():

    student_id = session["student"]

    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        SELECT
            courses.course_name,
            courses.course_code,
            marks.marks,
            marks.grade
        FROM marks

        JOIN courses
            ON marks.course_id = courses.id

        WHERE marks.student_id = %s
        ORDER BY courses.course_name
    """, (student_id,))

    records = cur.fetchall()

    total_marks = sum(row["marks"] for row in records)
    total_subjects = len(records)

    percentage = (
        round(total_marks / total_subjects, 2)
        if total_subjects > 0 else 0
    )

    gpa = round((percentage / 10), 2)

    if percentage >= 90:
        overall_grade = "A+"
    elif percentage >= 80:
        overall_grade = "A"
    elif percentage >= 70:
        overall_grade = "B"
    elif percentage >= 60:
        overall_grade = "C"
    elif percentage >= 50:
        overall_grade = "D"
    else:
        overall_grade = "F"

    return render_template(
        "student/marks.html",
        records=records,
        total_marks=total_marks,
        total_subjects=total_subjects,
        percentage=percentage,
        gpa=gpa,
        overall_grade=overall_grade
    )

@student.route("/student/marksheet/pdf")
@student_required
def download_marksheet():

    student_id = session["student"]

    cur = mysql.connection.cursor(DictCursor)

    # Student Details
    cur.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            department,
            semester,
            profile_image
        FROM students
        WHERE id=%s
    """, (student_id,))

    student = cur.fetchone()

    # Marks
    cur.execute("""
        SELECT
            courses.course_name,
            courses.course_code,
            marks.marks,
            marks.grade
        FROM marks

        JOIN courses
            ON marks.course_id = courses.id

        WHERE marks.student_id=%s
        ORDER BY courses.course_name
    """, (student_id,))

    records = cur.fetchall()

    total_marks = sum(r["marks"] for r in records)
    total_subjects = len(records)

    percentage = round(
        total_marks / total_subjects,
        2
    ) if total_subjects else 0

    gpa = round(percentage / 10, 2)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    summary = {
        "subjects": total_subjects,
        "marks": total_marks,
        "percentage": percentage,
        "gpa": gpa,
        "grade": grade
    }

    pdf = generate_marksheet(
        student,
        records,
        summary
    )

    return send_file(
        pdf,
        as_attachment=True
    )