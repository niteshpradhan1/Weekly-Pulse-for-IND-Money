#!/usr/bin/env python3
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont
import pathlib, textwrap
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "final_demo.mp4"
W, H = 1280, 720
FPS = 30

def load_font(size, bold=False):
    try:
        # Use Helvetica
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        return ImageFont.load_default()

def make_slide(title, subtitle, bullets, footer="weekly-pulse-for-ind-money.vercel.app • INDMoney • 232w • No PII", bg="#0A1931"):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    f_title = load_font(38)
    f_sub = load_font(16)
    f_body = load_font(16)
    f_small = load_font(12)
    f_mono = load_font(12)
    # Top bar white with logo
    draw.rectangle([0,0,W,64], fill="white")
    # Simulate logo: dark circle with ₹
    draw.ellipse([20,12,56,48], fill="#191C1F")
    draw.text((31,22), "₹", fill="white", font=load_font(20))
    draw.text((66,14), "INDMoney", fill="#0A1931", font=load_font(16))
    draw.text((66,32), "WEEKLY PULSE  •  LIP CHALLENGE", fill="#64748b", font=load_font(10))
    draw.rounded_rectangle([W-220,18, W-20,46], radius=20, fill="#FDB913")
    draw.text((W-200,24), "LIVE ON VERCEL", fill="#0A1931", font=load_font(11))
    draw.rectangle([0,64,W,68], fill="#FDB913")
    # Title
    draw.text((40,90), title, fill="white", font=f_title)
    draw.text((40,140), subtitle, fill="#CBD5E1", font=f_sub)
    # Card
    draw.rounded_rectangle([30,180, W-30, H-30], radius=16, fill="white", outline="#E2E8F0")
    y = 200
    for b in bullets:
        if not b.strip():
            y+=8
            continue
        # Bullet styling
        is_code = b.startswith("$") or b.startswith("→") or "src/" in b or "output/" in b
        is_bold = b.startswith("✓") or b.startswith("•")
        color = "#0A1931" if is_bold else "#334155"
        if is_code:
            color = "#475569"
            font = f_mono
        else:
            font = f_body
        # Wrap
        if len(b) > 88:
            for line in textwrap.wrap(b, width=88):
                draw.text((50,y), line, fill=color, font=font)
                y+=20
        else:
            draw.text((50,y), b, fill=color, font=font)
            y+=24
        if y > H-50:
            break
    draw.text((40, H-18), footer, fill="#94a3b8", font=f_small)
    return img

