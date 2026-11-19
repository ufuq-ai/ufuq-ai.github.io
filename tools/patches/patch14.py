import shutil, sys
P = '/home/claude/ai-horizon.html'
SP = '/tmp/claude-0/-home-claude/327151ab-1e8d-5ae2-ac0c-bd4759e557d5/scratchpad/'
shutil.copy(P, '/home/claude/ai-horizon-v2/pre-saudi.html')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'anchor count {n} != {count}: {old[:90]!r}')
    s = s.replace(old, new)
rep('      <a href="#lab" data-r="lab">المختبر</a>\n', '      <a href="#lab" data-r="lab">المختبر</a>\n      <a href="#saudi" data-r="saudi">السعودية والفضاء</a>\n')
rep('  else if(h==="solar") renderSolar();\n', '  else if(h==="solar") renderSolar();\n  else if(h==="saudi") renderSaudi();\n')
rep('/* ---------- capabilities: voice, comments, team data ---------- */',
    open(SP + 'saudi-ui.js', encoding='utf-8').read() + '\n/* ---------- capabilities: voice, comments, team data ---------- */')
CSS = r'''
/* Saudi Arabia and space */
.sa-hero{position:relative;overflow:hidden;color:#fff;min-height:360px;display:flex;align-items:flex-end;background:#070b24}
.sa-banner{position:absolute;inset:0;width:100%;height:100%}
.sa-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,30,.05) 0%,rgba(5,8,30,.35) 45%,rgba(5,8,30,.78) 100%)}
.sa-hero-in{position:relative;z-index:1;padding-block:80px 28px}
.sa-hero .kick{color:#ffd796}
.sa-hero h1{font-size:clamp(2rem,6vw,3.1rem);color:#fff;margin:4px 0 8px}
.sa-hero p{max-width:640px;color:#e9ecff;line-height:1.9;font-size:1.05rem}
.sa-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;max-width:780px;margin-top:22px}
.sa-stats div{padding:10px 8px;border-radius:14px;background:rgba(10,14,40,.6);border:1px solid rgba(255,255,255,.18);text-align:center}
.sa-stats b{display:block;font-family:var(--f-display);font-size:1.6rem;line-height:1.3;color:#fff}
.sa-stats span{display:block;font-size:.8rem;color:#d5dbff;line-height:1.5}
.sa{padding-block:34px 70px;display:flex;flex-direction:column;gap:48px}
.sa-sec h2{font-size:clamp(1.35rem,3.4vw,1.8rem);margin:4px 0 6px}
.sa-tl{list-style:none;margin:18px 0 0;padding:0;position:relative}
.sa-tl::before{content:"";position:absolute;inset-inline-start:11px;top:10px;bottom:10px;width:2px;background:linear-gradient(var(--accent),var(--ok))}
.sa-step{position:relative;padding-inline-start:38px;margin-bottom:10px}
.sa-dot{position:absolute;inset-inline-start:4px;top:19px;width:16px;height:16px;border-radius:50%;background:var(--surface);border:3px solid var(--accent)}
.sa-step.next .sa-dot{border-color:var(--gold,#b86b00);border-style:dashed}
.sa-head{display:grid;grid-template-columns:minmax(118px,auto) minmax(0,1fr) auto;gap:2px 14px;align-items:baseline;width:100%;text-align:start;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 16px;color:var(--fg);font:inherit;cursor:pointer}
.sa-head:hover,.sa-head[aria-expanded="true"]{border-color:var(--accent)}
.sa-when{grid-row:1/3;font-family:var(--f-display);font-weight:700;color:var(--accent);font-size:.95rem}
.sa-head b{font-size:1.02rem}
.sa-line{grid-column:2;color:var(--muted);font-size:.9rem;line-height:1.7}
.sa-chip{grid-column:3;grid-row:1;font-size:.75rem;border:1px solid currentColor;color:var(--gold,#b86b00);border-radius:999px;padding:1px 10px}
.sa-detail{margin:8px 0 6px;padding:14px 16px;background:var(--surface-2);border-radius:12px}
.sa-entry p{line-height:1.9;font-size:.95rem}
.sa-meta{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;margin-top:8px;font-size:.82rem;color:var(--muted)}
.sa-meta .src-link{font-size:.82rem}
.sa-tag{font-size:.72rem;border-radius:999px;padding:1px 9px;background:var(--warn-soft);color:var(--warn)}
.sa-meta .link-btn{margin-inline-start:auto;font-size:.88rem}
.sa-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:12px;margin-top:16px}
.sa-card h3{font-size:1.08rem}
.sa-ec .count{margin:2px 0}
.sa-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.sa-wabar{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:22px;align-items:start;margin-top:16px}
.sa-crater-wrap{background:#0f0b26;border-radius:14px;padding:14px}
.sa-crater{display:block;width:100%;height:auto;direction:ltr}
.sa-crater text{fill:#f1e9ff;font-size:11px;text-anchor:middle;font-family:var(--f-body)}
.sa-crater .sa-cm{fill:#ffd796;font-size:10px}
.sa-crater-wrap .legend{color:#c9c0ea;margin-top:6px}
.sa-fact+.sa-fact{border-top:1px solid var(--line);padding-top:12px;margin-top:12px}
.sa-fact h3{font-size:1rem;margin-bottom:4px}
.sa-quiz{max-width:760px;margin-top:16px}
.sa-quiz>.btn{align-self:flex-start}
.sa-note{text-align:center}
@media (max-width:820px){.sa-wabar{grid-template-columns:minmax(0,1fr)}}
@media (max-width:640px){.sa-stats{grid-template-columns:repeat(2,minmax(0,1fr))}.sa-stats b{font-size:1.35rem}}
@media (max-width:560px){.sa-head{grid-template-columns:minmax(0,1fr) auto}.sa-when{grid-row:auto}.sa-head b,.sa-line{grid-column:1/-1}.sa-chip{grid-column:2;grid-row:1}}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
