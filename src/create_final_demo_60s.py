#!/usr/bin/env python3
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont
import pathlib, textwrap
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "final_demo_60s.mp4"
W, H = 1280, 720
FPS = 30

def load_font(size):
    try: return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except: return ImageFont.load_default()

def make_slide(title, subtitle, bullets, footer="weekly-pulse-for-ind-money.vercel.app • INDMoney • 232w • No PII • Voiceover script", bg="#0A1931"):
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    f_title = load_font(32)
    f_sub = load_font(14)
    f_body = load_font(15)
    f_small = load_font(11)
    f_mono = load_font(11)
    draw.rectangle([0,0,W,64], fill="white")
    draw.ellipse([20,12,56,48], fill="#191C1F")
    draw.text((31,22), "₹", fill="white", font=load_font(18))
    draw.text((66,14), "INDMoney", fill="#0A1931", font=load_font(15))
    draw.text((66,32), "WEEKLY PULSE  •  60S FINAL DEMO", fill="#64748b", font=load_font(9))
    draw.rounded_rectangle([W-200,18, W-20,46], radius=20, fill="#FDB913")
    draw.text((W-185,24), "VOICEOVER", fill="#0A1931", font=load_font(10))
    draw.rectangle([0,64,W,68], fill="#FDB913")
    draw.text((40,90), title, fill="white", font=f_title)
    draw.text((40,132), subtitle, fill="#CBD5E1", font=f_sub)
    draw.rounded_rectangle([30,170, W-30, H-30], radius=16, fill="white", outline="#E2E8F0")
    y=190
    for b in bullets:
        if not b.strip():
            y+=6
            continue
        is_code = b.startswith("$") or "src/" in b or "output/" in b
        font = f_mono if is_code else f_body
        color = "#334155"
        if b.startswith("✓"): color="#16a34a"
        if b.startswith("→"): color="#475569"
        if b.startswith("🎙"): color="#0A1931"; font=load_font(13)
        lines = textwrap.wrap(b, width=90) if len(b)>90 else [b]
        for line in lines:
            draw.text((50,y), line, fill=color, font=font)
            y+=20
        if y > H-50: break
    draw.text((40, H-18), footer, fill="#94a3b8", font=f_small)
    # progress bar
    return img

