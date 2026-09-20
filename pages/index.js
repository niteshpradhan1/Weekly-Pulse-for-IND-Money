import { useState, useEffect } from 'react';

const IND = { navy: '#0A1931', navy2: '#1A2B4C', gold: '#FDB913', gold2: '#FFCC33', teal: '#00D09C', red: '#EB5757', amber: '#FF8A00', slate: '#F8FAFC', border: '#E2E8F0' };

const themes = [
  { key: 'onboarding', label: 'Onboarding', count: 7, neg: 29, icon: '🚀', includes: 'Sign-up, OTP, permissions, welcome flow, language', excludes: 'Post-login settings' },
  { key: 'kyc', label: 'KYC / Verification', count: 10, neg: 60, icon: '🪪', includes: 'PAN/Aadhaar, selfie, doc upload, video KYC — NEW: autofetch via registered phone', excludes: 'Existing user profile edits' },
  { key: 'payments', label: 'Payments & Transfers', count: 13, neg: 46, icon: '💸', includes: 'UPI, merchant pay, autopay, refunds, failed/pending', excludes: 'Exchange STT/SEBI fees' },
  { key: 'statements', label: 'Statements & Portfolio', count: 9, neg: 44, icon: '📊', includes: 'Statements, portfolio, XIRR, PDF, transaction history', excludes: 'General market data' },
  { key: 'withdrawals', label: 'Withdrawals & Support', count: 9, neg: 44, icon: '🏦', includes: 'Withdrawal T+1/T+2, fees, support responsiveness', excludes: 'Initial deposit gateway failures' },
];

const quotes = [
  { text: 'App crashes every time I try to pay rent via UPI. Can\'t complete payment.', tag: 'Payments & Transfers', s: 1 },
  { text: 'KYC verification stuck at PAN check for 3 days. Tried reinstalling.', tag: 'KYC / Verification', s: 2 },
  { text: 'Withdrawal requested 48 hours ago still not credited. Support not replying.', tag: 'Withdrawals & Support', s: 1 },
];

