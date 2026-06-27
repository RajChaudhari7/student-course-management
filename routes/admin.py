from flask import Blueprint, render_template, request, redirect, flash, session
from utils.db import mysql
from utils.decorators import admin_required
from utils.auth import hash_password
from MySQLdb.cursors import DictCursor
from datetime import date

admin = Blueprint("admin", __name__)

# ---------------- Dashboard ---------------- #

@admin.route("/admin/dashboard")
@admin_required
def dashboard():

    cur = mysql.connection.cursor(DictCursor)

    # Students Count
    cur.execute("SELECT COUNT(*) AS total FROM students")
    students = cur.fetchone()["total"]

    # Courses Count
    cur.execute("SELECT COUNT(*) AS total FROM courses")
    courses = cur.fetchone()["total"]

    # Attendance Count
    cur.execute("SELECT COUNT(*) AS total FROM attendance")
    attendance = cur.fetchone()["total"]

    # Marks Count
    cur.execute("SELECT COUNT(*) AS total FROM marks")
    marks = cur.fetchone()["total"]

    # Recent Students
    cur.execute("""
        SELECT
            full_name,
            department,
            semester
        FROM students
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_students = cur.fetchall()

    # Recent Courses
    cur.execute("""
        SELECT
            course_name,
            course_code,
            credits
        FROM courses
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_courses = cur.fetchall()

    # Top 5 Students by Average Marks
    cur.execute("""
    SELECT
        students.full_name,
        ROUND(AVG(marks.marks),2) AS average_marks
    FROM marks
    JOIN students
        ON marks.student_id = students.id
    GROUP BY students.id
    ORDER BY average_marks DESC
    LIMIT 5
    """)
    
    #Todays Attendance

    today = date.today()

    cur.execute("""
    SELECT
        COUNT(*) AS total
    FROM attendance
    WHERE attendance_date=%s
    """, (today,))

    today_attendance = cur.fetchone()["total"]

    top_students = cur.fetchall()

    return render_template(
    "admin/dashboard.html",
    students=students,
    courses=courses,
    attendance=attendance,
    marks=marks,
    recent_students=recent_students,
    recent_courses=recent_courses,
    top_students=top_students,
    today_attendance=today_attendance,
    chart_data={
        "students": students,
        "courses": courses,
        "attendance": attendance,
        "marks": marks
    }
)

# ---------------- View Students ---------------- #

@admin.route("/admin/students")
@admin_required
def students():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,
               full_name,
               email,
               phone,
               department,
               semester
        FROM students
        ORDER BY id DESC
    """)

    students = cur.fetchall()

    return render_template(
        "admin/students.html",
        students=students
    )


# ---------------- Add Student ---------------- #

@admin.route("/admin/student/add", methods=["GET", "POST"])
@admin_required
def add_student():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        semester = request.form["semester"]
        password = hash_password(request.form["password"])

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO students
            (full_name,email,phone,department,semester,password)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            full_name,
            email,
            phone,
            department,
            semester,
            password
        ))

        mysql.connection.commit()

        flash("Student Added Successfully", "success")

        return redirect("/admin/students")

    return render_template("admin/add_student.html")

# ---------------- Edit Student ---------------- #

@admin.route("/admin/student/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_student(id):

    cur = mysql.connection.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        semester = request.form["semester"]

        cur.execute("""
            UPDATE students
            SET full_name=%s,
                email=%s,
                phone=%s,
                department=%s,
                semester=%s
            WHERE id=%s
        """, (
            full_name,
            email,
            phone,
            department,
            semester,
            id
        ))

        mysql.connection.commit()

        flash("Student Updated Successfully", "success")

        return redirect("/admin/students")

    cur.execute("""
        SELECT id,
               full_name,
               email,
               phone,
               department,
               semester
        FROM students
        WHERE id=%s
    """, (id,))

    student = cur.fetchone()

    return render_template(
        "admin/edit_student.html",
        student=student
    )

# ---------------- Delete Student ---------------- #

@admin.route("/admin/student/delete/<int:id>")
@admin_required
def delete_student(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    flash("Student Deleted Successfully", "success")

    return redirect("/admin/students")

# ---------------- Search Student ---------------- #

@admin.route("/admin/student/search")
@admin_required
def search_student():

    keyword = request.args.get("keyword", "")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,
               full_name,
               email,
               phone,
               department,
               semester
        FROM students
        WHERE full_name LIKE %s
           OR email LIKE %s
           OR department LIKE %s
        ORDER BY id DESC
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    students = cur.fetchall()

    return render_template(
        "admin/students.html",
        students=students
    )