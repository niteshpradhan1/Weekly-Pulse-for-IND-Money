#!/usr/bin/env python3
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont
import pathlib

out = pathlib.Path(__file__).resolve().parents[1] / "output" / "demo.mp4"
W, H = 1280, 720
FPS = 30

def make_frame(title, subtitle, body_lines, bg="#0f172a", accent="#22c55e"):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    # Try to load font, fallback
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        body_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        mono_font = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", 14)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        mono_font = ImageFont.load_default()
    # Header bar
    draw.rectangle([0, 0, W, 70], fill="white")
    draw.text((30, 18), "INDMoney  •  Weekly Pulse  •  Vercel Live", fill="#0f172a", font=sub_font)
    draw.text((W-260, 22), "weekly-pulse-for-ind-money.vercel.app", fill="#64748b", font=mono_font)
    # Accent line
    draw.rectangle([0, 70, W, 74], fill=accent)
    # Title
    draw.text((40, 100), title, fill="white", font=title_font)
    draw.text((40, 165), subtitle, fill="#cbd5e1", font=sub_font)
    # Body box
    box_y = 210
    draw.rounded_rectangle([30, box_y, W-30, H-30], radius=16, fill="white", outline="#e2e8f0")
    y = box_y + 24
    for line in body_lines:
        # Use mono for code, else body
        is_code = line.startswith("$") or line.startswith("→") or "src/" in line or "output/" in line or "Top" in line or "Health" in line
        font = mono_font if is_code else body_font
        color = "#0f172a" if not is_code else "#334155"
        if line.startswith("✓") or line.startswith("→"):
            color = "#16a34a" if line.startswith("✓") else "#475569"
        # Wrap long lines
        draw.text((50, y), line, fill=color, font=font)
        y += 28
        if y > H-50:
            break
    return img

slides = [
    ("Weekly Pulse — INDMoney", "Live Demo  •  48 reviews → One-Pager (232 words) • No PII", [
        "Same product as LIP Challenge 4  •  Vercel: weekly-pulse-for-ind-money.vercel.app",
        "GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money  •  5 themes max",
        "",
        "Workflow: Import → Group → Generate Note → Draft Email (W2 + W3)",
        "NEW: KYC autofetch via registered phone  •  src/pulse.py:251",
        "",
        "→ Press play: 12 sec demo covering all process",
    ]),
    ("1. Import — Public Reviews Only", "8–12 weeks  •  rating, title, text, date, store", [
        "$ cat data/reviews.csv | head -3",
        "rating,title,text,date,store",
        "5,Super smooth UPI now,\"UPI payments are instant...\",2026-09-18,Play Store",
        "2,KYC stuck for days,\"KYC stuck at PAN check 3 days...\",2026-09-17,App Store",
        "",
        "✓ PII sanitized  •  src/pulse.py:20  •  48 reviews  •  2026-08-05 → 2026-09-18",
        "✓ No scraping behind logins — public exports only",
    ]),
    ("2. Group — 5 Themes Max", "Onboarding • KYC • Payments • Statements • Withdrawals", [
        "$ python3 src/pulse.py --weeks 12",
        "[Info] Imported 48/48 reviews from last 12 weeks",
        "✓ Payments & Transfers — 13 (46% ≤2★) — UPI failures top pain",
        "✓ KYC / Verification — 10 (60% ≤2★) — PAN/selfie loops",
        "✓ Withdrawals & Support — 9 (44% ≤2★) — pending + fees",
        "",
        "→ Weighted by count × (1+neg%/2)  •  prompts/grouping_prompt.txt",
    ]),
    ("3. Generate — One-Page Note ≤250w", "232 words • Scannable • Quotes + Actions", [
        "Health: 2.88★ avg • 48 reviews • 5★:9 4★:8 3★:9 2★:12 1★:10",
        "Top 3: Payments (13) • KYC (10) • Withdrawals (9)",
        "",
        "What Users Said (no PII):",
        "> “App crashes every time I try to pay rent via UPI...\" — Payments, 1★",
        "> “KYC stuck at PAN check for 3 days...\" — KYC, 2★",
        "NEW Action 2: autofetch PAN/Aadhaar via registered phone — Product",
    ]),
    ("4. Draft Email → Vercel Live", "Demo to 2 IDs • 2 clicks to send", [
        "To: niteshpradhan900@gmail.com, kaushikyashasvi@gmail.com",
        "Subject: [Weekly Pulse] INDMoney — Week 38 | 48 reviews",
        "$ open output/demo_email_combined.eml  → Mail.app (click Send)",
        "$ python3 src/send_email.py --to ... --smtp  (with App Password)",
        "",
        "Vercel Live: weekly-pulse-for-ind-money.vercel.app",
        "✓ Next.js 14.2.5  •  vercel.json: framework nextjs  •  200 OK",
        "✓ GitHub pushed: 61000bd → auto-deploy",
    ]),
    ("5. Re-run for New Week + Deliverables", "How to re-run weekly • All artifacts", [
        "$ python3 src/pulse.py --weeks 12 --to yourself@example.com",
        "→ output/weekly_note_latest.md  •  output/email_draft_*.eml",
        "→ output/stats_latest.json  •  data/reviews.csv",
        "",
        "Deliverables: prototype (CLI + Streamlit + Vercel), note PDF/MD,",
        "email draft, CSV, README with theme legend + re-run guide",
        "✓ Live on Vercel  •  Ready for LIP submission",
    ]),
]

frames = []
for title, sub, body in slides:
    img = make_frame(title, sub, body)
    # Hold each slide for 2 sec = 60 frames
    for _ in range(FPS*2):
        frames.append(img)

# Also add final title card hold 1 sec
for _ in range(FPS*1):
    frames.append(frames[-1])

# Convert PIL to numpy for imageio
import numpy as np
writer = imageio.get_writer(str(out), fps=FPS, macro_block_size=16, quality=8)
for f in frames:
    writer.append_data(np.array(f))
writer.close()
print(f"Created {out} with {len(frames)} frames, size {out.stat().st_size/1024:.1f} KB")
