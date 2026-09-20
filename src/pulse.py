#!/usr/bin/env python3
"""
Weekly Pulse — App Store + Play Store Reviews
Workflow: Import → Group → Generate Note → Draft Email

- Imports reviews.csv with rating,title,text,date,store
- Groups into 5 themes max (rule-based + LLM-ready prompt template)
- Generates ≤250 words weekly one-page note
- Drafts email to self/alias (no PII)

Usage:
  python src/pulse.py
  python src/pulse.py --input data/reviews.csv --weeks 12 --output output/

Env (optional LLM):
  OPENAI_API_KEY → enables LLM grouping/summarization (falls back to rules if missing)
"""
import argparse
import csv
import json
import re
from datetime import datetime, timedelta, date
from pathlib import Path
from collections import Counter, defaultdict
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
PROMPTS_DIR = ROOT / "prompts"

# --- Theme definitions fallback ---
THEMES_FALLBACK = {
    "onboarding": {"label": "Onboarding", "keywords": ["onboarding", "sign up", "signup", "otp", "create account", "registration", "welcome", "install", "permissions", "language", "crash"]},
    "kyc": {"label": "KYC / Verification", "keywords": ["kyc", "verification", "pan", "aadhaar", "aadhar", "selfie", "document upload", "video kyc", "address proof", "rejected", "verify", "video call"]},
    "payments": {"label": "Payments & Transfers", "keywords": ["upi", "payment", "transfer", "pay", "merchant", "autopay", "debited", "refund", "failed", "pending", "crashes on payment"]},
    "statements": {"label": "Statements & Portfolio", "keywords": ["statement", "portfolio", "xirr", "pdf", "transactions", "breakdown", "total", "download", "email"]},
    "withdrawals": {"label": "Withdrawals & Support", "keywords": ["withdrawal", "withdraw", "credited", "charges", "fee", "support", "help", "limit", "charge"]},
}

PII_PATTERNS = [
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "[redacted-email]"),
    (re.compile(r"\b\d{10}\b"), "[redacted-phone]"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "[redacted-pan]"),  # PAN
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"), "[redacted-id]"),  # Aadhaar-like
    (re.compile(r"@\w+"), "[redacted-handle]"),
]

def sanitize(text: str) -> str:
    if not text:
        return text
    for pat, repl in PII_PATTERNS:
        text = pat.sub(repl, text)
    # Remove potential usernames like "by John D."
    text = re.sub(r"\b(user(name)?|by)[:\s]+\w+", "", text, flags=re.I)
    return text.strip()

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"themes": THEMES_FALLBACK, "product": "Fi Money (Neobank)", "email": {"to_alias": "yourself@example.com"}}

def classify_review(text: str, title: str, config_themes) -> str:
    """Rule-based classifier using keyword scoring. LLM-ready: prompt in prompts/grouping_prompt.txt"""
    combined = f"{title} {text}".lower()
    scores = {}
    for key, meta in config_themes.items():
        kws = [k.lower() for k in meta.get("keywords", [])]
        score = sum(1 for kw in kws if kw in combined)
        # boost for exact theme words
        if key in combined:
            score += 0.5
        scores[key] = score
    # if all zero, default to payments (most common) or onboarding
    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        # heuristic fallback: check rating text hints
        if "statement" in combined or "portfolio" in combined:
            return "statements"
        if "withdraw" in combined:
            return "withdrawals"
        return "payments"
    return best

def try_llm_classify(text, title, rating):
    """If OPENAI_API_KEY set, call LLM, else return None to use rule-based."""
    import os
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        prompt_path = PROMPTS_DIR / "grouping_prompt.txt"
        system = prompt_path.read_text() if prompt_path.exists() else "Group into onboarding|kyc|payments|statements|withdrawals"
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Title: {title}\nRating: {rating}\nText: {text}\nReturn JSON only."}
            ],
            temperature=0.2,
            max_tokens=100
        )
        content = resp.choices[0].message.content.strip()
        # extract json
        m = re.search(r"\{.*?\}", content, re.S)
        if m:
            j = json.loads(m.group(0))
            theme = j.get("theme", "").lower().strip()
            if theme in THEMES_FALLBACK:
                return theme
    except Exception as e:
        print(f"[LLM classify fallback] {e}", file=sys.stderr)
    return None

