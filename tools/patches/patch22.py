# v1.1: (a) a permanent line in «اسأل أفق» saying it answers from the verified entries and does not invent,
#       (b) a dismissible «ابدأ من هنا» first-visit tour card on home: lab, rocket workshop, encyclopedia, ticked as visited.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:80])
    s=s.replace(o,n)

# ---------- (a) trust line in the assistant drawer ----------
rep('<div class="msg bot"><p>أهلًا! أنا أفق. اسألني عن أي شيء في الفلك والفضاء، وسأجيبك ببساطة، وأوضح لك ما هو مثبت بالرصد وما زال فرضية.</p></div>',
    '<div class="msg bot"><p>أهلًا! أنا أفق. اسألني عن أي شيء في الفلك والفضاء، وسأجيبك ببساطة، وأوضح لك ما هو مثبت بالرصد وما زال فرضية.</p>'
    '<p class="trust"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/></svg><span id="ai-trust"></span></p></div>')
rep('let aiOff=false,kbNoted=false;\nfunction setAIOff(){\n  if(aiOff)return;aiOff=true;\n',
    'let aiOff=false,kbNoted=false;\n'
    'function setTrust(){const t=$("#ai-trust");if(t)t.textContent=aiOff'
    '?"يبحث أفق في "+arN(KN,W_INFO)+" موثقة و"+arN(KB.length-KN,["مصطلح واحد","مصطلحين","مصطلحات","مصطلحًا"])+" من القاموس، ويجيبك بنصها مع مصدرها. وإذا لم يجد الجواب أخبرك بذلك، ولا يخترع إجابة."'
    ':"يبني أفق جوابه على "+arN(KN,W_INFO)+" موثقة في الموسوعة ويذكر مصدرها، وإذا أجاب من معرفته العامة نبّهك.";}\n'
    'setTrust();\n'
    'function setAIOff(){\n  if(aiOff)return;aiOff=true;setTrust();\n')
rep('.msg .note{display:block;margin-top:8px;font-size:.8rem;color:#ffd796}',
    '.msg .note{display:block;margin-top:8px;font-size:.8rem;color:#ffd796}\n'
    '.msg .trust{display:flex;gap:8px;align-items:flex-start;margin-top:10px;padding:8px 10px;border-radius:10px;background:rgba(79,227,161,.09);border:1px solid rgba(79,227,161,.3);color:#bdf3d8;font-size:.84rem;line-height:1.75}\n'
    '.msg .trust svg{flex:none;margin-top:3px;color:#4fe3a1}')

# ---------- (b) «ابدأ من هنا» tour card on home ----------
rep('''  </section>
  <section class="sec"><div class="wrap">
    <h2>ما الذي يميز أفق؟</h2>''','''  </section>
  <div id="start-sec"></div>
  <section class="sec"><div class="wrap">
    <h2>ما الذي يميز أفق؟</h2>''')
