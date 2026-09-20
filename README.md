# Weekly Pulse — App Store + Play Store Reviews → One-Page Note

Turns last 8–12 weeks of **public** app reviews into a scannable ≤250-word weekly pulse with Top Themes, Real Quotes, Action Ideas — and auto-drafts an email to yourself.

> **Product:** INDMoney — same product as LIP Challenge 4 (updated per your input).  
> Config: `config.json:2` → `com.indmoney` / `id1485942658`. Workflow is product-agnostic.

**W2 — LLMs & Prompting:** Grouping, summarization, quote selection, tone control via prompt templates in `prompts/` (LLM-ready, rule-based fallback).  
**W3 — AI Workflow Automations:** `Import → Group → Generate Note → Draft Email` runs end-to-end with one command.

---

## Deliverables (in this repo)

| Artifact | Path |
|----------|------|
| **Working prototype** | `src/pulse.py` (CLI) + `src/app.py` (Streamlit UI) — run locally |
| **Latest one-page weekly note** | `output/weekly_note_latest.md` (232 words, includes KYC autofetch) — also `output/weekly_note_2026-W38.md` |
| **Email draft** | `output/email_draft_latest.txt` + `.eml` (open in Mail/Outlook) |
| **Reviews CSV used** | `data/reviews.csv` (48 reviews, 2026-08-05 → 2026-09-18, no PII, redacted) |
| **Grouped + stats** | `output/stats_latest.json`, `output/reviews_grouped.csv` via UI |

---

## Theme Legend (Max 5 — fixed)

| # | Theme | What it covers | Keywords |
|---|-------|----------------|----------|
| 1 | **Onboarding** | Sign-up, OTP, permissions, welcome flow, language | onboarding, otp, signup, create account, permissions, language |
| 2 | **KYC / Verification** | PAN, Aadhaar, selfie, doc upload, video KYC, verification status | kyc, pan, aadhaar, selfie, document, video kyc, address proof |
| 3 | **Payments & Transfers** | UPI, merchant pay, autopay, refunds, failed/pending | upi, payment, transfer, merchant, debited, refund, pending |
| 4 | **Statements & Portfolio** | Statements, portfolio, XIRR, PDF, transaction history | statement, portfolio, xirr, pdf, transaction, download |
| 5 | **Withdrawals & Support** | Withdrawal time, fees, support responsiveness, limits | withdrawal, credited, charges, fee, support, limit |

> Only these 5 themes used. Every review mapped to **one** best-fit theme (LLM prompt in `prompts/grouping_prompt.txt`, rule-based fallback).

---

## How to Re-Run for a New Week

### 1) Get public reviews (no scraping behind logins)

Use **public review exports only**:

- **App Store:** App Store Connect → App Analytics → Ratings & Reviews → Export CSV
- **Play Store:** Google Play Console → Ratings & reviews → Export (CSV)
- Or community tools: `app-store-scraper`, `google-play-scraper` on **public** pages only

Export columns needed: `rating, title, text, date, store` — date as `YYYY-MM-DD`.  
Place file at `data/reviews.csv` (overwrite sample). No usernames/emails/IDs — script auto-redacts PII.

```bash
head data/reviews.csv
# rating,title,text,date,store
# 5,Great UPI,"UPI instant now",2026-09-18,Play Store
```

### 2) Run the workflow (CLI)

```bash
# from repo root: /Users/niteshpradhan/Desktop/weekly-pulse
python3 src/pulse.py --weeks 12 --to yourself@example.com
# outputs in output/:
#  weekly_note_YYYY-Www.md (≤250 words)
#  email_draft_YYYY-Www.txt + .eml
#  stats_YYYY-Www.json
```

Options:
- `--weeks 8` or `12` (required 8–12 window)
- `--input data/reviews.csv` (custom CSV)
- `--to your.alias@company.com` (draft recipient)

No API key needed — runs rule-based. To enable LLM polish (optional):
```bash
export OPENAI_API_KEY=sk-...
python3 src/pulse.py --weeks 12
# prompts used: prompts/grouping_prompt.txt, prompts/summarize_prompt.txt, prompts/action_ideas_prompt.txt
```

