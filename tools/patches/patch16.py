import shutil, sys
P='/home/claude/ai-horizon.html';SP='/tmp/claude-0/-home-claude/327151ab-1e8d-5ae2-ac0c-bd4759e557d5/scratchpad/'
shutil.copy(P,'/home/claude/ai-horizon-v2/pre-rbuild.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,c=1):
    global s
    if s.count(o)!=c: sys.exit(f'anchor {s.count(o)}: {o[:80]!r}')
    s=s.replace(o,n)
CARD='''    <div class="lab-card" id="rb">
      <div class="step-h"><span class="step-n">3</span><h3>ركّب صاروخك واختبره</h3></div>
      <p class="lab-note">اختر المهمة والحمولة، ثم ركّب المراحل والمحركات، واضغط «أطلق الصاروخ»: هل يرتفع عن المنصة؟ وإلى أين يصل؟</p>
      <div class="rb-grid">
        <div class="rb-ctl" id="rb-ctl"></div>
        <div class="rb-view"><div id="rb-scene"></div><div class="lab-row"><button class="btn btn-accent" id="rb-go" type="button">أطلق الصاروخ</button><button class="btn btn-ghost" id="rb-f9" type="button">تصميم يشبه فالكون 9</button></div></div>
        <div class="rb-side"><div class="rb-stats" id="rb-stats"></div><div class="rb-res" id="rb-res" aria-live="polite"></div></div>
      </div>
      <p class="legend rk-legend">لعبة تعليمية بأرقام تقريبية مبسطة لصواريخ تعمل بالكيروسين والأكسجين السائل: يدفع كل محرك نحو 850 كيلونيوتن، والحساب بمعادلة الصاروخ لكل مرحلة. ويلزم للوصول إلى المدار نحو 9.3 كم/ث: 7.8 كم/ث هي السرعة المدارية، ونحو 1.5 كم/ث تضيع في مقاومة الجاذبية والهواء.</p>
    </div>
    <div class="rk-two">'''
rep('    <div class="rk-two">',CARD)
rep('  rng.addEventListener("input",paintEq);paintEq();\n  labOff=()=>{clearInterval(timer);};','  rng.addEventListener("input",paintEq);paintEq();\n  const rbOff=rbSetup();\n  labOff=()=>{clearInterval(timer);rbOff();};')
rep('/* ---------- capabilities: voice, comments, team data ---------- */',open(SP+'rk-build.js',encoding='utf-8').read()+'\n/* ---------- capabilities: voice, comments, team data ---------- */')
CSS=r'''
/* rocket builder game */
.rb-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.9fr) minmax(0,1fr);gap:18px;align-items:start}
.rb-ctl{display:flex;flex-direction:column;gap:10px}
.rb-f{display:flex;flex-direction:column;gap:4px}
.rb-l{font-size:.82rem;color:var(--sky-muted);font-weight:600}
.rb-seg{flex-wrap:wrap;border-radius:14px;align-self:flex-start}
.rb-seg button{padding:5px 11px;font-size:.84rem}
.rb-svg{display:block;width:100%;max-width:300px;margin-inline:auto;height:auto;direction:ltr;border-radius:16px}
.rb-svg text{font-family:var(--f-body)}
.rb-k{fill:#ffd796;font-size:10px;direction:rtl}
.rb-n{fill:#fff;font-size:9px;text-anchor:middle}
.rb-view .lab-row{justify-content:center;flex-wrap:wrap;margin-top:10px}
.rb-stats{display:flex;flex-direction:column;gap:6px}
.rb-st{display:flex;justify-content:space-between;gap:10px;font-size:.9rem;border-bottom:1px solid var(--sky-line);padding-bottom:5px}
.rb-st span{color:var(--sky-muted)}
.rb-st b{font-family:var(--f-mono);direction:ltr;unicode-bidi:isolate}
.rb-st.ok b{color:#4fe3a1}.rb-st.warn b{color:#ffc857}.rb-st.bad b{color:#ff8a94}
.rb-bar{position:relative;height:12px;border-radius:9px;background:rgba(255,255,255,.08);margin-top:8px;direction:ltr}
.rb-bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,#7b45ff,#c13fc0)}
.rb-mk{position:absolute;top:-4px;bottom:-4px;width:2px;background:#bdb3e6}
.rb-mk.on{background:#ffd796;width:3px}
.rb-bl{color:var(--sky-muted);font-size:.78rem;line-height:1.6}
.rb-res{margin-top:12px;display:flex;flex-direction:column;gap:6px}
.rb-res h3.ok{color:#4fe3a1}.rb-res h3.no{color:#ff8a94}
.rb-res p{line-height:1.85}
.rb-tips{margin:0;padding-inline-start:18px;color:var(--sky-muted);font-size:.9rem;line-height:1.8}
.rb-count{font-family:var(--f-display);font-size:2.4rem;text-align:center;color:#ffd796}
@media (max-width:980px){.rb-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.rb-side{grid-column:1/-1}}
@media (max-width:640px){.rb-grid{grid-template-columns:minmax(0,1fr)}}
'''
i=s.index('</style>');s=s[:i]+CSS+s[i:]
open(P,'w',encoding='utf-8').write(s);print('ok')
