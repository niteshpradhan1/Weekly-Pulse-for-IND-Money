import { useState } from 'react';

const weeklyNote = `# Weekly Pulse — INDMoney | Week 38 (2026-08-05 → 2026-09-18)

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
2. Cut KYC drop-off: autofetch PAN/Aadhaar via registered phone number + inline validation + selfie light guide — Product — Track approval %
3. Make withdrawals transparent: show fee + ETA + confirm account before debit — Ops — Track pending tickets

*Source: 48 public reviews (App Store + Play Store) • No PII*`;

export default function Home() {
  const [weeks, setWeeks] = useState(12);
  return (
    <div style={{ fontFamily: 'Inter, system-ui, -apple-system, sans-serif', maxWidth: 900, margin: '0 auto', padding: 24, background: '#fafafa', minHeight: '100vh' }}>
      <header style={{ borderBottom: '2px solid #e5e7eb', paddingBottom: 16, marginBottom: 24 }}>
        <h1 style={{ fontSize: 28, fontWeight: 800, margin: 0 }}>📊 Weekly Pulse — INDMoney</h1>
        <p style={{ color: '#6b7280', margin: '8px 0 0' }}>App Store + Play Store → One-Page Note (≤250 words) • No PII • Public reviews only</p>
        <p style={{ fontSize: 12, color: '#9ca3af' }}>Same product as LIP Challenge 4 • Workflow: Import → Group (5 themes) → Generate → Draft Email • NEW: KYC autofetch via registered phone</p>
      </header>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
        <div style={{ background: 'white', padding: 16, borderRadius: 12, border: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: 12, color: '#6b7280' }}>Health</div>
          <div style={{ fontSize: 20, fontWeight: 700 }}>2.88★ avg</div>
          <div style={{ fontSize: 12, color: '#6b7280' }}>48 reviews (12w) • 5★:9 4★:8 3★:9 2★:12 1★:10</div>
        </div>
        <div style={{ background: 'white', padding: 16, borderRadius: 12, border: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: 12, color: '#6b7280' }}>Top Themes (of 5)</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>Payments (13, 46% ≤2★)</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>KYC (10, 60% ≤2★)</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>Withdrawals (9, 44% ≤2★)</div>
        </div>
        <div style={{ background: 'white', padding: 16, borderRadius: 12, border: '1px solid #e5e7eb' }}>
          <div style={{ fontSize: 12, color: '#6b7280' }}>Theme Legend (Max 5)</div>
          <div style={{ fontSize: 12 }}>Onboarding • KYC/Verification • Payments • Statements/Portfolio • Withdrawals</div>
          <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 8 }}>Verified via output/stats_latest.json</div>
        </div>
      </section>

      <section style={{ background: 'white', padding: 20, borderRadius: 12, border: '1px solid #e5e7eb', marginBottom: 24, whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: 14 }}>
        <h2 style={{ marginTop: 0 }}>One-Page Weekly Note — 232 words</h2>
        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', margin: 0 }}>{weeklyNote}</pre>
        <div style={{ marginTop: 16, display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <a href="/weekly_note_latest.md" download style={{ background: '#111827', color: 'white', padding: '8px 12px', borderRadius: 8, textDecoration: 'none', fontSize: 13 }}>📄 Download MD</a>
          <a href="https://github.com/niteshpradhan1/Weekly-Pulse-for-IND-Money" target="_blank" style={{ background: 'white', border: '1px solid #e5e7eb', padding: '8px 12px', borderRadius: 8, textDecoration: 'none', color: '#111827', fontSize: 13 }}>GitHub Repo</a>
        </div>
      </section>

      <section style={{ background: 'white', padding: 20, borderRadius: 12, border: '1px solid #e5e7eb', marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>Import → Group → Generate → Draft Email (W3)</h3>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 12 }}>
          <label style={{ fontSize: 13 }}>Weeks:</label>
          <input type="range" min="8" max="12" value={weeks} onChange={e => setWeeks(e.target.value)} />
          <span style={{ fontSize: 13, fontWeight: 600 }}>{weeks}w</span>
          <span style={{ fontSize: 12, color: '#6b7280' }}>→ Top 3 weighted by count × (1+neg%/2)</span>
        </div>
        <ul style={{ fontSize: 13, lineHeight: 1.6 }}>
          <li><b>Import:</b> <code>data/reviews.csv</code> (public exports, rating/title/text/date/store) + PII sanitize <code>src/pulse.py:20</code></li>
          <li><b>Group:</b> 5 themes max via <code>prompts/grouping_prompt.txt</code> + keyword fallback → <code>output/stats_latest.json</code></li>
          <li><b>Quotes:</b> 3 vivid, anonymized, ≤25 words, one per top theme</li>
          <li><b>Actions:</b> 3 shippable ideas with owner + metric — incl. <b>NEW: KYC autofetch via registered phone</b> <code>src/pulse.py:251</code></li>
          <li><b>Email:</b> <code>output/demo_email_combined.eml</code> To: niteshpradhan900@gmail.com, kaushikyashasvi@gmail.com</li>
        </ul>
        <div style={{ background: '#f9fafb', padding: 12, borderRadius: 8, fontSize: 12, fontFamily: 'monospace' }}>
          python3 src/pulse.py --weeks {weeks} --to yourself@example.com<br/>
          python3 src/send_email.py --to niteshpradhan900@gmail.com --smtp
        </div>
      </section>

      <section style={{ background: '#111827', color: 'white', padding: 20, borderRadius: 12 }}>
        <h3 style={{ marginTop: 0, color: 'white' }}>Deliverables</h3>
        <ul style={{ fontSize: 13, lineHeight: 1.8 }}>
          <li>Working prototype: <code>src/pulse.py</code> (CLI) + Streamlit <code>src/app.py</code> + Vercel Next.js here</li>
          <li>Weekly note: <code>output/weekly_note_latest.md</code> (232w, ≤250) — also PDF-ready</li>
          <li>Email draft: <code>output/demo_email*.eml</code> — demo to 2 IDs</li>
          <li>Reviews CSV: <code>data/reviews.csv</code> (48, PII-redacted)</li>
          <li>README: how to re-run + theme legend</li>
        </ul>
        <p style={{ fontSize: 12, color: '#9ca3af' }}>Live on Vercel • GitHub: niteshpradhan1/Weekly-Pulse-for-IND-Money • INDMoney — same as LIP Challenge 4</p>
      </section>
    </div>
  );
}