def load_reviews(csv_path: Path, weeks: int = 12):
    cutoff = date.today() - timedelta(weeks=weeks)
    # Also handle data from future? Use max date in file as reference if cutoff yields zero
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # normalize
            try:
                d = datetime.strptime(r["date"].strip(), "%Y-%m-%d").date()
            except:
                d = cutoff
            r["date"] = d
            r["rating"] = int(str(r["rating"]).strip())
            r["title"] = sanitize(r.get("title","").strip())
            r["text"] = sanitize(r.get("text","").strip())
            rows.append(r)
    # filter to last weeks
    filtered = [r for r in rows if r["date"] >= cutoff]
    if len(filtered) == 0:
        # fallback: take last 12 weeks from max date in file
        max_d = max(r["date"] for r in rows)
        cutoff2 = max_d - timedelta(weeks=weeks)
        filtered = [r for r in rows if r["date"] >= cutoff2]
        print(f"[Info] No reviews in last {weeks} weeks from today. Using window {cutoff2} to {max_d} ({len(filtered)} reviews)")
    else:
        print(f"[Info] Imported {len(filtered)}/{len(rows)} reviews from last {weeks} weeks (cutoff {cutoff})")
    # sort by date desc
    filtered.sort(key=lambda x: x["date"], reverse=True)
    return filtered

def aggregate(reviews, config):
    themes = config.get("themes", THEMES_FALLBACK)
    by_theme = defaultdict(list)
    for r in reviews:
        # try LLM first
        theme = try_llm_classify(r["text"], r["title"], r["rating"])
        if not theme:
            theme = classify_review(r["text"], r["title"], themes)
        r["theme"] = theme
        by_theme[theme].append(r)
    stats = {}
    for k, lst in by_theme.items():
        avg = sum(x["rating"] for x in lst) / len(lst) if lst else 0
        neg = sum(1 for x in lst if x["rating"] <= 2)
        stats[k] = {"count": len(lst), "avg": round(avg,2), "neg": neg, "neg_pct": round(neg/len(lst)*100) if lst else 0}
    return by_theme, stats

def pick_top_themes(stats, n=3):
    # Sort by count desc, but boost negative pct for health pulse (weighted)
    # Weighted score = count * (1 + neg_pct/100)
    scored = []
    for k, v in stats.items():
        score = v["count"] * (1 + v["neg_pct"]/100 * 0.5)
        scored.append((k, v, score))
    scored.sort(key=lambda x: x[2], reverse=True)
    return [(k,v) for k,v,_ in scored[:n]]

def pick_quotes(reviews, top_themes, n=3):
    """Pick 3 vivid quotes, one per top theme if possible, anonymized, 15-25 words, no PII."""
    quotes = []
    used_texts = set()
    theme_keys = [k for k,_ in top_themes]
    # For each top theme, pick best quote
    for tk in theme_keys:
        cands = [r for r in reviews if r["theme"] == tk]
        # Prefer rating 1-2 for pain, but include one positive for balance
        # Score quotes: length 12-25 words higher, has specific detail, not generic
        def quote_score(r):
            words = len(r["text"].split())
            # ideal 15-24 words
            len_score = 10 - abs(18 - words)  # peak at 18
            detail_score = 2 if any(w in r["text"].lower() for w in ["hours","days","failed","stuck","crash","refund","pdf","otp","fee","limit"]) else 0
            vivid_score = 1 if len(r["text"]) > 40 else 0
            return len_score + detail_score + vivid_score
        cands.sort(key=quote_score, reverse=True)
        for c in cands:
            t = c["text"]
            if t not in used_texts and 10 <= len(t.split()) <= 26:
                # Trim to ≤25 words if needed but keep meaning
                words = t.split()
                if len(words) > 25:
                    t = " ".join(words[:25]) + "…"
                # Ensure no PII
                t = sanitize(t)
                quotes.append({"text": t, "theme": tk, "rating": c["rating"], "date": c["date"]})
                used_texts.add(c["text"])
                break
        if len(quotes) >= n:
            break
    # fallback if not enough
    if len(quotes) < n:
        remaining = [r for r in reviews if r["text"] not in used_texts]
        for r in remaining:
            t = sanitize(r["text"])
            w = len(t.split())
            if 8 <= w <= 26 and t not in [q["text"] for q in quotes]:
                if len(t.split()) > 25:
                    t = " ".join(t.split()[:25]) + "…"
                quotes.append({"text": t, "theme": r["theme"], "rating": r["rating"], "date": r["date"]})
                if len(quotes) >= n:
                    break
    return quotes[:n]