slides = [
    ("Final Demo — INDMoney Weekly Pulse (60s)", "Vercel Live  •  Same as LIP 4  •  Original logo from indmoney.com", [
        "🎙 Voiceover: 'This is the INDMoney Weekly Pulse — turning 48 App Store and Play Store reviews into a one-page action note in 30 seconds.'",
        "Live: weekly-pulse-for-ind-money.vercel.app  •  GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money",
        "W2: LLMs & Prompting (grouping, quotes, tone)  •  W3: Import → Group → Generate → Draft Email",
        "NEW: KYC autofetch via registered phone  •  Max 5 themes  •  ≤250 words  •  Zero PII  •  4.6★ Live Store",
        "→ This 60s demo covers all process before submission",
    ]),
    ("1. Import — Public Reviews Only (0:10)", "8–12 weeks  •  CSV: rating, title, text, date, store", [
        "🎙 'We import only public exports — no scraping behind logins.'",
        "$ cat data/reviews.csv  →  48 rows, 2026-08-05 → 2026-09-18",
        "✓ PII scrubbed src/pulse.py:20  •  Emails, phones, PAN redacted",
        "✓ Drag & drop or Load reviews.csv (1-Click Test) → 48 rows • PII Scrubbed",
        "✓ Slider 8w→12w updates live — reviews count & health animate",
        "→ INDMoney has 4.6★ over 4L+ reviews — sample pulse shows 2.88★ (48) scaled live",
    ]),
    ("2. Group — 5 Themes Max (0:20)", "INDMoney Taxonomy  •  Clickable Legend", [
        "🎙 'Reviews auto-group into 5 INDMoney themes — same filing as config.json.'",
        "• Onboarding (7)  •  KYC / Verification (10, 60% neg) — NEW autofetch  •  Payments (13)",
        "• Statements & Portfolio (9)  •  Withdrawals & Support (9)",
        "→ Click any legend pill → highlights Top 3 card with gold outline + smooth scroll",
        "→ prompts/grouping_prompt.txt + keyword fallback  •  No usernames/IDs",
        "→ Top 3 ranked by volume share, negativity weighted",
    ]),
    ("3. Generate — One-Page Note 232w (0:30)", "Scannable  •  Top 3 + 3 Quotes + 3 Actions", [
        "🎙 'The note is scannable in 30 seconds — 232 words, well under 250.'",
        "Health: Live Store 4.6★ (4L+) vs Sample Pulse 2.88★ (dynamic) — bars animate on weeks change",
        "Top 3: Payments 13 (46% ≤2★)  •  KYC 10 (60%)  •  Withdrawals 9 (44%)",
        "Quotes (sanitized): 'App crashes on UPI...' (1★), 'KYC stuck 3 days...' (2★)",
        "Actions: P0 UPI idempotency (Eng) • P1 KYC autofetch via phone (Product) • P2 Withdrawal transparency (Ops)",
        "→ Download as MD / PDF / Image  •  232w ≤250 ✓",
    ]),
    ("4. Read via 4 Formats + Draft Email (0:40)", "CSV • Excel • Image • PDF  •  Demo Email", [
        "🎙 'Read the pulse however you need — CSV, Excel, Image, or PDF — plus draft email.'",
        "READ VIA bar:  📊 CSV (/reviews.csv)  •  📗 Excel (7.8KB, openpyxl)  •  🖼️ Image (PNG)  •  📄 PDF",
        "To: yourself@example.com (masked)  •  Subject: [Weekly Pulse] INDMoney — Week 38",
        "$ open output/demo_email_combined.eml → Mail.app (click Send)",
        "$ python3 src/send_email.py --to yourself@example.com --smtp (App Password)",
        "→ No PII in any artifact — emails masked, IDs redacted",
    ]),
    ("5. Live on Vercel + How to Re-run (0:50)", "Original INDMoney logo  •  Auto-deploy on git push", [
        "🎙 'Live on Vercel at weekly-pulse-for-ind-money.vercel.app — deployed from GitHub.'",
        "Live: 200 OK  •  Next.js 14.2.5  •  vercel.json: framework nextjs  •  Ignores Python src/app.py",
        "GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money — commits: 08b78be → latest",
        "How to re-run weekly:  python3 src/pulse.py --weeks 12 --to yourself@example.com",
        "→ Generates weekly_note_latest.md + email_draft + stats + public/* in one command",
        "✓ Ready for LIP submission • Deliverables: prototype, note, email, CSV, README",
    ]),
]

frames=[]
for title, sub, body in [(s[0],s[1],s[2]) for s in slides]:
    footer = "weekly-pulse-for-ind-money.vercel.app • INDMoney • Original theme • Voiceover script included"
    img = make_slide(title, sub, body, footer=footer)
    for _ in range(FPS*10): # 10 sec per slide = 60s total
        frames.append(img)
# Hold last 0
import numpy as np
writer = imageio.get_writer(str(OUT), fps=FPS, macro_block_size=16, quality=8)
for f in frames:
    writer.append_data(np.array(f))
writer.close()
print(f"Created {OUT} {len(frames)} frames {OUT.stat().st_size/1024:.1f} KB, duration {len(frames)/FPS:.1f}s")

# Also create voiceover script txt
script = ROOT / "output" / "voiceover_script.txt"
with open(script, "w") as f:
    f.write("FINAL DEMO VOICEOVER SCRIPT — INDMoney Weekly Pulse (60s, ≤3min)\n")
    f.write("="*60+"\n\n")
    for i, (title, sub, body) in enumerate([(s[0],s[1],s[2]) for s in slides],1):
        f.write(f"Slide {i}: {title} ({sub})\n")
        for b in body:
            if b.startswith("🎙"):
                f.write(f"  {b}\n")
        f.write("\n")
print(f"Voiceover script: {script}")
