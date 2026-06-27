import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

styles = getSampleStyleSheet()


def generate_marksheet(student, records, summary):

    output_path = os.path.join(
        "static",
        "marksheets",
        f"marksheet_{student['id']}.pdf"
    )

    doc = SimpleDocTemplate(output_path)

    elements = []

    # College Heading

    elements.append(
        Paragraph(
            "<font size=22><b>Student Course Management System</b></font>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "<font size=14>Official Academic Marksheet</font>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 20))

    # Student Image

    image_path = os.path.join(
        "static",
        "uploads",
        "profile",
        student["profile_image"]
    )

    if os.path.exists(image_path):
        img = Image(image_path, width=1.2 * inch, height=1.2 * inch)
        elements.append(img)

    elements.append(Spacer(1, 15))

    # Student Information

    info = [
        ["Student ID", student["id"]],
        ["Name", student["full_name"]],
        ["Department", student["department"]],
        ["Semester", student["semester"]],
        ["Email", student["email"]],
        ["Phone", student["phone"]]
    ]

    info_table = Table(info, colWidths=[130, 300])

    info_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 20))

    # Marks Table

    data = [["Course", "Code", "Marks", "Grade"]]

    for row in records:

        data.append([
            row["course_name"],
            row["course_code"],
            row["marks"],
            row["grade"]
        ])

    marks_table = Table(data)

    marks_table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10)

    ]))

    elements.append(marks_table)

    elements.append(Spacer(1, 20))

    # Summary

    summary_table = Table([

        ["Total Subjects", summary["subjects"]],

        ["Total Marks", summary["marks"]],

        ["Percentage", f'{summary["percentage"]}%'],

        ["GPA", summary["gpa"]],

        ["Overall Grade", summary["grade"]]

    ])

    summary_table.setStyle(TableStyle([

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 0), (0, -1), colors.lightblue)

    ]))

    elements.append(summary_table)

    elements.append(Spacer(1, 30))

    elements.append(

        Paragraph(

            f"Issue Date : {datetime.now().strftime('%d-%m-%Y')}",

            styles["Normal"]

        )

    )

    elements.append(Spacer(1, 40))

    elements.append(

        Paragraph(

            "<b>Principal Signature</b>",

            styles["Normal"]

        )

    )

    doc.build(elements)

    return output_path