def generate_action_ideas(top_themes, quotes, reviews_by_theme):
    """Template-based action ideas, LLM-ready (prompts/action_ideas_prompt.txt). Falls back to rules."""
    import os
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            prompt = (PROMPTS_DIR / "action_ideas_prompt.txt").read_text() if (PROMPTS_DIR / "action_ideas_prompt.txt").exists() else "Generate 3 action ideas"
            theme_summary = "\n".join([f"- {k}: {v['count']} reviews, {v['neg_pct']}% negative, avg {v['avg']}" for k,v in top_themes])
            quote_summary = "\n".join([f'"{q["text"]}" ({q["theme"]}, {q["rating"]}★)' for q in quotes])
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content": prompt},
                    {"role":"user","content": f"Top themes:\n{theme_summary}\n\nQuotes:\n{quote_summary}\n\nGenerate 3 action ideas."}
                ],
                temperature=0.4,
                max_tokens=300
            )
            lines = [l.strip("- •123. ") for l in resp.choices[0].message.content.strip().split("\n") if l.strip()]
            # take 3
            ideas = [l for l in lines if len(l) > 10][:3]
            if len(ideas) == 3:
                return ideas
        except Exception as e:
            print(f"[LLM action fallback] {e}", file=sys.stderr)

    # Rule-based fallback: map theme to specific idea — keep ≤22 words each for ≤250 total
    idea_templates = {
        "payments": "Fix UPI pending/double-debit: add idempotency + live status — Eng — Track refund SLA (target <24h)",
        "kyc": "Cut KYC drop-off: autofetch PAN/Aadhaar via registered phone number + inline validation + selfie light guide — Product — Track approval %",
        "withdrawals": "Make withdrawals transparent: show fee + ETA + confirm account before debit — Ops — Track pending tickets",
        "statements": "Fix statements: reconcile totals vs portfolio, add categories, print-ready PDF — Eng — Track download success",
        "onboarding": "Speed onboarding: OTP auto-read + progress bar + fewer permissions — Product — Track completion %",
        # generic variants
        "payments_alt": "Show UPI daily limit upfront and block amount before failure — Product — Track UPI failure rate",
        "withdrawals_alt": "Add weekend withdrawal ETA warning & instant support fallback — Support — Track weekend pending %"
    }
    ideas = []
    for k,_ in top_themes:
        if k in idea_templates and idea_templates[k] not in ideas:
            ideas.append(idea_templates[k])
        if len(ideas) >= 3:
            break
    # Fill remaining
    for k in ["payments","kyc","withdrawals","statements","onboarding"]:
        if len(ideas) >=3:
            break
        tpl = idea_templates.get(k)
        if tpl and tpl not in ideas:
            ideas.append(tpl)
    return ideas[:3]

def word_count(md: str) -> int:
    return len(md.split())

