import shutil, sys, json, re
P = '/home/claude/ai-horizon.html'
SP = '/tmp/claude-0/-home-claude/327151ab-1e8d-5ae2-ac0c-bd4759e557d5/scratchpad/'
shutil.copy(P, '/home/claude/ai-horizon-v2/pre-quiz2.html')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'anchor count {n} != {count}: {old[:90]!r}')
    s = s.replace(old, new)
# --- resolve refs of new questions
a = s.index('const KB_RAW = ['); b = s.index('const SRC', a)
titles = {t: k for k, t in re.findall(r'\["(K\d+)",\s*"\w+",\s*"([^"]*)"', s[a:b])}
ta = s.index('const TERMS = [\n'); tb = s.index('\n];', ta)
terms = [json.loads(l.strip().rstrip(','))[0] for l in s[ta + len('const TERMS = [\n'):tb].split('\n') if l.strip()]
ns = {}; exec(open(SP + 'quiz-new.py', encoding='utf-8').read(), ns)
qa = s.index('const QUIZ=['); qb = s.index('\n];', qa)
old_q = s[qa:qb]
existing = set(re.findall(r'^ \["([^"]+)"', old_q, re.M))
rows = []
for q, opts, why, ref, lvl in ns['NEW_Q']:
    if ref.startswith('G:'): rid = 'G%d' % (terms.index(ref[2:]) + 1)
    else: rid = titles[ref]
    assert q not in existing, q
    rows.append(' ' + json.dumps([q, opts, 0, why, rid, lvl], ensure_ascii=False))
s = s[:qb] + ',\n' + ',\n'.join(rows) + s[qb:]
# --- quiz page
a = s.index('function renderQuiz(){'); b = s.index('\nfunction ', a + 10)
s = s[:a] + open(SP + 'quiz-ui.js', encoding='utf-8').read().rstrip() + '\n' + s[b:]
# --- glossary: matching game mode
rep('const bL=el("button",null,"القائمة"),bF=el("button",null,"بطاقات المراجعة");bL.type=bF.type="button";seg.append(bL,bF);',
    'const bL=el("button",null,"القائمة"),bF=el("button",null,"بطاقات المراجعة"),bM=el("button",null,"لعبة التوصيل");bL.type=bF.type=bM.type="button";seg.append(bL,bF,bM);')
rep('  function refresh(){if(mode==="list")draw();else cards();}\n  function setMode(m){mode=m;if(m==="cards")f.value="";bL.setAttribute("aria-pressed",String(m==="list"));bF.setAttribute("aria-pressed",String(m==="cards"));f.hidden=m==="cards";refresh();}\n  bL.onclick=()=>setMode("list");bF.onclick=()=>setMode("cards");',
    open(SP + 'gloss-match.js', encoding='utf-8').read().rstrip() + '\n  function refresh(){clearInterval(mTimer);mTimer=0;if(mode==="list")draw();else if(mode==="cards")cards();else match();}\n  function setMode(m){mode=m;if(m!=="list")f.value="";bL.setAttribute("aria-pressed",String(m==="list"));bF.setAttribute("aria-pressed",String(m==="cards"));bM.setAttribute("aria-pressed",String(m==="match"));f.hidden=m!=="list";letters.hidden=m==="match";if(m!=="match"){clearInterval(mTimer);mTimer=0;}refresh();}\n  bL.onclick=()=>setMode("list");bF.onclick=()=>setMode("cards");bM.onclick=()=>setMode("match");')
CSS = r'''
/* quiz: topics, modes, timed challenge, review, certificate */
.q-topics{margin-top:0}
.qbox .lv[disabled]{opacity:.5;cursor:default}
.q-sub{font-size:1rem;color:var(--muted);margin-top:6px}
.q-modes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.q-mode{display:flex;flex-direction:column;align-items:flex-start;gap:4px;text-align:start;background:var(--surface-2);border:1.5px solid transparent;border-radius:14px;padding:14px;font:inherit;color:var(--fg);cursor:pointer}
.q-mode:hover:not([disabled]){border-color:var(--accent)}
.q-mode[disabled]{opacity:.55;cursor:default}
.q-mic{display:inline-flex;color:var(--accent)}
.q-mode b{font-family:var(--f-display);font-size:1.05rem}
.q-mode small{color:var(--muted);font-size:.82rem;line-height:1.6}
.q-mode small.bst{color:var(--accent)}
.q-timebar{height:8px;border-radius:9px;background:var(--surface-2);overflow:hidden}
.q-timebar i{display:block;height:100%;background:var(--grad,var(--accent));transition:width .2s linear}
.q-tleft{font-family:var(--f-mono);color:var(--accent)}
.q-stage{display:flex;flex-direction:column;gap:14px}
.q-review{display:flex;flex-direction:column;gap:10px}
.q-rev{border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:4px}
.q-rev b{font-size:.98rem;line-height:1.7}
.q-rev .ans{color:var(--ok);font-weight:600;font-size:.92rem}
.q-rev p{color:var(--muted);font-size:.9rem;line-height:1.8}
.q-rev .link-btn{align-self:flex-start}
.q-cert-req{display:flex;flex-wrap:wrap;gap:8px}
.q-cert-req button{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;padding:5px 14px;font:inherit;font-size:.9rem;cursor:pointer}
.q-cert-req button.ok{border-color:var(--ok);color:var(--ok);background:var(--ok-soft)}
.q-name{display:flex;gap:8px;flex-wrap:wrap}
.q-name input{flex:1;min-width:200px;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:12px;padding:10px 14px;font:inherit}
.q-cert-out{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.q-cert-img{width:100%;border-radius:12px;border:1px solid var(--line)}
@media (max-width:640px){.q-modes{grid-template-columns:minmax(0,1fr)}}
/* glossary: matching game */
.g-match{display:flex;flex-direction:column;gap:14px;margin:22px 0 70px}
.g-mhead{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between}
.g-mstat{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.88rem;color:var(--muted);font-family:var(--f-body)}
.g-mstat .bst{color:var(--accent)}
.g-mgrid{display:grid;grid-template-columns:minmax(0,.75fr) minmax(0,1.6fr);gap:14px;align-items:start}
.g-mcol{display:flex;flex-direction:column;gap:8px}
.g-mt,.g-md{text-align:start;background:var(--surface);color:var(--fg);border:1.5px solid var(--line);border-radius:12px;padding:10px 14px;font:inherit;cursor:pointer;transition:border-color .15s,background .15s}
.g-mt{font-family:var(--f-display);font-weight:700}
.g-md{font-size:.92rem;line-height:1.8;color:var(--muted)}
.g-mt:hover:not([disabled]),.g-md:hover:not([disabled]){border-color:var(--accent)}
.g-mt[aria-pressed="true"],.g-md[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft);color:var(--fg)}
.g-mt.ok,.g-md.ok{border-color:var(--ok);background:var(--ok-soft);color:var(--fg);cursor:default}
.g-mt.bad,.g-md.bad{border-color:var(--bad);background:var(--bad-soft);animation:gshake .4s}
@keyframes gshake{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
.g-mdone{background:var(--accent-soft);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:8px}
.g-mdone .g-fc-row{justify-content:flex-start}
@media (max-width:640px){.g-mgrid{grid-template-columns:minmax(0,1fr)}.g-mterms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (prefers-reduced-motion:reduce){.g-mt.bad,.g-md.bad{animation:none}}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(rows), 'new questions')