### 3) Check the note (≤250 words enforced)

```bash
wc -w output/weekly_note_latest.md
cat output/weekly_note_latest.md
```

Example latest (229 words):

```
# Weekly Pulse — INDMoney | Week 38 (2026-08-05 → 2026-09-18)
**Health:** 2.88★ avg • 48 reviews (12w) • 5★:9 4★:8 3★:9 2★:12 1★:10
**Top 3 Themes (of 5):** Payments & Transfers (13), KYC/Verification (10), Withdrawals & Support (9)
**What Users Said:** 3 anonymized quotes (no PII)
**3 Action Ideas:** Eng/Product/Ops owners + metric to watch
```

### 4) Email draft

- **Preview:** `cat output/email_draft_latest.txt`
- **Open in Mail app:** `open output/email_draft_latest.eml` (macOS) or double-click the `.eml`
- **Actually send via SMTP (optional):**
  ```bash
  export SMTP_USER=you@gmail.com
  export SMTP_PASS=your_gmail_app_password  # Gmail → App Passwords
  python3 src/send_email.py --to yourself@example.com --smtp
  # or without --smtp to just open draft (dry-run, recommended)
  python3 src/send_email.py --to yourself@example.com
  ```

### 5) Streamlit prototype (interactive demo — 2-min)

```bash
pip install -r requirements.txt
streamlit run src/app.py
# → http://localhost:8501
# Upload new CSV, slide weeks 8–12, see top themes + quotes + actions live, download note/email/CSV
```

### 6) Weekly automation (cron)

```bash
# Every Monday 9am
0 9 * * 1 cd /Users/niteshpradhan/Desktop/weekly-pulse && /usr/bin/python3 src/pulse.py --weeks 12 --to yourself@example.com
```

Or GitHub Actions: add `.github/workflows/pulse.yml` running `python src/pulse.py` and committing `output/`.

---

## Workflow Detail

```
data/reviews.csv (public exports, last 8-12 weeks)
        ↓
  [Import]  sanitize PII (regex: emails, phones, PAN, Aadhaar), parse dates, filter by window
        ↓
  [Group]  prompts/grouping_prompt.txt → LLM (if key) else keyword scoring → 5 themes max
        ↓ stats: count, avg rating, neg% per theme
        ↓
  [Top 3]  weighted by count × (1 + neg%/2) → most urgent themes
        ↓
  [Quotes]  scored by vividness + specificity (12-25 words), one per top theme, anonymized, no PII
        ↓
  [Actions] prompts/action_ideas_prompt.txt → LLM else template per theme → 3 shippable ideas with owner + metric
        ↓
  [Generate Note]  prompts/summarize_prompt.txt → ≤250 words, scannable markdown (health + top3 + quotes + actions)
        ↓
  [Draft Email]  To: yourself@alias, subject with week + stats, body = note + attachments + next step
```

**Scannable:** bold headers, bullets, 1-line theme summaries, word count logged.  
**Tone control:** neutral, concise, product-manager friendly (enforced in prompts).  
**No PII:** regex redaction + no usernames/emails/IDs stored in any artifact.

---

## Weekly Note (Latest) — Copy-Paste Ready

> See `output/weekly_note_latest.md` — also rendered below. 232 words, verified. Includes NEW KYC autofetch idea.

```md
# Weekly Pulse — INDMoney | Week 38 (2026-08-05 → 2026-09-18)

**Health:** 2.88★ avg • 48 reviews (12w) • 5★:9 4★:8 3★:9 2★:12 1★:10

**Top 3 Themes (of 5):**
1. **Payments & Transfers** — 13 reviews (46% ≤2★, 3.0★ avg) • UPI failures & double-debits still top pain; successes up after recent fix
2. **KYC / Verification** — 10 reviews (60% ≤2★, 2.5★ avg) • Verification stuck/rejected loops; selfie + PAN upload are blockers
3. **Withdrawals & Support** — 9 reviews (44% ≤2★, 2.89★ avg) • 48h+ pending + hidden fees erode trust; fast weekday cases praised

**What Users Said:**
> “App crashes every time I try to pay rent via UPI. Can't complete payment.” — Payments & Transfers, 1★

> “KYC verification stuck at PAN check for 3 days. Tried reinstalling.” — KYC / Verification, 2★

> “Withdrawal requested 48 hours ago still not credited. Support not replying.” — Withdrawals & Support, 1★

**3 Action Ideas — Next 7 Days:**
1. Fix UPI pending/double-debit: add idempotency + live status — Eng — Track refund SLA (target <24h)
2. Cut KYC drop-off: autofetch PAN/Aadhaar via registered phone number + inline validation + selfie light guide — Product — Track approval % **[NEW: your autofetch idea]**
3. Make withdrawals transparent: show fee + ETA + confirm account before debit — Ops — Track pending tickets

*Source: 48 public reviews (App Store + Play Store) • No PII*
```

---

## Email Draft (Preview)

```
To: yourself@example.com
Subject: [Weekly Pulse] INDMoney — Week 38 | 48 reviews, top 3 themes + 3 actions

Hi team,

Weekly pulse for INDMoney (last 12 weeks, 48 public reviews). Scannable one-pager below — ≤250 words, no PII.

---
[weekly note goes here]
---

Attachment: weekly_note_2026-09-20.md (one-pager PDF-ready)
CSV: data/reviews.csv (public exports only, PII removed)

Next step: Pick 1 action for this sprint. Reply with owner.

— Auto-generated by weekly-pulse workflow (Import → Group → Generate → Draft)
How to re-run: python src/pulse.py --weeks 12  (see README)
```

Screenshot: open `output/email_draft_latest.eml` → Mail app renders with To/Subject/Body exactly as above.

---

## Project Structure

```
weekly-pulse/
├── config.json                 # product + 5 themes + email alias
├── data/
│   └── reviews.csv             # sample 48 reviews (public, PII-redacted)
├── prompts/
│   ├── grouping_prompt.txt     # W2: theme grouping LLM prompt
│   ├── summarize_prompt.txt    # W2: ≤250-word note prompt
│   └── action_ideas_prompt.txt # W2: action ideas prompt
├── src/
│   ├── pulse.py                # W3: Import → Group → Generate → Draft (CLI)
│   ├── app.py                  # Streamlit interactive prototype
│   └── send_email.py           # Draft opener / SMTP sender
├── output/
│   ├── weekly_note_latest.md   # latest one-pager
│   ├── email_draft_latest.txt  # email draft
│   ├── email_draft_latest.eml  # one-click mail open
│   └── stats_latest.json       # counts + quotes + ideas
├── requirements.txt
└── README.md
```

---

## Constraints Checklist

- ✅ Public review exports only — no scraping behind logins (documented above)
- ✅ Max 5 themes (exactly 5, fixed legend)
- ✅ Notes scannable, ≤250 words (229 verified via `wc -w`)
- ✅ No usernames/emails/IDs in any artifacts (PII sanitization + no user column)
- ✅ Import rating/title/text/date, group, top3, 3 quotes, 3 actions, draft email to self

---

## Demo Video Script (≤3 min)

1. **0:00-0:20** Show `data/reviews.csv` (48 public reviews)
2. **0:20-0:50** Run `python src/pulse.py --weeks 12` → logs Import/Group/Word count
3. **0:50-1:20** Open `output/weekly_note_latest.md` → highlight Top 3 Themes, Quotes, Actions
4. **1:20-1:50** `open output/email_draft_latest.eml` → shows draft email to yourself
5. **1:50-2:30** `streamlit run src/app.py` → upload CSV, slide weeks, live note
6. **2:30-3:00** Show README → how to re-run for new week

---

## Notes

- **If Challenge 4 product differs:** Change `"product"` and store app IDs in `config.json`, replace `data/reviews.csv`, keep same 5 themes (onboarding, KYC, payments, statements, withdrawals) — generic enough for any fintech.
- **LLM optional:** Works fully offline rule-based; set `OPENAI_API_KEY` to enable prompting polish.
- **PDF:** `output/weekly_note_latest.md` → print to PDF from VS Code/Notion (File → Print → PDF) or `pandoc -o weekly.pdf`.

Questions/feedback: open issue at https://github.com/anomalyco/opencode
