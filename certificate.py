from __future__ import annotations
from datetime import datetime
from io import BytesIO
import hashlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from database import create_certificate, get_certificate


PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)


def make_certificate_id(user_id: int, email: str, issued_date: str) -> str:
    digest = hashlib.sha256(f"{user_id}|{email}|{issued_date}".encode()).hexdigest()[:10]
    return f"CSAT-{issued_date.replace('-', '')}-{digest.upper()}"


def _fit_text(c: canvas.Canvas, text: str, font_name: str, max_size: int, max_width: float) -> int:
    size = max_size
    while size > 18 and stringWidth(text, font_name, size) > max_width:
        size -= 1
    return size


def generate_certificate_pdf(user: dict, certificate: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    c.setTitle("Cybersecurity Awareness Training Certificate")
    c.setAuthor("Cybersecurity Awareness Training Tool")

    navy = colors.HexColor("#102A43")
    blue = colors.HexColor("#1769AA")
    gold = colors.HexColor("#C89B3C")
    pale = colors.HexColor("#F5F8FC")
    charcoal = colors.HexColor("#263238")

    # Background and layered borders
    c.setFillColor(pale)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    c.setStrokeColor(navy)
    c.setLineWidth(3)
    c.rect(10 * mm, 10 * mm, PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 20 * mm)

    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.rect(15 * mm, 15 * mm, PAGE_WIDTH - 30 * mm, PAGE_HEIGHT - 30 * mm)

    # Header band
    c.setFillColor(navy)
    c.rect(15 * mm, PAGE_HEIGHT - 48 * mm, PAGE_WIDTH - 30 * mm, 33 * mm, fill=1, stroke=0)

    # Shield mark
    shield_x, shield_y = 31 * mm, PAGE_HEIGHT - 31.5 * mm
    c.setFillColor(gold)
    path = c.beginPath()
    path.moveTo(shield_x, shield_y + 10 * mm)
    path.lineTo(shield_x + 8 * mm, shield_y + 7 * mm)
    path.lineTo(shield_x + 7 * mm, shield_y - 4 * mm)
    path.curveTo(shield_x + 5 * mm, shield_y - 9 * mm, shield_x, shield_y - 12 * mm, shield_x, shield_y - 12 * mm)
    path.curveTo(shield_x, shield_y - 12 * mm, shield_x - 5 * mm, shield_y - 9 * mm, shield_x - 7 * mm, shield_y - 4 * mm)
    path.lineTo(shield_x - 8 * mm, shield_y + 7 * mm)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(shield_x, shield_y - 2 * mm, "✓")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 25)
    c.drawString(47 * mm, PAGE_HEIGHT - 30 * mm, "CYBERSECURITY AWARENESS")
    c.setFont("Helvetica", 12)
    c.drawString(47 * mm, PAGE_HEIGHT - 39 * mm, "Training and assessment programme")

    # Main title
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 67 * mm, "CERTIFICATE OF COMPLETION")

    c.setStrokeColor(gold)
    c.setLineWidth(1)
    c.line(68 * mm, PAGE_HEIGHT - 73 * mm, PAGE_WIDTH - 68 * mm, PAGE_HEIGHT - 73 * mm)

    c.setFillColor(charcoal)
    c.setFont("Helvetica", 13)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 86 * mm, "This certificate is proudly presented to")

    name = user["full_name"].upper()
    name_size = _fit_text(c, name, "Helvetica-Bold", 29, PAGE_WIDTH - 70 * mm)
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", name_size)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 105 * mm, name)

    c.setStrokeColor(colors.HexColor("#B8C7D9"))
    c.line(55 * mm, PAGE_HEIGHT - 111 * mm, PAGE_WIDTH - 55 * mm, PAGE_HEIGHT - 111 * mm)

    body_style = ParagraphStyle(
        "certificate_body",
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=charcoal,
    )
    body_text = (
        "for successfully completing the <b>Cybersecurity Awareness Training Programme</b> "
        "and demonstrating knowledge of phishing prevention, password security, "
        "social engineering awareness and safe online behaviour."
    )
    p = Paragraph(body_text, body_style)
    w, h = p.wrap(PAGE_WIDTH - 70 * mm, 45 * mm)
    p.drawOn(c, (PAGE_WIDTH - w) / 2, PAGE_HEIGHT - 143 * mm)

    # Information panel
    panel_y = 31 * mm
    panel_h = 29 * mm
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#D5DFEA"))
    c.roundRect(26 * mm, panel_y, PAGE_WIDTH - 52 * mm, panel_h, 4 * mm, fill=1, stroke=1)

    issue_dt = datetime.fromisoformat(certificate["issued_at"].replace("Z", "+00:00"))
    issue_date = issue_dt.strftime("%d %B %Y")
    score_text = f'{certificate["score"]}/{certificate["total"]} ({certificate["percentage"]:.0f}%)'

    columns = [
        ("ORGANISATION", user["organisation"]),
        ("ASSESSMENT SCORE", score_text),
        ("DATE ISSUED", issue_date),
        ("CERTIFICATE ID", certificate["certificate_id"]),
    ]
    col_w = (PAGE_WIDTH - 52 * mm) / 4
    for i, (label, value) in enumerate(columns):
        x = 26 * mm + i * col_w
        if i:
            c.setStrokeColor(colors.HexColor("#E0E7EF"))
            c.line(x, panel_y + 5 * mm, x, panel_y + panel_h - 5 * mm)
        c.setFillColor(colors.HexColor("#607D8B"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(x + col_w / 2, panel_y + 18.5 * mm, label)
        c.setFillColor(navy)
        value_size = 10
        while value_size > 7 and stringWidth(str(value), "Helvetica-Bold", value_size) > col_w - 8 * mm:
            value_size -= 0.5
        c.setFont("Helvetica-Bold", value_size)
        c.drawCentredString(x + col_w / 2, panel_y + 9 * mm, str(value))

    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(
        PAGE_WIDTH / 2,
        20 * mm,
        "Issued electronically after successful completion of the assessment. "
        "Certificate authenticity can be checked using the unique certificate ID."
    )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def get_or_create_certificate(user: dict, score: int, total: int, percentage: float) -> dict:
    existing = get_certificate(user["id"])
    if existing:
        return existing

    issued_date = datetime.utcnow().strftime("%Y-%m-%d")
    certificate_id = make_certificate_id(user["id"], user["email"], issued_date)
    return create_certificate(
        user_id=user["id"],
        certificate_id=certificate_id,
        score=score,
        total=total,
        percentage=percentage,
    )
