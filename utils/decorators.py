from functools import wraps
from flask import session, redirect, flash


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "admin" not in session:

            flash("Please login first", "warning")

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


def student_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "student" not in session:

            flash("Please login first", "warning")

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper