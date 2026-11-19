import shutil, sys, json, re
P = '/home/claude/ai-horizon.html'
SP = '/tmp/claude-0/-home-claude/327151ab-1e8d-5ae2-ac0c-bd4759e557d5/scratchpad/'
shutil.copy(P, '/home/claude/ai-horizon-v2/pre-solar-gloss.html')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'anchor count {n} != {count}: {old[:90]!r}')
    s = s.replace(old, new)
# 1. terms: categories + new terms
ns = {}; exec(open(SP + 'gloss-terms.py', encoding='utf-8').read(), ns)
a = s.index('const TERMS = [\n'); b = s.index('\n];', a)
rows = []
for line in s[a + len('const TERMS = [\n'):b].split('\n'):
    line = line.strip()
    if not line: continue
    r = json.loads(line.rstrip(','))
    r.append(ns['OLD_CAT'][r[0]]); rows.append(r)
assert len(rows) == 24
names = {r[0] for r in rows}
for r in ns['NEW']:
    assert r[0] not in names, r[0]; names.add(r[0]); rows.append(r)
s = s[:a] + 'const TERMS = [\n' + ',\n'.join('  ' + json.dumps(r, ensure_ascii=False) for r in rows) + s[b:]
# 2. glossary page
a = s.index('function renderGlossary(){'); b = s.index('\nconst QLEVELS', a)
s = s[:a] + open(SP + 'gloss-ui.js', encoding='utf-8').read().rstrip() + '\n' + s[b:]
rep('function goTo(e){ if(e.c==="glossary"){location.hash="glossary";return;}',
    'function goTo(e){ if(e.c==="glossary"){glossPending=e.t;if(location.hash==="#glossary")route();else location.hash="glossary";return;}')
# 3. solar page code
rep('/* ---------- capabilities: voice, comments, team data ---------- */',
    open(SP + 'sol-engine.js', encoding='utf-8').read() + '\n' + open(SP + 'sol-ui.js', encoding='utf-8').read() + '\n/* ---------- capabilities: voice, comments, team data ---------- */')
rep('  else if(h==="sky") renderSky();\n', '  else if(h==="sky") renderSky();\n  else if(h==="solar") renderSolar();\n')
rep('    <div id="t-rocket" class="rk-cta"></div>\n', '    <div id="t-rocket" class="rk-cta"></div>\n    <div id="t-solar" class="sol-cta"></div>\n')
rep('أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، وتشريح الصاروخ،', 'أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، والمجموعة الشمسية الآن، وتشريح الصاروخ،')
rep('  $("#t-rocket").replaceWith(rocketCta(', '  $("#t-solar").replaceWith(solCta("جديد","المجموعة الشمسية الآن","أين الكواكب الثمانية في مداراتها الآن؟ وكم تبعد عنا؟ ومتى يكون كل كوكب في أفضل وضع لرؤيته؟ حرّك الزمن وشاهدها تدور حول الشمس."));\n  $("#t-rocket").replaceWith(rocketCta(')
CSS = r'''
/* solar system now */
.sol-grid{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)}
.sol-fig{max-width:560px;margin-inline:auto;width:100%}
.sol-svg{display:block;width:100%;height:auto;direction:ltr;border-radius:22px}
.sol-svg text{font-family:var(--f-body)}
.sol-lb{fill:#fff;font-size:14px;font-weight:700;text-anchor:middle;paint-order:stroke;stroke:#0b0820;stroke-width:3.5px;pointer-events:none}
.sol-p{cursor:pointer;outline:none}
.sol-p.on .sol-lb{fill:#ffd796}
.sol-p:focus-visible circle:first-child{stroke:#ffd796;stroke-width:2}
.sol-dir{fill:#ffd796;font-size:12px;opacity:.85}
.sol-time{flex-wrap:wrap;justify-content:center}
.sol-time .seg{direction:rtl}
.sol-ctl .seg{flex-wrap:wrap}
.sol-card.on{border-color:var(--c);background:rgba(255,255,255,.11)}
.sk-card.sol-card .sk-chip{color:var(--sky-muted);border-color:var(--sky-line)}
.sk-card.sol-card .sk-chip.sol-near{color:#4fe3a1;border-color:rgba(79,227,161,.5)}
.sol-ev .ev-list .link-btn{margin-top:4px;align-self:flex-start}
.tools .sol-cta{grid-column:1/-1}
@media (max-width:820px){.sol-grid{grid-template-columns:minmax(0,1fr)}}
@media (max-width:560px){.sol-ctl .seg button{padding:6px 10px;font-size:.82rem}.sol-time .seg button{padding:6px 9px;font-size:.8rem}}
/* glossary: tools, filters, cross-links, review cards */
.g-tools{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin-top:14px}
.g-prog{display:flex;align-items:center;gap:8px;font-size:.85rem;color:var(--muted)}
.g-prog>i{display:block;width:110px;height:6px;border-radius:9px;background:var(--surface-2);overflow:hidden}
.g-prog>i b{display:block;height:100%;background:var(--grad,var(--accent))}
.g-prog .link-btn{font-size:.82rem}
.g-chips,.g-letters{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.g-chips button,.g-letters button{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;padding:5px 12px;font:inherit;font-size:.85rem;cursor:pointer}
.g-letters{gap:4px}
.g-letters button{min-width:34px;justify-content:center;padding:3px 9px;font-weight:700}
.g-chips button:hover,.g-letters button:hover{border-color:var(--accent)}
.g-chips button[aria-pressed="true"],.g-letters button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.g-chips small{opacity:.7;font-family:var(--f-mono);font-size:.75rem}
.g-ic{display:inline-flex;color:hsl(var(--h) var(--ic-cs) var(--ic-cl))}
.g-chips button[aria-pressed="true"] .g-ic{color:inherit}
.g-count{color:var(--muted);font-size:.88rem;margin-top:18px}
.terms .term{scroll-margin-top:90px}
.term-top{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.g-known{font-size:.75rem;color:var(--ok);white-space:nowrap}
.g-tag{align-self:flex-start;font-size:.72rem;font-weight:600;border-radius:999px;padding:1px 10px;background:hsl(var(--h) var(--ic-bs) var(--ic-bl));color:hsl(var(--h) var(--ic-cs) var(--ic-cl))}
.g-x{display:inline;background:none;border:0;padding:0;font:inherit;color:var(--accent);cursor:pointer;text-decoration:underline;text-decoration-style:dotted;text-underline-offset:4px}
.g-rel{display:flex;flex-wrap:wrap;gap:2px 12px;align-items:baseline;font-size:.85rem}
.g-rel small{color:var(--muted)}
.term .g-rel .link-btn,.term .g-act .link-btn{align-self:auto;margin-top:0;text-align:start;font-size:.88rem}
.g-act{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center;margin-top:auto;padding-top:4px}
.g-act .link-btn{display:inline-flex;align-items:center;gap:5px}
.term.g-spot{grid-column:1/-1;background:var(--accent-soft);border-color:transparent}
.term.g-spot h3{font-size:1.4rem}
.term.flash{animation:gflash 1.8s ease}
@keyframes gflash{0%,45%{box-shadow:0 0 0 3px var(--accent)}100%{box-shadow:0 0 0 0 transparent}}
.g-fc{max-width:580px;margin:26px auto 70px;display:flex;flex-direction:column;gap:14px}
.g-fc-top{display:flex;justify-content:space-between;color:var(--muted);font-size:.9rem}
.g-card{min-height:250px;width:100%;border-radius:20px;border:1px solid var(--line);background:var(--surface);color:var(--fg);padding:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px;font:inherit;cursor:pointer}
.g-card .g-tag{align-self:center}
.g-card h2{font-size:clamp(1.6rem,5vw,2.2rem)}
.g-card .en{color:var(--muted);font-size:.85rem}
.g-card p{font-size:1.05rem;line-height:1.95;max-width:46ch}
.g-card.g-done{cursor:default}
.g-fc-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
@media (prefers-reduced-motion:reduce){.term.flash{animation:none;box-shadow:0 0 0 3px var(--accent)}}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(rows), 'terms')
