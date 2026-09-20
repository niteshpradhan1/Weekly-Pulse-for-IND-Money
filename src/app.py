import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from pulse import load_reviews, aggregate, pick_top_themes, pick_quotes, generate_action_ideas, generate_weekly_note, draft_email, load_config, word_count

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Weekly Pulse — Reviews to One-Pager", layout="wide", page_icon="📊")

st.title("📊 Weekly Pulse — App Reviews → One-Page Note")
st.caption("Import → Group (5 themes) → Generate Note (≤250 words) → Draft Email • No PII • Public reviews only")

with st.sidebar:
    st.header("Config")
    cfg = load_config()
    product = st.text_input("Product", value=cfg.get("product","Fi Money (Neobank)"))
    weeks = st.slider("Weeks window", 8, 12, 12)
    to_alias = st.text_input("Email alias (draft to yourself)", value=cfg.get("email",{}).get("to_alias","yourself@example.com"))
    uploaded = st.file_uploader("Upload reviews.csv (or use data/reviews.csv)", type=["csv"])
    st.divider()
    st.markdown("**Theme Legend**")
    for k, v in cfg.get("themes",{}).items():
        st.markdown(f"**{v['label']}** — {v['description']}")
    st.divider()
    st.caption("W2: LLM prompting for grouping/summarization (falls back to rules). W3: Full workflow automation.")

# Load reviews
if uploaded:
    tmp = ROOT / "data" / "_uploaded.csv"
    tmp.write_bytes(uploaded.getvalue())
    csv_path = tmp
else:
    csv_path = ROOT / "data" / "reviews.csv"

if not csv_path.exists():
    st.error("No reviews.csv found. Upload one with columns: rating,title,text,date,store")
    st.stop()

reviews = load_reviews(csv_path, weeks=weeks)
config = load_config()
config["product"] = product
by_theme, stats = aggregate(reviews, config)
top_themes = pick_top_themes(stats, n=3)
quotes = pick_quotes(reviews, top_themes, n=3)
ideas = generate_action_ideas(top_themes, quotes, by_theme)

total = len(reviews)
avg = round(sum(r["rating"] for r in reviews)/total,2) if total else 0
import collections
cnt = collections.Counter(r["rating"] for r in reviews)
dist = " ".join([f"{k}★:{cnt.get(k,0)}" for k in range(5,0,-1)])
date_range = f"{min(r['date'] for r in reviews).isoformat()} → {max(r['date'] for r in reviews).isoformat()}" if reviews else ""

md_note = generate_weekly_note(product, weeks, total, stats, by_theme, top_themes, quotes, ideas, date_range, avg, dist)
subject, body = draft_email(product, md_note, to_alias, weeks, total)
wc = word_count(md_note)

col1, col2 = st.columns([2,1])
with col1:
    st.subheader(f"One-Page Weekly Note • {wc} words" + (" ✅" if wc<=250 else " ⚠️ >250"))
    st.markdown(md_note)
    st.download_button("📄 Download Note (MD)", md_note, file_name="weekly_note.md")
    st.download_button("📧 Download Email Draft (.txt)", body, file_name="email_draft.txt")
    st.download_button("📧 Download Email Draft (.eml)", f"To: {to_alias}\r\nSubject: {subject}\r\n\r\n{body}".encode(), file_name="weekly_note.eml")

with col2:
    st.metric("Reviews", total)
    st.metric("Avg Rating", f"{avg} ★")
    st.metric("Weeks", weeks)
    st.write(dist)
    st.divider()
    st.subheader("Top Themes")
    for k, v in top_themes:
        label = config["themes"].get(k,{}).get("label",k)
        st.markdown(f"**{label}** — {v['count']} ({v['neg_pct']}% ≤2★)")
        st.progress(v["count"]/max(x["count"] for x in stats.values()) )
    st.divider()
    st.subheader("Quotes (anonymized)")
    for q in quotes:
        label = config["themes"].get(q["theme"],{}).get("label",q["theme"])
        st.info(f"“{q['text']}” — {label}, {q['rating']}★")
    st.divider()
    st.subheader("Action Ideas")
    for i, idea in enumerate(ideas,1):
        st.markdown(f"{i}. {idea}")

st.divider()
st.subheader("All Reviews (grouped, PII-removed)")
df = pd.DataFrame([{"date": r["date"], "store": r["store"], "rating": r["rating"], "theme": config["themes"].get(r["theme"],{}).get("label",r["theme"]), "title": r["title"], "text": r["text"]} for r in reviews])
st.dataframe(df, use_container_width=True, height=300)
st.download_button("⬇️ Download Grouped CSV", df.to_csv(index=False).encode(), file_name="reviews_grouped.csv")

st.caption("No usernames/emails/IDs stored. Sources: Public App Store + Play Store exports only.")
