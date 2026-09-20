#!/usr/bin/env python3
import csv, json, pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
PUB = ROOT / "public"

# Ensure public exists
PUB.mkdir(exist_ok=True)

# Copy CSV to public
import shutil
shutil.copy(ROOT / "data" / "reviews.csv", PUB / "reviews.csv")
shutil.copy(ROOT / "data" / "reviews.csv", OUT / "reviews_export.csv")
print("Copied CSV to public/reviews.csv")

# Generate Excel via openpyxl
try:
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reviews"
    with open(ROOT / "data" / "reviews.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ws.append(reader.fieldnames)
        for row in reader:
            ws.append([row.get(k,"") for k in reader.fieldnames])
    # Style header
    from openpyxl.styles import Font, PatternFill, Alignment
    header_fill = PatternFill(start_color="0f172a", end_color="0f172a", fill_type="solid")
    for c in ws[1]:
        c.font = Font(color="FFFFFF", bold=True, size=11)
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")
    ws.freeze_panes = "A2"
    # Auto width
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len+2, 50)
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(OUT / "reviews.xlsx")
    wb.save(PUB / "reviews.xlsx")
    print(f"Created Excel: {OUT/'reviews.xlsx'} ({(OUT/'reviews.xlsx').stat().st_size/1024:.1f} KB)")
except Exception as e:
    print(f"Excel failed (pip install openpyxl?): {e}")

# Generate PDF via reportlab if available else via pillow
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib import colors
    note = (ROOT / "output" / "weekly_note_latest.md").read_text(encoding="utf-8")
    pdf_path = OUT / "weekly_note.pdf"
    pub_pdf = PUB / "weekly_note.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=15*mm, title="Weekly Pulse — INDMoney")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title2', parent=styles['Title'], fontSize=18, leading=20, textColor=colors.HexColor("#0f172a"), alignment=TA_CENTER, spaceAfter=6)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, leading=14, textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=9.5, leading=13, textColor=colors.HexColor("#334155"))
    quote_style = ParagraphStyle('Quote', parent=styles['BodyText'], fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), leftIndent=10, borderPadding=(6,6,6), textColor2=colors.HexColor("#475569"))
    small_style = ParagraphStyle('Small', parent=styles['BodyText'], fontSize=7.5, leading=9, textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER)
    story = []
    story.append(Paragraph("Weekly Pulse — INDMoney", title_style))
    story.append(Paragraph("Week 38  (2026-08-05 → 2026-09-18)  •  Health: 2.88★ avg • 48 reviews (12w) • 232 words • No PII", ParagraphStyle('sub', parent=body_style, alignment=TA_CENTER, textColor=colors.HexColor("#64748b"), fontSize=8)))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#e2e8f0")))
    # Parse note roughly: split lines
    for line in note.splitlines():
        line=line.strip()
        if not line:
            story.append(Spacer(1,4))
            continue
        if line.startswith("# "):
            continue # already title
        if line.startswith("**Health:**"):
            story.append(Paragraph(line.replace("**","<b>").replace("**","</b>") if "**" in line else line, body_style))
        elif line.startswith("**Top") or line.startswith("**What") or line.startswith("**3 Action"):
            clean = line.replace("**","").strip(":")
            story.append(Paragraph(f"<b>{clean}</b>", h2_style))
        elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("- "):
            story.append(Paragraph(line, body_style))
        elif line.startswith(">"):
            story.append(Paragraph(line.replace(">","").strip().replace("“","<i>“").replace("”","”</i>"), quote_style))
        elif line.startswith("*Source"):
            story.append(Spacer(1,6))
            story.append(Paragraph(line.replace("*",""), small_style))
        else:
            story.append(Paragraph(line, body_style))
    doc.build(story)
    shutil.copy(pdf_path, pub_pdf)
    print(f"Created PDF: {pdf_path} ({pdf_path.stat().st_size/1024:.1f} KB)")
except Exception as e:
    print(f"PDF reportlab failed: {e}")
    # Fallback to pillow image pdf
    try:
        from PIL import Image, ImageDraw, ImageFont
        note = (ROOT / "output" / "weekly_note_latest.md").read_text(encoding="utf-8")
        W,H = 1240, 1754 # A4 at 150dpi
        img = Image.new("RGB", (W,H), "white")
        draw = ImageDraw.Draw(img)
        try:
            f_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            f_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        except:
            f_title = ImageFont.load_default()
            f_body = ImageFont.load_default()
        draw.text((60,40), "Weekly Pulse — INDMoney", fill="#0f172a", font=f_title)
        y=100
        for line in note.splitlines()[:40]:
            draw.text((60,y), line[:120], fill="#334155", font=f_body)
            y+=22
        pdf_path = OUT / "weekly_note.pdf"
        pub_pdf = PUB / "weekly_note.pdf"
        img.save(pdf_path, "PDF")
        shutil.copy(pdf_path, pub_pdf)
        print(f"Fallback PDF created: {pdf_path}")
    except Exception as e2:
        print(f"Fallback also failed: {e2}")

# Generate Image PNG of note via PIL
try:
    from PIL import Image, ImageDraw, ImageFont
    note = (ROOT / "output" / "weekly_note_latest.md").read_text(encoding="utf-8")
    # Create tall image
    W = 1000
    # Estimate height
    lines = note.splitlines()
    H = 80 + len(lines)*26 + 120
    H = max(H, 800)
    img = Image.new("RGB", (W, H), "#f8fafc")
    draw = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        f_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        f_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        f_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
    except:
        f_title = f_sub = f_body = f_small = ImageFont.load_default()
    # Header
    draw.rounded_rectangle([20,20,W-20,90], radius=12, fill="#0f172a")
    draw.text((40,38), "Weekly Pulse — INDMoney  •  Week 38", fill="white", font=f_title)
    draw.text((40,68), "2026-08-05 → 2026-09-18 • 2.88★ avg • 48 reviews • 232 words • No PII", fill="#cbd5e1", font=f_sub)
    y = 120
    # Card
    draw.rounded_rectangle([20,y,W-20,H-20], radius=12, fill="white", outline="#e2e8f0")
    y+=20
    for line in lines:
        if not line.strip():
            y+=8
            continue
        # Remove markdown markers for image
        clean = line.replace("**","").replace("# ","").replace("> ","“ ").replace("*","")
        color = "#0f172a" if line.startswith("#") or line.startswith("**Top") or line.startswith("**What") or line.startswith("**3 Action") else "#334155"
        font = f_body
        if line.startswith("#"):
            font = f_title
            color="#0f172a"
        elif line.startswith(">"):
            color="#475569"
        draw.text((40,y), clean[:110], fill=color, font=font)
        y+=22
    draw.text((40,H-30), "Source: 48 public reviews (App Store + Play Store) • No PII  •  INDMoney — same as LIP Challenge 4", fill="#94a3b8", font=f_small)
    png_path = OUT / "weekly_note.png"
    pub_png = PUB / "weekly_note.png"
    img.save(png_path, "PNG")
    shutil.copy(png_path, pub_png)
    print(f"Created PNG: {png_path} ({png_path.stat().st_size/1024:.1f} KB) {W}x{H}")
except Exception as e:
    print(f"PNG failed: {e}")

print("Done. Public files:", list(PUB.glob("*")))
