
def draw_centered_fit(pdf, text, x, y, font, max_size, min_size, max_width):
    """Center text and reduce its font size when it is too long."""
    size = max_size

    while size > min_size and stringWidth(text, font, size) > max_width:
        size -= 1

    pdf.setFont(font, size)
    pdf.drawCentredString(x, y, text)



import os

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


NAVY = HexColor("#102844")
GOLD = HexColor("#C5A052")
LIGHT_GOLD = HexColor("#E9D9AE")
IVORY = HexColor("#FFFEF8")
TEXT = HexColor("#354458")


def fit_centered_text(pdf, text, x, y, font, max_size, min_size, max_width):
    size = max_size

    while size > min_size and stringWidth(text, font, size) > max_width:
        size -= 1

    pdf.setFont(font, size)
    pdf.drawCentredString(x, y, text)


def draw_seal(pdf, x, y):
    # Decorative gold award seal
    pdf.setFillColor(LIGHT_GOLD)
    pdf.circle(x, y, 31, fill=1, stroke=0)

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.circle(x, y, 31, fill=0, stroke=1)
    pdf.circle(x, y, 25, fill=0, stroke=1)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawCentredString(x, y + 3, "AWARD")
    pdf.drawCentredString(x, y - 7, "OF MERIT")


def generate_certificate(name, course_name, recipient_id, certificate_id):
    os.makedirs("certificates", exist_ok=True)

    file_path = f"certificates/certificate_{recipient_id}.pdf"
    page_size = landscape(A4)
    pdf = canvas.Canvas(file_path, pagesize=page_size)
    width, height = page_size

    # Fixed background
    pdf.setFillColor(IVORY)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Luxury double frame
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(6)
    pdf.rect(22, 22, width - 44, height - 44)

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.rect(34, 34, width - 68, height - 68)

    # Decorative corner lines
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)

    for x, dx in [(43, 1), (width - 43, -1)]:
        for y, dy in [(43, 1), (height - 43, -1)]:
            pdf.line(x, y, x + 28 * dx, y)
            pdf.line(x, y, x, y + 28 * dy)

    # Subtle watermark
    pdf.saveState()
    pdf.setFillColor(HexColor("#F3EBD8"))
    pdf.setFont("Helvetica-Bold", 48)
    pdf.translate(width / 2, height / 2)
    pdf.rotate(25)
    pdf.drawCentredString(0, 0, "ACHIEVEMENT")
    pdf.restoreState()

    # Main content on top of watermark
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(width / 2, height - 91, "CERTIFICATE OF")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 29)
    pdf.drawCentredString(width / 2, height - 128, "COMPLETION")

    # Gold ornamental divider
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.line(190, height - 146, width - 190, height - 146)
    pdf.setFillColor(GOLD)
    pdf.circle(width / 2, height - 146, 3, fill=1, stroke=0)

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2, height - 184,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(NAVY)
    fit_centered_text(
        pdf, name, width / 2, height - 226,
        "Helvetica-Bold", 28, 14, width - 150
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)
    pdf.line(215, height - 240, width - 215, height - 240)

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        width / 2, height - 270,
        "for successfully completing the course"
    )

    # Course name
    pdf.setFillColor(NAVY)
    fit_centered_text(
        pdf, course_name, width / 2, height - 300,
        "Helvetica-Bold", 19, 11, width - 130
    )

    # Decorative achievement seal
    draw_seal(pdf, width / 2, 91)

    # Signature lines are intentionally blank for authorized signing
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)
    pdf.line(95, 91, 235, 91)
    pdf.line(width - 235, 91, width - 95, 91)

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(165, 76, "AUTHORIZED SIGNATURE")
    pdf.drawCentredString(width - 165, 76, "DATE / ISSUING AUTHORITY")

    # Unique verification ID
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(
        width / 2, 47,
        f"Certificate ID: {certificate_id}"
    )

    pdf.save()
    return file_path