rep('''  $("#feat-ask").onclick=()=>openDrawer();
''','''  $("#feat-ask").onclick=()=>openDrawer();
  startCard();
''')
rep('function renderHome(){','''const TOUR_K="ufuq-tour",TOUR_OFF="ufuq-tour-off";
function tourMark(k){const t=store.get(TOUR_K,{})||{};if(t[k])return;t[k]=1;store.set(TOUR_K,t);}
function startCard(){
  const ph=$("#start-sec");if(!ph)return;
  if(store.get(TOUR_OFF,false)){ph.remove();return;}
  const t=Object.assign({},store.get(TOUR_K,{})||{});if(readSet.size)t.enc=1;
  const BOOK='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5c-.8 0-1.5.6-1.5 1.4z"/><path d="M20 5.5c0-.8-.7-1.5-1.5-1.5H13v15h5.5c.8 0 1.5.6 1.5 1.4z"/><path d="M6.5 8h2.5M6.5 11h2.5M15 8h2.5M15 11h2.5"/></svg>';
  const CHECK='<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>';
  const steps=[
    {k:"lab",href:"#lab",h:HUE.ai,ic:icon("ai",22),t:"مختبر الذكاء",p:"اصطد كوكبًا مختبئًا في ضوء نجم، ودرّب نموذجًا يصنّف المجرات بنفسك.",go:"ادخل المختبر"},
    {k:"build",href:"#build",h:HUE.exploration,ic:icon("exploration",22),t:"ورشة الصواريخ",p:"ركّب صاروخك قطعة قطعة، ثم أطلقه وتابع رحلته إلى الفضاء أو المدار أو القمر.",go:"افتح الورشة"},
    {k:"enc",href:"#topic-"+SECTIONS[0].id,h:HUE.astrophysics,ic:BOOK,t:"الموسوعة",p:`${arN(KN,W_INFO)} موثقة بمصادرها في ${SECTIONS.length} مواضيع، ولكل موضوع مقالة بمستويين للقراءة.`,go:"اختر موضوعًا"}
  ];
  const n=steps.filter(x=>t[x.k]).length,all=n===steps.length;
  const sec=el("section","sec start-sec");sec.id="start-sec";sec.setAttribute("aria-labelledby","start-h");
  sec.innerHTML=`<div class="wrap"><div class="start${all?" all":""}">
    <div class="start-top"><div><span class="kick">${all?"أحسنت":"أول مرة هنا؟"}</span><h2 id="start-h">${all?"أكملت الجولة!":"ابدأ من هنا"}</h2>
    <p class="sec-sub">${all?"جرّبت أقوى ثلاثة أشياء في أفق. الآن تعرف طريقك، ولن تظهر لك هذه البطاقة مرة أخرى.":"ثلاث محطات تعرّفك بأقوى ما في أفق. ابدأ بأيها شئت، وسنعلّم لك ما جرّبته."}</p></div>
    <button class="start-x" type="button" aria-label="إخفاء جولة البداية"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13"/></svg></button></div>
    <ol class="start-steps">${steps.map((x,i)=>`<li><a class="start-step${t[x.k]?" done":""}" href="${x.href}" data-k="${x.k}" style="--h:${x.h}">
      <span class="n" aria-hidden="true">${t[x.k]?CHECK:i+1}</span><span class="ic">${x.ic}</span>
      <span class="tx"><b>${x.t}</b><small>${x.p}</small><span class="go">${t[x.k]?"جرّبتها":x.go+" ←"}</span>${t[x.k]?'<span class="sr-only"> (جرّبتها)</span>':""}</span></a></li>`).join("")}</ol>
    <div class="progress-line"><span>جرّبت ${n} من ${steps.length}</span><div class="bar"><i style="width:${n/steps.length*100}%"></i></div></div>
  </div></div>`;
  ph.replaceWith(sec);
  const enc=sec.querySelector('[data-k="enc"]');
  enc.onclick=ev=>{if(ev.button!==0||ev.metaKey||ev.ctrlKey)return;ev.preventDefault();
    const g=$("#topics");if(!g)return;const sm=!matchMedia("(prefers-reduced-motion: reduce)").matches;
    g.closest("section").scrollIntoView({behavior:sm?"smooth":"auto",block:"start"});
    const a=g.querySelector("a");if(a)a.focus({preventScroll:true});};
  sec.querySelector(".start-x").onclick=()=>{store.set(TOUR_OFF,true);const f=$("#q");sec.remove();toast("أخفينا جولة البداية.");if(f)f.focus({preventScroll:true});};
  if(all)store.set(TOUR_OFF,true);
}
function renderHome(){''')
rep('''  const h=location.hash.slice(1);
  let kept=false;
''','''  const h=location.hash.slice(1);
  let kept=false;
  if(h==="lab")tourMark("lab");else if(h==="build")tourMark("build");else if(h.startsWith("topic-")||h==="glossary")tourMark("enc");
''')
rep('.sr-only{','''.start-sec{padding-bottom:0}
.start{position:relative;border-radius:20px;padding:22px;border:1px solid var(--line);background:radial-gradient(80% 140% at 100% 0%,rgba(140,80,255,.13),transparent 62%),radial-gradient(60% 120% at 0% 100%,rgba(40,190,255,.08),transparent 60%),var(--surface)}
.start-top{display:flex;align-items:flex-start;gap:12px}
.start-top>div{flex:1;min-width:0}
.start-x{flex:none;width:38px;height:38px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--muted);display:grid;place-items:center}
.start-x:hover{color:var(--fg);border-color:var(--accent)}
.start-steps{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.start-steps li{min-width:0}
.start-step{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:10px;height:100%;padding:16px;border-radius:16px;border:1px solid var(--line);background:var(--surface-2);color:var(--fg);text-decoration:none;transition:transform .15s,border-color .15s,box-shadow .15s}
.start-step:hover{transform:translateY(-2px);border-color:var(--accent);box-shadow:0 10px 26px rgba(106,47,245,.14)}
.start-step .n{position:absolute;top:12px;inset-inline-end:12px;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-size:.82rem;font-weight:700;background:var(--surface);border:1px solid var(--line);color:var(--muted)}
.start-step .ic{width:44px;height:44px;border-radius:13px}
.start-step .tx{display:block;min-width:0}
.start-step b{display:block;font-family:var(--f-display);font-size:1.08rem}
.start-step small{display:block;color:var(--muted);font-size:.9rem;line-height:1.75;margin-top:2px}
.start-step .go{display:block;margin-top:8px;color:var(--accent);font-weight:600;font-size:.92rem}
.start-step.done{border-color:var(--ok);background:var(--surface)}
.start-step.done .n{background:var(--ok);border-color:var(--ok);color:var(--surface)}
.start-step.done .go{color:var(--ok)}
.start .progress-line{margin-top:14px}
@media (max-width:820px){.start{padding:18px}.start-steps{grid-template-columns:minmax(0,1fr);gap:10px}.start-step{flex-direction:row;gap:12px;padding:14px}.start-step .ic{width:40px;height:40px}.start-step .n{top:6px;inset-inline-end:auto;inset-inline-start:6px;width:21px;height:21px;font-size:.72rem}}
.sr-only{''')

# ---------- version 1.1 ----------
rep('<small class="ver">الإصدار 1.0 · آخر تحديث 19 نوفمبر 2026</small>','<small class="ver">الإصدار 1.1 · آخر تحديث 19 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch22 ok')
