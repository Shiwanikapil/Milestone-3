from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import textwrap
import os

def generate_pdf(title, author, summary_text):
    file_name = f"{title.replace(' ', '_')}_summary.pdf"
    file_path = os.path.join("uploads", file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    x_margin = 40
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, title)
    y -= 25

    # Author & Date
    c.setFont("Helvetica", 10)
    if author:
        c.drawString(x_margin, y, f"Author: {author}")
        y -= 15

    c.drawString(x_margin, y, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 25

    # Summary heading
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_margin, y, "Summary")
    y -= 20

    # Summary text
    c.setFont("Helvetica", 10)
    wrapped_lines = textwrap.wrap(summary_text, 90)

    for line in wrapped_lines:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
        c.drawString(x_margin, y, line)
        y -= 14

    c.save()
    return file_path