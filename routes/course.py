from flask import Blueprint, render_template, request, redirect, flash
from utils.db import mysql
from utils.decorators import admin_required

course = Blueprint("course", __name__)


# ---------------- VIEW COURSES ---------------- #

@course.route("/admin/courses")
@admin_required
def courses():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,
               course_name,
               course_code,
               credits
        FROM courses
        ORDER BY id DESC
    """)

    courses = cur.fetchall()

    return render_template(
        "admin/courses.html",
        courses=courses
    )


# ---------------- ADD COURSE ---------------- #

@course.route("/admin/course/add", methods=["GET", "POST"])
@admin_required
def add_course():

    if request.method == "POST":

        course_name = request.form["course_name"]
        course_code = request.form["course_code"]
        credits = request.form["credits"]

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO courses
            (course_name, course_code, credits)
            VALUES(%s,%s,%s)
        """, (
            course_name,
            course_code,
            credits
        ))

        mysql.connection.commit()

        flash("Course Added Successfully", "success")

        return redirect("/admin/courses")

    return render_template("admin/add_course.html")


# ---------------- EDIT COURSE ---------------- #

@course.route("/admin/course/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_course(id):

    cur = mysql.connection.cursor()

    if request.method == "POST":

        course_name = request.form["course_name"]
        course_code = request.form["course_code"]
        credits = request.form["credits"]

        cur.execute("""
            UPDATE courses
            SET
                course_name=%s,
                course_code=%s,
                credits=%s
            WHERE id=%s
        """, (
            course_name,
            course_code,
            credits,
            id
        ))

        mysql.connection.commit()

        flash("Course Updated Successfully", "success")

        return redirect("/admin/courses")

    cur.execute("""
        SELECT *
        FROM courses
        WHERE id=%s
    """, (id,))

    course = cur.fetchone()

    return render_template(
        "admin/edit_course.html",
        course=course
    )


# ---------------- DELETE COURSE ---------------- #

@course.route("/admin/course/delete/<int:id>")
@admin_required
def delete_course(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM courses WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    flash("Course Deleted Successfully", "success")

    return redirect("/admin/courses")


# ---------------- SEARCH COURSE ---------------- #

@course.route("/admin/course/search")
@admin_required
def search_course():

    keyword = request.args.get("keyword", "")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,
               course_name,
               course_code,
               credits
        FROM courses
        WHERE course_name LIKE %s
           OR course_code LIKE %s
        ORDER BY id DESC
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    courses = cur.fetchall()

    return render_template(
        "admin/courses.html",
        courses=courses
    )

# ---------------- ASSIGN COURSE ---------------- #

@course.route("/admin/enroll", methods=["GET", "POST"])
@admin_required
def enroll_student():

    cur = mysql.connection.cursor()

    if request.method == "POST":

        student_id = request.form["student_id"]
        course_id = request.form["course_id"]

        # Check duplicate enrollment
        cur.execute("""
            SELECT id
            FROM enrollments
            WHERE student_id=%s
            AND course_id=%s
        """, (student_id, course_id))

        enrollment = cur.fetchone()

        if enrollment:

            flash("Student is already enrolled in this course.", "warning")
            return redirect("/admin/enroll")

        # Insert enrollment
        cur.execute("""
            INSERT INTO enrollments(student_id, course_id)
            VALUES(%s,%s)
        """, (student_id, course_id))

        mysql.connection.commit()

        flash("Course assigned successfully.", "success")

        return redirect("/admin/enroll")

    # Load students
    cur.execute("""
        SELECT id, full_name
        FROM students
        ORDER BY full_name
    """)
    students = cur.fetchall()

    # Load courses
    cur.execute("""
        SELECT id, course_name
        FROM courses
        ORDER BY course_name
    """)
    courses = cur.fetchall()

    return render_template(
        "admin/enroll.html",
        students=students,
        courses=courses
    )

# ---------------- VIEW ENROLLMENTS ---------------- #

@course.route("/admin/enrollments")
@admin_required
def enrollments():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            enrollments.id,
            students.full_name,
            students.department,
            courses.course_name,
            courses.course_code
        FROM enrollments
        JOIN students
        ON enrollments.student_id = students.id
        JOIN courses
        ON enrollments.course_id = courses.id
        ORDER BY students.full_name
    """)

    enrollments = cur.fetchall()

    return render_template(
        "admin/enrollments.html",
        enrollments=enrollments
    )

# ---------------- DELETE ENROLLMENT ---------------- #

@course.route("/admin/enrollment/delete/<int:id>")
@admin_required
def delete_enrollment(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM enrollments WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    flash("Enrollment removed successfully.", "success")

    return redirect("/admin/enrollments")