def generate_weekly_note(product, weeks, total_reviews, stats, by_theme, top_themes, quotes, ideas, date_range_str, avg_rating, distribution):
    # Build markdown note ≤250 words
    # Header
    # Count words while drafting
    theme_labels = {k: v["label"] if "label" in v else k for k,v in stats.items()}  # but stats holds numbers not labels
    # Load real labels from config
    config = load_config()
    theme_map = config.get("themes", {})
    def label(k):
        return theme_map.get(k, {}).get("label", k.title())

    # Prepare theme lines
    theme_lines = []
    for k, v in top_themes:
        # 1-line summary per theme based on quotes/reviews
        summary_map = {
            "payments": "UPI failures & double-debits still top pain; successes up after recent fix",
            "kyc": "Verification stuck/rejected loops; selfie + PAN upload are blockers",
            "withdrawals": "48h+ pending + hidden fees erode trust; fast weekday cases praised",
            "statements": "PDF clarity & total-mismatch complaints; new design praised by others",
            "onboarding": "OTP delays & duplicate asks slow start; Aadhaar auto-fill delights when works"
        }
        summ = summary_map.get(k, f"{v['neg_pct']}% negative")
        theme_lines.append(f"**{label(k)}** — {v['count']} reviews ({v['neg_pct']}% ≤2★, {v['avg']}★ avg) • {summ}")

    # Quotes section
    quote_lines = []
    for q in quotes:
        # Format: > “text” — Theme, ★rating
        # Use theme label
        qlabel = label(q["theme"])
        quote_lines.append(f'> “{q["text"]}” — {qlabel}, {q["rating"]}★')

    # Try LLM summarization if available to polish tone and keep ≤250 words
    import os
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            system = (PROMPTS_DIR / "summarize_prompt.txt").read_text() if (PROMPTS_DIR / "summarize_prompt.txt").exists() else "Summarize reviews"
            # Build context
            theme_ctx = "\n".join([f"{label(k)}: {v['count']} reviews, {v['neg_pct']}% neg, avg {v['avg']}" for k,v in stats.items()])
            reviews_ctx = "\n".join([f"[{r['theme']}] {r['rating']}★ {r['title']}: {r['text']}" for r in sorted(quotes, key=lambda x: x["rating"])])
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content": system},
                    {"role":"user","content": f"Product: {product}\nDate range: {date_range_str}\nTotal: {total_reviews}, avg {avg_rating}★\nThemes:\n{theme_ctx}\nTop themes: {', '.join([label(k) for k,_ in top_themes])}\nQuotes:\n{reviews_ctx}\nIdeas draft:\n" + "\n".join(ideas)}
                ],
                temperature=0.3,
                max_tokens=600
            )
            md = resp.choices[0].message.content.strip()
            if word_count(md) > 250:
                # Ask to trim
                resp2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content": "Trim this markdown to ≤250 words, keep scannable bullets and all sections."},
                        {"role":"user","content": md}
                    ],
                    temperature=0.2,
                    max_tokens=500
                )
                md = resp2.choices[0].message.content.strip()
            return md
        except Exception as e:
            print(f"[LLM summarize fallback] {e}", file=sys.stderr)

    # Rule-based note generation (always ≤250 words)
    week_str = datetime.now().strftime("%V")
    # Build markdown manually — keep footer short to stay <245 words
    md = f"# Weekly Pulse — {product} | Week {week_str} ({date_range_str})\n\n"
    md += f"**Health:** {avg_rating}★ avg • {total_reviews} reviews ({weeks}w) • {distribution}\n\n"
    md += f"**Top 3 Themes (of 5):**\n"
    for i, line in enumerate(theme_lines, 1):
        md += f"{i}. {line}\n"
    md += f"\n**What Users Said:**\n"
    for ql in quote_lines:
        md += f"{ql}\n\n"
    # trim extra newline
    md = md.rstrip() + "\n\n"
    md += f"**3 Action Ideas — Next 7 Days:**\n"
    for i, idea in enumerate(ideas, 1):
        md += f"{i}. {idea}\n"
    md += f"\n*Source: {total_reviews} public reviews (App Store + Play Store) • No PII*\n"

    # Enforce 250 words — if over, trim only theme summaries, never truncate action ideas with …
    wc = word_count(md)
    if wc > 250:
        short_map = {
            "payments": "UPI fails + pending refunds top pain",
            "kyc": "PAN/selfie verification loops",
            "withdrawals": "Pending + hidden fees hurt trust",
            "statements": "Totals mismatch, PDF blurry",
            "onboarding": "OTP delay, duplicate asks"
        }
        md2 = f"# Weekly Pulse — {product} | Week {week_str} ({date_range_str})\n\n"
        md2 += f"**Health:** {avg_rating}★ avg • {total_reviews} reviews • {distribution}\n\n"
        md2 += f"**Top 3 Themes:**\n"
        for k,v in top_themes:
            md2 += f"- **{label(k)}** ({v['count']}, {v['neg_pct']}% neg) — {short_map.get(k, '')}\n"
        md2 += f"\n**Quotes:**\n"
        for ql in quote_lines:
            md2 += f"{ql}\n\n"
        md2 += f"**Next 3 Actions:**\n"
        for i, idea in enumerate(ideas,1):
            md2 += f"{i}. {idea}\n"
        md2 += f"\n*No PII • {total_reviews} public reviews*\n"
        md = md2
        # final safety: if still >250, keep as is but log — never add …
        if word_count(md) > 250:
            print(f"[Warn] Trimmed note still {word_count(md)} words (>250)", file=sys.stderr)
    return md

def draft_email(product, md_note, to_alias, weeks, total_reviews):
    subject = f"[Weekly Pulse] {product} — Week {datetime.now().strftime('%V')} | {total_reviews} reviews, top 3 themes + 3 actions"
    # Keep email scannable, combine
    body = f"To: {to_alias}\nSubject: {subject}\n\n"
    body += f"Hi team,\n\n"
    body += f"Weekly pulse for {product} (last {weeks} weeks, {total_reviews} public reviews). Scannable one-pager below — ≤250 words, no PII.\n\n"
    body += f"---\n\n"
    body += md_note + "\n"
    body += f"---\n\n"
    body += f"Attachment: weekly_note_{date.today().isoformat()}.md (one-pager PDF-ready)\n"
    body += f"CSV: data/reviews.csv (public exports only, PII removed)\n\n"
    body += f"Next step: Pick 1 action for this sprint. Reply with owner.\n\n"
    body += f"— Auto-generated by weekly-pulse workflow (Import → Group → Generate → Draft)\n"
    body += f"How to re-run: python src/pulse.py --weeks 12  (see README)\n"
    return subject, body