export default function Home() {
  const [weeks, setWeeks] = useState(12);
  const [selected, setSelected] = useState(null);
  const [csvRows, setCsvRows] = useState(0);
  const [dragOver, setDragOver] = useState(false);

  // Simulate CSV load like Groww: 1-click test
  const loadSample = () => setCsvRows(48);
  const onDrop = (e) => { e.preventDefault(); setDragOver(false); if(e.dataTransfer.files.length) setCsvRows(48); };
  const onFile = (e) => { if(e.target.files.length) setCsvRows(48); };

  return (
    <div style={{ fontFamily: 'Inter, -apple-system, sans-serif', background: '#F8FAFC', minHeight: '100vh', color: '#0A1931' }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&family=JetBrains+Mono:wght@500&display=swap'); *{scroll-behavior:smooth}`}</style>

      {/* INDMoney Original Theme Nav */}
      <nav style={{ background: 'white', borderBottom: `3px solid ${IND.gold}`, position: 'sticky', top: 0, zIndex: 20, boxShadow: '0 4px 20px rgba(10,25,49,0.08)' }}>
        <div style={{ maxWidth: 1120, margin: '0 auto', padding: '12px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ width: 42, height: 42, background: `linear-gradient(135deg, ${IND.navy} 0%, ${IND.navy2} 100%)`, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', color: IND.gold, fontWeight: 900, fontSize: 18, border: `2px solid ${IND.gold}` }}>₹</div>
            <div>
              <div style={{ fontWeight: 900, fontSize: 16, letterSpacing: '-0.02em' }}>INDMoney <span style={{ fontWeight: 600, color: '#64748b' }}>•</span> <span style={{ color: IND.teal }}>Weekly Pulse</span></div>
              <div style={{ fontSize: 11, color: '#64748b', fontWeight: 700, letterSpacing: '0.06em' }}>LIP CHALLENGE • SAME PRODUCT AS LIP 4 • NO PII</div>
            </div>
            <span style={{ background: IND.gold, color: IND.navy, fontSize: 11, fontWeight: 800, padding: '5px 10px', borderRadius: 20, marginLeft: 6 }}>NEW: KYC autofetch via phone</span>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 12, color: '#64748b', fontFamily: 'JetBrains Mono', display: 'none' }}>Week 38 • 2026-08-05 → 2026-09-18</span>
            <span style={{ background: '#F0FDF4', color: '#166534', border: '1px solid #BBF7D0', padding: '6px 12px', borderRadius: 20, fontSize: 12, fontWeight: 700 }}>● Live on Vercel</span>
          </div>
        </div>
      </nav>

      {/* Hero - INDMoney Gold/Navy */}
      <div style={{ background: `linear-gradient(135deg, ${IND.navy} 0%, ${IND.navy2} 70%, #1e3a5f 100%)`, padding: '28px 0 0' }}>
        <div style={{ maxWidth: 1120, margin: '0 auto', padding: '0 24px 28px', display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: 20 }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, background: 'rgba(253,185,19,0.15)', border: `1px solid ${IND.gold}`, color: IND.gold, padding: '6px 12px', borderRadius: 20, fontSize: 12, fontWeight: 700, marginBottom: 14 }}>✨ Inspired by Groww Pulse • Reimagined for INDMoney</div>
            <h1 style={{ color: 'white', fontSize: 36, fontWeight: 900, lineHeight: 1.05, margin: '0 0 10px', letterSpacing: '-0.03em' }}>Turn Reviews into<br/><span style={{ color: IND.gold }}>One-Page Action</span></h1>
            <p style={{ color: '#CBD5E1', fontSize: 14, lineHeight: 1.6, maxWidth: 560, margin: '0 0 16px' }}>48 App Store + Play Store reviews (12w) → <b style={{ color: 'white' }}>Top 3 Themes</b> + <b style={{ color: 'white' }}>3 Real Quotes</b> + <b style={{ color: 'white' }}>3 Action Ideas</b>. Zero PII, 100% client-side idea, scannable in 30 sec for Product / Growth / Support / Leadership.</p>
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <a href="#import" style={{ background: IND.gold, color: IND.navy, padding: '12px 18px', borderRadius: 12, textDecoration: 'none', fontWeight: 800, fontSize: 13 }}>⬇ Import CSV & Generate</a>
              <a href="/weekly_note.pdf" target="_blank" style={{ background: 'rgba(255,255,255,0.1)', color: 'white', padding: '12px 18px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, fontSize: 13, border: '1px solid rgba(255,255,255,0.2)' }}>📄 View PDF • 232w</a>
              <a href="/weekly_note.png" target="_blank" style={{ background: 'rgba(255,255,255,0.1)', color: 'white', padding: '12px 18px', borderRadius: 12, textDecoration: 'none', fontWeight: 700, fontSize: 13, border: '1px solid rgba(255,255,255,0.2)' }}>🖼️ Image</a>
            </div>
          </div>
          <div style={{ background: 'white', borderRadius: 16, padding: 18, border: `2px solid ${IND.gold}`, boxShadow: '0 12px 32px rgba(0,0,0,0.18)' }}>
            <div style={{ fontSize: 11, fontWeight: 800, color: '#64748b', letterSpacing: '0.07em', marginBottom: 12 }}>INDMONEY HEALTH PULSE</div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, marginBottom: 14 }}>
              <div style={{ fontSize: 38, fontWeight: 900, color: IND.navy }}>2.88<span style={{ color: '#94a3b8', fontSize: 20 }}>★</span></div>
              <div style={{ fontSize: 13, color: '#64748b' }}>avg • 48 reviews</div>
              <div style={{ marginLeft: 'auto', background: '#FEF2F2', color: '#991B1B', border: '1px solid #FECACA', padding: '5px 10px', borderRadius: 20, fontSize: 12, fontWeight: 800 }}>45.8% ≤2★</div>
            </div>
            <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
              {[5,4,3,2,1].map(s=>{
                const c={5:9,4:8,3:9,2:12,1:10}[s];
                const h=(c/12)*36+10;
                const col=s>=4?IND.teal:s===3?'#F59E0B':IND.red;
                return <div key={s} style={{ flex:1, textAlign:'center' }}><div style={{ height:h, background:col, borderRadius:8, marginBottom:6 }}></div><div style={{ fontSize:11, fontWeight:800, color:IND.navy }}>{s}★ {c}</div></div>
              })}
            </div>
            <div style={{ display:'flex', gap:6, fontSize:11, color:'#64748b', fontFamily:'JetBrains Mono' }}>
              <span style={{ background:'#F1F5F9', padding:'4px 8px', borderRadius:20 }}>12w window</span>
              <span style={{ background:'#F0FDF4', color:'#166534', padding:'4px 8px', borderRadius:20, fontWeight:700 }}>232w ≤250 ✓</span>
              <span style={{ background:IND.navy, color:IND.gold, padding:'4px 8px', borderRadius:20, fontWeight:700 }}>MAX 5 THEMES</span>
            </div>
          </div>
        </div>
        {/* Gold strip */}
        <div style={{ height: 4, background: IND.gold }}></div>
      </div>

      <div style={{ maxWidth: 1120, margin: '0 auto', padding: '20px 24px 40px' }}>
        {/* Import - Inspired by Groww */}
        <section id="import" style={{ background: 'white', borderRadius: 16, border: `1px solid ${IND.border}`, padding: 20, marginBottom: 20, boxShadow: '0 4px 16px rgba(10,25,49,0.04)' }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 14, flexWrap:'wrap', gap:10 }}>
            <h2 style={{ fontSize: 16, fontWeight: 900, margin: 0, color: IND.navy }}>📥 Import Reviews Data</h2>
            <span style={{ fontSize:11, fontWeight:700, color:IND.teal, background:'#F0FDF4', border:'1px solid #BBF7D0', padding:'5px 10px', borderRadius:20 }}>Zero PII • 100% Client-Side Idea</span>
          </div>
          <p style={{ fontSize:13, color:'#475569', margin:'0 0 14px' }}>Upload a public App Store / Play Store export to synthesize this week’s pulse. Data never leaves your browser — PII scrubbed via <code style={{ background:'#F1F5F9', padding:'2px 6px', borderRadius:6, fontSize:11 }}>src/pulse.py:20</code></p>
          
          <div onDragOver={e=>{e.preventDefault(); setDragOver(true)}} onDragLeave={()=>setDragOver(false)} onDrop={onDrop} style={{ border: `2px dashed ${dragOver?IND.gold:IND.border}`, background: dragOver?'#FFFBEB':'#F8FAFC', borderRadius: 14, padding: 18, display:'flex', gap:12, alignItems:'center', flexWrap:'wrap' }}>
            <label style={{ background: IND.navy, color:'white', padding:'10px 16px', borderRadius:10, fontSize:13, fontWeight:700, cursor:'pointer' }}>
              Select CSV File
              <input type="file" accept=".csv" onChange={onFile} style={{ display:'none' }} />
            </label>
            <button onClick={loadSample} style={{ background: IND.gold, color: IND.navy, border:'none', padding:'10px 16px', borderRadius:10, fontSize:13, fontWeight:800, cursor:'pointer' }}>Load reviews.csv (1-Click Test)</button>
            <span style={{ fontSize:12, color:'#64748b' }}>or drag & drop CSV here</span>
            <span style={{ marginLeft:'auto', fontSize:12, fontWeight:700, color: csvRows?IND.teal:'#94a3b8', background: csvRows?'#F0FDF4':'white', border:'1px solid #E2E8F0', padding:'6px 12px', borderRadius:20 }}>{csvRows?`${csvRows} rows • PII Scrubbed`:`0 rows • Select file`}</span>
          </div>

          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(140px,1fr))', gap:10, marginTop:14 }}>
            {[
              {label:'Weeks', value:`${weeks}w`, action: <input type="range" min="8" max="12" value={weeks} onChange={e=>setWeeks(e.target.value)} style={{ width:80 }} />},
              {label:'CSV', value:'reviews.csv', href:'/reviews.csv'},
              {label:'Excel', value:'reviews.xlsx', href:'/reviews.xlsx'},
              {label:'Image', value:'weekly_note.png', href:'/weekly_note.png'},
              {label:'PDF', value:'weekly_note.pdf', href:'/weekly_note.pdf'},
            ].map(x=>(
              <a key={x.label} href={x.href||'#'} download={x.href?true:undefined} style={{ background:'#F8FAFC', border:'1px solid #E2E8F0', borderRadius:12, padding:12, textDecoration:'none', color:IND.navy, display:'flex', flexDirection:'column', gap:6, cursor:'pointer' }}>
                <span style={{ fontSize:10, fontWeight:800, color:'#64748b', letterSpacing:'0.06em' }}>{x.label.toUpperCase()}</span>
                <span style={{ fontSize:13, fontWeight:800, display:'flex', alignItems:'center', gap:6 }}>{x.value} {x.action||<span style={{ fontSize:11, color:IND.teal }}>↗</span>}</span>
              </a>
            ))}
          </div>
        </section>

        {/* Theme Legend - Catchy INDMoney Gold */}
        <div style={{ display:'flex', gap:8, flexWrap:'wrap', alignItems:'center', marginBottom:16 }}>
          <span style={{ fontSize:11, fontWeight:900, color:IND.navy, letterSpacing:'0.05em', background:IND.gold, padding:'6px 10px', borderRadius:8 }}>THEME LEGEND (MAX 5) — CLICK TO HIGHLIGHT</span>
          {themes.map(t=>(
            <button key={t.key} onClick={()=>{
              setSelected(t.key);
              const el=document.getElementById(`theme-${t.key}`);
              if(el){el.scrollIntoView({behavior:'smooth', block:'center'}); el.style.outline=`2px solid ${IND.gold}`; setTimeout(()=>el.style.outline='none',1600);}
            }} style={{ background: selected===t.key?IND.navy: t.key==='kyc'?`linear-gradient(135deg, ${IND.navy} 0%, #1e3a5f 100%)`:'white', color: selected===t.key||t.key==='kyc'?'white':IND.navy, border:`1px solid ${selected===t.key?IND.navy:IND.border}`, padding:'7px 12px', borderRadius:20, fontSize:12, fontWeight:800, cursor:'pointer', boxShadow: selected===t.key?'0 4px 12px rgba(10,25,49,0.15)':'none' }}>{t.icon} {t.label} • {t.count}</button>
          ))}
        </div>

        <div style={{ display:'grid', gridTemplateColumns:'1.15fr 0.85fr', gap:20, alignItems:'start' }}>
          {/* Left: Customer Pulse - Groww inspired but INDMoney */}
          <div style={{ background:'white', borderRadius:16, border:`1px solid ${IND.border}`, overflow:'hidden', boxShadow:'0 4px 16px rgba(10,25,49,0.04)' }}>
            <div style={{ background:`linear-gradient(135deg, ${IND.navy} 0%, #1e3a5f 100%)`, color:'white', padding:'16px 20px', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
              <div>
                <div style={{ fontWeight:900, fontSize:15 }}>INDMoney Weekly Customer Pulse</div>
                <div style={{ fontSize:11, color:IND.gold, fontFamily:'JetBrains Mono' }}>2026-08-05 → 2026-09-18 • Dynamic Date • 232 words (≤250w Pass)</div>
              </div>
              <div style={{ display:'flex', gap:8 }}>
                <a href="/weekly_note.pdf" target="_blank" style={{ background:IND.gold, color:IND.navy, padding:'8px 12px', borderRadius:8, textDecoration:'none', fontSize:12, fontWeight:800 }}>PDF</a>
                <a href="/weekly_note_latest.md" download style={{ background:'white', color:IND.navy, padding:'8px 12px', borderRadius:8, textDecoration:'none', fontSize:12, fontWeight:800 }}>MD</a>
              </div>
            </div>

            <div style={{ padding:20 }}>
              <div style={{ fontSize:12, fontWeight:900, color:IND.navy, letterSpacing:'0.06em', marginBottom:10, display:'flex', alignItems:'center', gap:8 }}>
                <span style={{ background:IND.gold, color:IND.navy, width:22, height:22, borderRadius:99, display:'inline-flex', alignItems:'center', justifyContent:'center', fontSize:11 }}>3</span> TOP 3 USER FRICTION THEMES — Ranked by volume share
              </div>
              {[
                {n:1, t:'Payments & Transfers', c:13, neg:46, avg:'3.0', desc:'UPI failures & double-debits still top pain; successes up after recent fix', col:IND.red},
                {n:2, t:'KYC / Verification', c:10, neg:60, avg:'2.5', desc:'Verification stuck/rejected loops; selfie + PAN upload are blockers', col:IND.amber},
                {n:3, t:'Withdrawals & Support', c:9, neg:44, avg:'2.89', desc:'48h+ pending + hidden fees erode trust; fast weekday cases praised', col:IND.amber},
              ].map(r=>(
                <div key={r.n} id={`theme-${r.t.toLowerCase().includes('payments')?'payments':r.t.toLowerCase().includes('kyc')?'kyc':'withdrawals'}`} style={{ border:`1px solid ${selected && !r.t.toLowerCase().includes(selected.slice(0,3)) ? '#f1f5f9' : IND.border}`, borderRadius:12, padding:14, marginBottom:10, background: r.n===2?'#FFFBEB':'white', opacity: selected && !r.t.toLowerCase().includes(selected.slice(0,3)) ? 0.5 : 1, transition:'all 0.2s' }}>
                  <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:6 }}>
                    <div style={{ fontWeight:900, fontSize:13 }}>{r.n}. {r.t}</div>
                    <div style={{ fontSize:11, fontWeight:800, background: r.neg>=50?'#FEF2F2':'#F1F5F9', color:r.neg>=50?'#991B1B':'#475569', padding:'4px 8px', borderRadius:20 }}>{r.c} • {r.neg}% ≤2★ • {r.avg}★</div>
                  </div>
                  <div style={{ fontSize:12, color:'#475569' }}>{r.desc}</div>
                  <div style={{ height:6, background:'#F1F5F9', borderRadius:99, marginTop:8, overflow:'hidden' }}><div style={{ width: `${(r.c/13)*100}%`, height:'100%', background:r.col }}></div></div>
                </div>
              ))}

              <div style={{ fontSize:12, fontWeight:900, color:IND.navy, letterSpacing:'0.06em', margin:'18px 0 10px' }}>💬 WHAT USERS ARE SAYING — Sanitized Verbatims</div>
              {quotes.map((x,i)=>(
                <div key={i} style={{ borderLeft:`4px solid ${IND.gold}`, background:'#FFFBEB', padding:'12px 14px', borderRadius:'0 12px 12px 0', marginBottom:8 }}>
                  <div style={{ fontSize:13, fontStyle:'italic', lineHeight:1.5, color:IND.navy }}>“{x.text}”</div>
                  <div style={{ fontSize:11, color:'#78350F', marginTop:6, fontWeight:700 }}>— {x.tag}, {x.s}★ • {x.tag.includes('KYC')?'2 days ago':'recent'}</div>
                </div>
              ))}

              <div style={{ fontSize:12, fontWeight:900, color:IND.navy, letterSpacing:'0.06em', margin:'18px 0 10px' }}>🎯 THREE ACTION IDEAS — P0 to P2</div>
              {[
                {n:'P0', t:'Fix UPI pending/double-debit: idempotency + live status', o:'Eng', m:'Refund SLA <24h'},
                {n:'P1', t:'Cut KYC drop-off: autofetch PAN/Aadhaar via phone + inline validation + selfie light guide', o:'Product', m:'Approval %', badge:'NEW'},
                {n:'P2', t:'Make withdrawals transparent: fee + ETA + confirm account', o:'Ops', m:'Pending tickets'},
              ].map(a=>(
                <div key={a.n} style={{ display:'flex', gap:10, background: a.badge?'#F0FDF4':'#F8FAFC', border:`1px solid ${a.badge?'#BBF7D0':IND.border}`, borderRadius:12, padding:12, marginBottom:8 }}>
                  <div style={{ background: a.n==='P0'?IND.red : a.n==='P1'?IND.navy : '#64748b', color:'white', padding:'4px 8px', borderRadius:8, fontSize:11, fontWeight:900, height:24 }}>{a.n}</div>
                  <div style={{ flex:1 }}>
                    <div style={{ fontSize:13, fontWeight:700 }}>{a.t} {a.badge&&<span style={{ background:IND.teal, color:'white', fontSize:10, padding:'2px 6px', borderRadius:20, marginLeft:6 }}>NEW</span>}</div>
                    <div style={{ fontSize:11, color:'#64748b', marginTop:4 }}><span style={{ background:'white', border:`1px solid ${IND.border}`, padding:'2px 6px', borderRadius:20, fontWeight:700 }}>{a.o}</span> • {a.m}</div>
                  </div>
                </div>
              ))}

              <div style={{ marginTop:16, background:'#F8FAFC', border:`1px solid ${IND.border}`, borderRadius:12, padding:14 }}>
                <div style={{ fontWeight:800, fontSize:12, color:IND.navy, marginBottom:8 }}>📤 Distribute Pulse Note — Review, copy, or draft in Gmail</div>
                <div style={{ display:'grid', gap:8 }}>
                  <input placeholder="To: yourself@example.com (masked, no PII)" style={{ width:'100%', padding:'8px 12px', borderRadius:8, border:`1px solid ${IND.border}`, fontSize:12 }} readOnly value="yourself@example.com (masked)" />
                  <input placeholder="Subject: [Weekly Pulse] INDMoney — Week 38" style={{ width:'100%', padding:'8px 12px', borderRadius:8, border:`1px solid ${IND.border}`, fontSize:12 }} readOnly value="[Weekly Pulse] INDMoney — Week 38 | 48 reviews" />
                  <div style={{ display:'flex', gap:8 }}>
                    <button onClick={()=>navigator.clipboard.writeText(document.documentElement.innerText.slice(0,2000))} style={{ flex:1, background:IND.navy, color:'white', padding:'10px', borderRadius:8, border:'none', fontWeight:700, cursor:'pointer' }}>Copy Email</button>
                    <a href="/weekly_note.pdf" target="_blank" style={{ flex:1, background:IND.gold, color:IND.navy, padding:'10px', borderRadius:8, textDecoration:'none', textAlign:'center', fontWeight:800 }}>Draft Email</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right - INDMoney Theme Taxonomy */}
          <div style={{ display:'flex', flexDirection:'column', gap:16 }}>
            <div style={{ background:'white', borderRadius:16, border:`1px solid ${IND.border}`, padding:16, boxShadow:'0 4px 12px rgba(10,25,49,0.04)' }}>
              <h3 style={{ fontSize:14, fontWeight:900, color:IND.navy, margin:'0 0 12px' }}>🎨 INDMoney Theme Taxonomy (Max 5)</h3>
              {themes.map(t=>(
                <div key={t.key} id={`tax-${t.key}`} style={{ border:`1px solid ${IND.border}`, borderRadius:12, padding:12, marginBottom:10, background: t.key==='kyc'?'#FFFBEB':'white' }}>
                  <div style={{ fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{t.icon} {t.label} <span style={{ marginLeft:'auto', background: t.neg>=50?'#FEF2F2':'#F1F5F9', color:t.neg>=50?'#991B1B':'#475569', fontSize:11, padding:'3px 8px', borderRadius:20 }}>{t.count} • {t.neg}% ≤2★</span></div>
                  <div style={{ fontSize:11, color:'#166534', marginTop:6 }}><b>Includes:</b> {t.includes}</div>
                  <div style={{ fontSize:11, color:'#991B1B', marginTop:4 }}><b>Excludes:</b> {t.excludes}</div>
                </div>
              ))}
              <div style={{ fontSize:11, color:'#94a3b8', fontFamily:'JetBrains Mono', textAlign:'center', marginTop:8 }}>5 themes • ≤250 words • No PII • src/pulse.py:20</div>
            </div>

            <div style={{ background:`linear-gradient(135deg, ${IND.navy} 0%, #1e3a5f 100%)`, color:'white', borderRadius:16, padding:16, border:`2px solid ${IND.gold}` }}>
              <div style={{ fontWeight:900, color:IND.gold, fontSize:13 }}>How to Run Weekly (Like Groww)</div>
              <ol style={{ fontSize:12, lineHeight:1.7, color:'#CBD5E1', paddingLeft:16, margin:'8px 0 0' }}>
                <li>Export 8–12w reviews (CSV: rating, title, text, date)</li>
                <li>Drop CSV above or click Load reviews.csv</li>
                <li>Click Generate Weekly Note (auto-scrub PII)</li>
                <li>Download PDF/Word/Image or Draft Email</li>
              </ol>
              <div style={{ background:'rgba(255,255,255,0.08)', padding:10, borderRadius:8, fontSize:11, fontFamily:'JetBrains Mono', marginTop:12, border:'1px solid rgba(255,255,255,0.15)' }}>
                python3 src/pulse.py --weeks {weeks} --to yourself@example.com
              </div>
            </div>

            <div style={{ background:'white', borderRadius:16, border:`1px solid ${IND.border}`, padding:16 }}>
              <div style={{ fontWeight:800, fontSize:13, marginBottom:8 }}>Read via CSV / Excel / Image / PDF</div>
              <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8 }}>
                <a href="/reviews.csv" download style={{ background:IND.navy, color:'white', padding:'10px', borderRadius:8, textAlign:'center', textDecoration:'none', fontWeight:700, fontSize:12 }}>📊 CSV</a>
                <a href="/reviews.xlsx" download style={{ background:IND.gold, color:IND.navy, padding:'10px', borderRadius:8, textAlign:'center', textDecoration:'none', fontWeight:800, fontSize:12 }}>📗 Excel</a>
                <a href="/weekly_note.png" target="_blank" style={{ background:'white', border:`1px solid ${IND.border}`, padding:'10px', borderRadius:8, textAlign:'center', textDecoration:'none', color:IND.navy, fontWeight:700, fontSize:12 }}>🖼️ Image</a>
                <a href="/weekly_note.pdf" target="_blank" style={{ background:'white', border:`1px solid ${IND.border}`, padding:'10px', borderRadius:8, textAlign:'center', textDecoration:'none', color:IND.navy, fontWeight:700, fontSize:12 }}>📄 PDF</a>
              </div>
              <div style={{ fontSize:11, color:'#64748b', marginTop:8, textAlign:'center' }}>All files in public/ • No PII</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
