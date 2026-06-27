from flask import Flask
from config import Config
from utils.db import mysql

from routes.auth import auth
from routes.admin import admin
from routes.student import student
from routes.course import course
import os
from werkzeug.utils import secure_filename
from routes.attendance import attendance
from routes.marks import marks
from routes.export import export

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/profile"

app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(student)
app.register_blueprint(course)
app.register_blueprint(attendance)
app.register_blueprint(marks)
app.register_blueprint(export)

if __name__ == "__main__":
    app.run(debug=True)