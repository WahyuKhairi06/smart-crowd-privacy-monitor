"""
report_generator.py
Menghasilkan laporan PDF (report.pdf) dari hasil analisis menggunakan ReportLab.
"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Flip7-inspired palette (hex -> reportlab color)
PRIMARY_DARK = colors.HexColor("#1E8C86")
PRIMARY_TEAL = colors.HexColor("#2BA8A2")
ACCENT_GOLD = colors.HexColor("#FFD23F")
CORAL = colors.HexColor("#EF6C4A")
SUCCESS = colors.HexColor("#27AE60")
CREAM = colors.HexColor("#FFF8E7")

DENSITY_COLOR_MAP = {
    "Low": SUCCESS,
    "Medium": ACCENT_GOLD,
    "High": CORAL,
}


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleFlip7",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=PRIMARY_DARK,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="SubtitleFlip7",
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=18,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=PRIMARY_TEAL,
        spaceBefore=14,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="BodyFlip7",
        fontName="Helvetica",
        fontSize=10.5,
        textColor=colors.black,
        alignment=TA_LEFT,
        leading=15,
    ))

    return styles


def generate_pdf_report(image_path: str,
                         face_count: int,
                         density_level: str,
                         timestamp: str,
                         output_dir: str = "outputs/reports") -> str:
    """
    Membuat laporan PDF berisi hasil analisis crowd privacy monitoring.

    Parameters
    ----------
    image_path : str
        Path gambar hasil blur (protected image).
    face_count : int
        Jumlah wajah yang terdeteksi.
    density_level : str
        Tingkat kepadatan (Low/Medium/High).
    timestamp : str
        Timestamp proses (format YYYYMMDD_HHMMSS).
    output_dir : str
        Folder tujuan penyimpanan PDF.

    Returns
    -------
    str
        Path file PDF yang dihasilkan.
    """
    os.makedirs(output_dir, exist_ok=True)

    pdf_filename = f"report_{timestamp}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    styles = _build_styles()
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    elements = []

    # --- Header ---
    elements.append(Paragraph("Smart Crowd Privacy Monitoring System", styles["TitleFlip7"]))
    elements.append(Paragraph(
        "Laporan Analisis Kepadatan Keramaian Berbasis Web "
        "(Haar Cascade &amp; Gaussian Blur)",
        styles["SubtitleFlip7"]
    ))
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_TEAL, spaceAfter=12))

    # --- Info Analisis ---
    elements.append(Paragraph("Informasi Analisis", styles["SectionHeader"]))

    try:
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        readable_time = dt.strftime("%d %B %Y, %H:%M:%S")
    except ValueError:
        readable_time = timestamp

    density_color = DENSITY_COLOR_MAP.get(density_level, PRIMARY_TEAL)

    info_table_data = [
        ["Waktu Analisis", readable_time],
        ["Jumlah Wajah Terdeteksi", str(face_count)],
        ["Tingkat Kepadatan", density_level],
    ]

    info_table = Table(info_table_data, colWidths=[6 * cm, 10 * cm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (0, -1), PRIMARY_DARK),
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.75, PRIMARY_TEAL),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        # Highlight density row with its color
        ("TEXTCOLOR", (1, 2), (1, 2), density_color),
        ("FONTNAME", (1, 2), (1, 2), "Helvetica-Bold"),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 16))

    # --- Gambar Hasil ---
    elements.append(Paragraph("Gambar Hasil (Wajah Tersamarkan)", styles["SectionHeader"]))

    if image_path and os.path.exists(image_path):
        img = Image(image_path)
        # Batasi ukuran gambar agar tidak melebihi halaman
        max_width = 16 * cm
        if img.drawWidth > max_width:
            ratio = max_width / img.drawWidth
            img.drawWidth *= ratio
            img.drawHeight *= ratio
        elements.append(img)
    else:
        elements.append(Paragraph("Gambar tidak ditemukan.", styles["BodyFlip7"]))

    elements.append(Spacer(1, 16))

    # --- Catatan Privasi ---
    elements.append(Paragraph("Catatan Privasi", styles["SectionHeader"]))
    elements.append(Paragraph(
        "Seluruh wajah yang terdeteksi pada gambar telah disamarkan menggunakan "
        "metode Gaussian Blur untuk melindungi privasi individu sebelum gambar "
        "ditampilkan atau disimpan dalam sistem.",
        styles["BodyFlip7"]
    ))

    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=8))
    elements.append(Paragraph(
        "Dihasilkan secara otomatis oleh Smart Crowd Privacy Monitoring System.",
        styles["SubtitleFlip7"]
    ))

    doc.build(elements)
    return pdf_path