slides = [
    ("Final Demo — INDMoney Weekly Pulse", "Vercel Live  •  48 reviews → One-Pager (232w)  •  Same as LIP 4", [
        "Live: https://weekly-pulse-for-ind-money.vercel.app  •  GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money",
        "Original INDMoney logo from www.indmoney.com (ind-money-logo.svg) + navy/gold theme",
        "",
        "W2: LLMs & Prompting (grouping, quotes, tone)  •  W3: Import → Group → Generate → Draft Email",
        "NEW: KYC autofetch via registered phone  •  Max 5 themes  •  ≤250 words  •  Zero PII",
        "",
        "→ 60 sec demo covering all process before use",
    ], "INDMoney 4.7★ iOS • 4.6★ Android • 2Cr+ Downloads"),
    ("1. Import — Public Reviews Only", "8–12 weeks  •  App Store + Play Store", [
        "$ cat data/reviews.csv | head -3",
        "rating,title,text,date,store",
        '5,Super smooth UPI now,"UPI payments are instant...",2026-09-18,Play Store',
        '2,KYC stuck for days,"KYC stuck at PAN check 3 days...",2026-09-17,App Store',
        "",
        "✓ PII scrubbed src/pulse.py:20  •  Columns: rating,title,text,date,store",
        "✓ 48 rows → filter by weeks (8→12w) → live impact on pulse",
        "✓ No scraping behind logins — public exports only",
    ], "data/reviews.csv • 48 rows • Public exports only"),
    ("2. Group — 5 Themes Max (INDMoney)", "Onboarding • KYC • Payments • Statements • Withdrawals", [
        "$ python3 src/pulse.py --weeks 12  →  [Info] Imported 48/48  •  232w ✓",
        "• Payments & Transfers — 13 (46% ≤2★) — UPI failures top pain",
        "• KYC / Verification — 10 (60% ≤2★) — PAN/selfie loops → autofetch fix",
        "• Withdrawals & Support — 9 (44% ≤2★) — 48h pending + fees",
        "",
        "→ Click THEME LEGEND to highlight Top 3 (smooth scroll + gold outline)",
        "→ prompts/grouping_prompt.txt  +  keyword fallback  •  No PII",
    ], "config.json:7 • 5 themes • Clickable legend"),
    ("3. Generate — One-Page Note 232w", "Scannable • Top 3 + 3 Quotes + 3 Actions", [
        "Health: Live Store 4.6★ (4L+) vs Sample Pulse 2.88★ (48, dynamic with weeks)",
        "Top 3: Payments (13) • KYC (10) • Withdrawals (9) — bars animate on weeks change",
        "",
        "What Users Said (sanitized, no PII):",
        '“App crashes every time I try to pay rent via UPI...” — Payments, 1★',
        '“KYC stuck at PAN check for 3 days...” — KYC, 2★',
        "NEW Action P1: autofetch PAN/Aadhaar via phone — Product — Track approval %",
    ], "output/weekly_note_latest.md • 232w ≤250 ✓ • PDF/PNG/MD"),
    ("4. Draft Email + Read via 4 Formats", "Demo to masked alias • CSV/Excel/Image/PDF", [
        "To: yourself@example.com (masked, no PII)  •  Subject: [Weekly Pulse] INDMoney — Week 38",
        "$ open output/demo_email_combined.eml → Mail.app (click Send)",
        "$ python3 src/send_email.py --to yourself@example.com --smtp (App Password)",
        "",
        "Read via:  /reviews.csv  •  /reviews.xlsx (openpyxl)  •  /weekly_note.png  •  /weekly_note.pdf",
        "→ Click READ VIA bar in Vercel UI → view/download instantly",
        "→ output/demo.mp4 (13s) + output/final_demo.mp4 (this demo)",
    ], "public/* • No PII • 4 formats"),
    ("5. Live on Vercel + How to Re-run", "Original INDMoney logo + navy/gold • Auto-deploy", [
        "Live: weekly-pulse-for-ind-money.vercel.app  •  200 OK  •  Next.js 14.2.5",
        "vercel.json: framework nextjs  •  .vercelignore: ignore src/app.py (Streamlit)",
        "GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money  •  Commits: 89318fc → eef5b4b → 2345bb3",
        "",
        "How to re-run weekly:  python3 src/pulse.py --weeks 12 --to yourself@example.com",
        "→ output/weekly_note_latest.md + email_draft + stats + public/*",
        "✓ Ready for LIP submission • Deliverables: prototype, note, email, CSV, README",
    ], "Vercel auto-deploy on git push • Public repo"),
]

frames = []
for title, sub, body, _ in slides:
    # Actually slides is list of tuples (title, sub, body, footer) but we defined 4 items, need unpack correctly
    pass
# Correct slides unpack
frames = []
for item in slides:
    title, sub, body = item[0], item[1], item[2]
    footer = item[3] if len(item)>3 else "weekly-pulse-for-ind-money.vercel.app"
    img = make_slide(title, sub, body, footer=footer)
    for _ in range(FPS*2):  # 2 sec per slide
        frames.append(img)
# Hold last 1 sec
for _ in range(FPS*1):
    frames.append(frames[-1])

import numpy as np
writer = imageio.get_writer(str(OUT), fps=FPS, macro_block_size=16, quality=8)
for f in frames:
    writer.append_data(np.array(f))
writer.close()
print(f"Created {OUT} {len(frames)} frames {OUT.stat().st_size/1024:.1f} KB")
