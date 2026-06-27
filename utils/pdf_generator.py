import os
import qrcode

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Image,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_student_id(student):

    pdf_path = os.path.join(
        "static",
        "idcards",
        f"student_{student['id']}.pdf"
    )

    qr_path = os.path.join(
        "static",
        "idcards",
        f"student_{student['id']}.png"
    )

    qr = qrcode.make(
        f"""
Student ID : {student['id']}
Name : {student['full_name']}
Email : {student['email']}
Department : {student['department']}
Semester : {student['semester']}
"""
    )

    qr.save(qr_path)

    doc = SimpleDocTemplate(pdf_path)

    elements = []

    elements.append(
        Paragraph(
            "<b><font size=18>Student Identity Card</font></b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    photo = Image(
        os.path.join(
            "static",
            "uploads",
            "profile",
            student["profile_image"]
        ),
        width=100,
        height=100
    )

    qr_image = Image(
        qr_path,
        width=100,
        height=100
    )

    data = [
        ["Photo", photo],
        ["Student ID", student["id"]],
        ["Name", student["full_name"]],
        ["Email", student["email"]],
        ["Phone", student["phone"]],
        ["Department", student["department"]],
        ["Semester", student["semester"]],
        ["QR Code", qr_image]
    ]

    table = Table(data, colWidths=[120, 300])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica")
    ]))

    elements.append(table)

    doc.build(elements)

    return pdf_path