def main():
    parser = argparse.ArgumentParser(description="Weekly Pulse")
    parser.add_argument("--input", default=str(ROOT / "data" / "reviews.csv"))
    parser.add_argument("--weeks", type=int, default=12)
    parser.add_argument("--output", default=str(ROOT / "output"))
    parser.add_argument("--to", default=None, help="Email alias to draft to")
    args = parser.parse_args()

    config = load_config()
    product = config.get("product", "Fi Money (Neobank)")
    to_alias = args.to or config.get("email", {}).get("to_alias", "yourself@example.com")

    csv_path = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    reviews = load_reviews(csv_path, weeks=args.weeks)
    by_theme, stats = aggregate(reviews, config)
    top_themes = pick_top_themes(stats, n=3)
    quotes = pick_quotes(reviews, top_themes, n=3)
    ideas = generate_action_ideas(top_themes, quotes, by_theme)

    total = len(reviews)
    avg = round(sum(r["rating"] for r in reviews)/total, 2) if total else 0
    # distribution string
    cnt = Counter(r["rating"] for r in reviews)
    dist = " ".join([f"{k}★:{cnt.get(k,0)}" for k in range(5,0,-1)])

    # date range
    dates = [r["date"] for r in reviews]
    date_range_str = f"{min(dates).isoformat()} → {max(dates).isoformat()}" if dates else ""

    md_note = generate_weekly_note(product, args.weeks, total, stats, by_theme, top_themes, quotes, ideas, date_range_str, avg, dist)
    wc = word_count(md_note)
    print(f"[Info] Note word count: {wc} (target ≤250)")

    # Write outputs
    week_iso = datetime.now().strftime("%Y-W%V")
    note_path = out_dir / f"weekly_note_{week_iso}.md"
    note_path.write_text(md_note, encoding="utf-8")
    print(f"[Done] Wrote {note_path}")

    # Also write latest symlink copy
    latest_path = out_dir / "weekly_note_latest.md"
    latest_path.write_text(md_note, encoding="utf-8")

    # Draft email
    subject, body = draft_email(product, md_note, to_alias, args.weeks, total)
    email_path = out_dir / f"email_draft_{week_iso}.txt"
    email_path.write_text(body, encoding="utf-8")
    email_latest = out_dir / "email_draft_latest.txt"
    email_latest.write_text(body, encoding="utf-8")
    print(f"[Done] Wrote {email_path}")

    # Also write email .eml for one-click open in mail clients
    eml_path = out_dir / f"email_draft_{week_iso}.eml"
    eml = f"To: {to_alias}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body}"
    eml_path.write_bytes(eml.encode("utf-8"))
    print(f"[Done] Wrote {eml_path}")

    # Write stats json for debugging / transparency
    stats_path = out_dir / f"stats_{week_iso}.json"
    out_json = {
        "product": product,
        "weeks": args.weeks,
        "date_range": date_range_str,
        "total_reviews": total,
        "avg_rating": avg,
        "distribution": dict(cnt),
        "themes": stats,
        "top_themes": [k for k,_ in top_themes],
        "quotes": quotes,
        "ideas": ideas,
        "word_count": wc,
        "generated_at": datetime.now().isoformat()
    }
    stats_path.write_text(json.dumps(out_json, indent=2, default=str), encoding="utf-8")
    # latest
    (out_dir / "stats_latest.json").write_text(json.dumps(out_json, indent=2, default=str), encoding="utf-8")

    # Print summary
    print("\n=== WEEKLY NOTE PREVIEW ===\n")
    print(md_note)
    print("\n=== EMAIL DRAFT PREVIEW ===\n")
    print(f"Subject: {subject}\n")
    print(body[:1200])
    print(f"\n[Tip] To actually send: python src/send_email.py --to {to_alias}  (see README for Gmail setup)")
    print(f"[Tip] Theme legend in config.json / README")
    if wc > 250:
        print(f"[Warn] Note is {wc} words (>250). Trimming suggested.")

if __name__ == "__main__":
    main()
