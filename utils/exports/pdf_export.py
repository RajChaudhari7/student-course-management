from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from datetime import datetime

styles = getSampleStyleSheet()


def export_to_pdf(filename, report_title, headers, rows):

    doc = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph(
            "<b>Student Course Management System</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            report_title,
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "Generated on: "
            + datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    table_data = [headers]

    table_data.extend(rows)

    table = Table(table_data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0D6EFD")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Generated automatically by Student Course Management System.",
            styles["Italic"]
        )
    )

    doc.build(elements)

    return filename