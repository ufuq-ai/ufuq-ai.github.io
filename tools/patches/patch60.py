# 1.3: صفحة «نجم يوم ميلادك» (#birthstar)، وبطاقة تدل عليها في «جرّب بنفسك».
#  تكتب تاريخ ميلادك، فتقول الصفحة أي نجم خرج نوره الذي يصلنا اليوم قرب يوم ميلادك (المسافة بالسنوات الضوئية = السنوات التي قطعها نوره)،
#  ومتى يصير نجم آخر «نجم يوم ميلادك»، وتعرض «مسطرة الضوء»: 28 نجمًا حتى 100 سنة ضوئية، و4 نجوم أبعد.
#  المسافات من اختلاف المنظر (parallax) في قاعدة SIMBAD، وقياساته من مهمتي هيباركوس وغايا التابعتين لوكالة الفضاء الأوروبية.
#  الجدول BS_STARS يُكتب من tools/research/notes/birth_star_1_3.json (فيه القيم الحرفية ومرجع كل قياس). ولم يُدرج نجم هامش خطأ مسافته فوق 10%.
#  اللون تقريبي من الصنف الطيفي، والحجم من السطوع (القدر V). وتنبيه «يُرى من الجنوب فقط» حساب هندسي من ميل النجم.
#  تاريخ الميلاد لا يُرسل ولا يُحفظ: يُحسب في المتصفح فقط.
import os,json
D=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(D,'..','src','ai-horizon.html')
N=os.path.join(D,'..','research','notes','birth_star_1_3.json')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)
def cls(sp):
    if sp.startswith('k') and 'h' in sp: return sp[sp.index('h')+1]
    return sp[0]
rows=[]
for x in json.load(open(N,encoding='utf-8'))['stars']:
    south=1 if x['dec']<-55 else 2 if x['dec']<-50 else 0
    V=float(x['V']) if x['V'] else 2.2  # ميزار وحده بلا قدر في الجدول، وليس في القائمة
    rows.append([x['ar'],x['iau'],x['constellation'],x['d_ly'],x['d_err_ly'],V,cls(x['sp_type']),x['simbad_id'],south])
assert len(rows)==32 and all(r[6] in 'OBAFGKM' for r in rows),[r[6] for r in rows]
TABLE='const BS_STARS=[\n'+',\n'.join(' '+json.dumps(r,ensure_ascii=False) for r in rows)+'];'

rep('''.pt-tease{margin-top:14px}
@media (max-width:640px){.pt-grid{grid-template-columns:minmax(0,1fr)}}''','''.pt-tease{margin-top:14px}
@media (max-width:640px){.pt-grid{grid-template-columns:minmax(0,1fr)}}
/* نجم يوم ميلادك */
.tools .bs-cta{grid-column:1/-1}
.bs-priv,.bs-sub{color:var(--sky-muted);font-size:.9rem;line-height:1.8}
.bs-h{font-size:clamp(1.2rem,3.6vw,1.45rem)}
.bs-h3{font-size:1.05rem;margin-top:12px}
.bs-dot{flex:none;display:inline-block;width:var(--z,10px);height:var(--z,10px);border-radius:50%;background:var(--c);box-shadow:0 0 0 1px rgba(255,255,255,.25),0 0 12px var(--c)}
.bs-hint{color:var(--sky-muted)}
.bs-err{color:#ffb4a8}
.bs-res{display:flex;flex-direction:column;gap:12px;border-top:1px solid var(--sky-line);padding-top:16px}
.bs-hd{display:flex;align-items:center;gap:18px}
.bs-hd .bs-dot{width:44px;height:44px;margin-inline:6px;box-shadow:0 0 0 1px rgba(255,255,255,.3),0 0 30px 8px var(--c)}
.bs-hd h2{font-size:clamp(1.6rem,6vw,2.2rem);line-height:1.35}
.bs-iau{display:block;font-size:.85rem;color:var(--sky-muted);font-family:var(--f-body)}
.bs-say{font-size:1.08rem;line-height:1.9}
.bs-facts{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.bs-facts li{border:1px solid var(--sky-line);background:rgba(255,255,255,.06);border-radius:999px;padding:4px 12px;font-size:.88rem;line-height:1.7}
.bs-note,.bs-src{font-size:.85rem;color:var(--sky-muted);line-height:1.8}
.bs-src a{color:inherit}
.bs-next{background:rgba(255,215,150,.1);border:1px solid rgba(255,215,150,.3);border-radius:14px;padding:10px 14px;line-height:1.85}
.bs-act{display:flex;flex-wrap:wrap;gap:8px}
.bs-act .btn{min-height:44px;display:inline-flex;align-items:center}
.bs-rl{list-style:none;margin:0;padding:0}
.bs-rl li{display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:2px 12px;align-items:center;padding:8px 6px;border-bottom:1px solid var(--sky-line)}
.bs-rl li>.bs-dot{justify-self:center}
.bs-nm{min-width:0}
.bs-nm b{font-family:var(--f-display);font-weight:700}
.bs-nm .bs-iau{font-size:.78rem;line-height:1.5}
.bs-yr{text-align:end;font-variant-numeric:tabular-nums;line-height:1.5}
.bs-yr span{display:block;font-size:.9rem}
.bs-yr small{color:var(--sky-muted);font-size:.8rem}
.bs-rl li.on{background:rgba(255,215,150,.13);border-radius:12px;border-bottom-color:transparent}
.bs-rl li.bs-me{grid-template-columns:24px auto minmax(0,1fr);color:#ffd796;border-bottom:2px dashed rgba(255,215,150,.55)}
.bs-ring{justify-self:center;width:14px;height:14px;border-radius:50%;border:2px solid #ffd796}
.bs-me small{color:var(--sky-muted)}
.bs-how{display:flex;flex-direction:column;gap:12px;margin-top:8px}
.bs-how h2{font-size:clamp(1.2rem,3.6vw,1.45rem)}''')

rep('''function renderMyths(){''','''/* «نجم يوم ميلادك»: المسافات من اختلاف المنظر في قاعدة SIMBAD (قياسات هيباركوس وغايا)، والأدلة في tools/research/notes/birth_star_1_3.json
   [الاسم العربي، الاسم الدولي، الكوكبة، المسافة بالسنوات الضوئية، هامش الخطأ، القدر، الصنف الطيفي، رمزه في SIMBAD، 1 لا يُرى إلا من الجنوب و2 منخفض في الجنوب] */
'''+TABLE+'''
const BS_COL={O:"#9db4ff",B:"#aabfff",A:"#dfe7ff",F:"#fff4e0",G:"#ffe39b",K:"#ffbf73",M:"#ff9a66"};
const BS_YR=365.2425*864e5,BS_Y=["سنة","سنتين","سنوات","سنة"],BS_M=["شهر","شهرين","أشهر","شهرًا"];
function bsN(n,f){return n===1?f[0]:n===2?f[1]:n<=10?n+" "+f[2]:n+" "+f[3];}
function bsDur(y){const m=Math.round(Math.abs(y)*12),Y=Math.floor(m/12),M=m%12,p=[];if(Y)p.push(bsN(Y,BS_Y));if(M)p.push(bsN(M,BS_M));return p.join(" و");}
function bsMonth(t){try{return new Date(t).toLocaleDateString("ar-SA-u-ca-gregory-nu-latn",{month:"long",year:"numeric",timeZone:"UTC"});}catch(_){return new Date(t).toISOString().slice(0,7);}}
function bsYear(t){return new Date(t).getUTCFullYear();}
function bsDot(s){const d=el("span","bs-dot");d.style.setProperty("--c",BS_COL[s[6]]||"#fff");const z=Math.round(Math.max(7,Math.min(18,6+(5-s[5])*2)));d.style.setProperty("--z",z+"px");return d;}
function bsIau(t){const e=el("span","bs-iau",t);e.dir="ltr";e.lang="en";return e;}
function bsCta(kick,title,text){const a=el("a","lab-cta bs-cta");a.href="#birthstar";
  a.innerHTML=`<div><span class="kick">${kick}</span><h3>${title}</h3><p>${text}</p><span class="link-btn">افتح ←</span></div><svg class="mini-lc" viewBox="0 0 240 70" aria-hidden="true"><line x1="12" y1="40" x2="228" y2="40" stroke="#8d7fd0" stroke-width="1.5"/><g stroke="#8d7fd0" stroke-opacity=".6">${[40,80,120,160,200].map(x=>`<line x1="${x}" y1="34" x2="${x}" y2="46"/>`).join("")}</g><circle cx="22" cy="40" r="5" fill="#ffe39b"/><circle cx="58" cy="40" r="7" fill="#dfe7ff"/><circle cx="96" cy="40" r="4" fill="#ffbf73"/><circle cx="138" cy="40" r="6" fill="#dfe7ff"/><circle cx="138" cy="40" r="12" fill="none" stroke="#ffd796" stroke-width="1.5"/><circle cx="178" cy="40" r="5" fill="#ffbf73"/><circle cx="216" cy="40" r="4" fill="#aabfff"/></svg>`;return a;}
function renderBirth(){
  setNav("tools");
  const now=Date.now();
  view.innerHTML=`
  <section class="page-head" style="--h:38"><div class="wrap">
    <div class="crumb"><a href="#tools">جرّب</a> / نجم يوم ميلادك</div>
    <h1>نجم يوم ميلادك</h1>
    <p class="muted">الضوء أسرع شيء في الكون، ومع ذلك يحتاج سنوات ليصلنا من النجوم. فالنور الذي يصلنا الليلة من نجم يبعد 16 سنة ضوئية خرج منه قبل 16 سنة. اكتب تاريخ ميلادك لتعرف أي نجم خرج نوره الذي يصلنا اليوم قرب يوم ميلادك.</p>
  </div></section>
  <section class="wrap sk bs">
    <div class="lab-card">
      <div class="sk-ctl"><label class="field">تاريخ ميلادك<input type="date" id="bs-date" min="1900-01-01" max="${new Date(now).toISOString().slice(0,10)}"></label></div>
      <p class="bs-priv">التاريخ يبقى في جهازك: لا نرسله ولا نحفظه.</p>
      <div id="bs-out" aria-live="polite"><p class="bs-hint">اختر تاريخ ميلادك لترى نجمك.</p></div>
    </div>
    <div class="lab-card">
      <h2 class="bs-h">مسطرة الضوء</h2>
      <p class="bs-sub">كل نجم هنا يبعد عنا عددًا من السنوات الضوئية، فالنور الذي يصلنا منه اليوم خرج منه قبل هذا العدد من السنين.</p>
      <ol class="bs-rl" id="bs-rl"></ol>
      <h3 class="bs-h3">نجوم نورها أقدم من أعمارنا</h3>
      <ol class="bs-rl" id="bs-far"></ol>
    </div>
    <div class="bs-how" id="bs-how"></div>
    <p class="legend">المسافات تقريبية: لكل قياس هامش خطأ صغير يكبر كلما بعد النجم. وقياساتها من مهمتي «هيباركوس» و«غايا» التابعتين لوكالة الفضاء الأوروبية، عن قاعدة بيانات النجوم SIMBAD.</p>
  </section>`;
  const near=BS_STARS.filter(s=>s[3]<=100),far=BS_STARS.filter(s=>s[3]>100),rl=$("#bs-rl"),inp=$("#bs-date"),out=$("#bs-out");
  const row=(s,d,y)=>{const li=el("li"),nm=el("div","bs-nm"),yr=el("div","bs-yr");nm.append(el("b",null,s[0]),bsIau(s[1]));
    yr.append(el("span",null,d+" سنة ضوئية"),el("small",null,"خرج نوره "+y));li.append(bsDot(s),nm,yr);return li;};
  /* النجوم الأبعد: هامش الخطأ فيها سنوات، فالسنة تقريبية (وتُقرَّب إلى العشرات إن زاد الهامش على 5 سنوات) */
  far.forEach(s=>{const y=bsYear(now-s[3]*BS_YR);$("#bs-far").append(row(s,"نحو "+Math.round(s[3]),"نحو سنة "+(s[4]>5?Math.round(y/10)*10:y)));});
  function ruler(age,pick,bt){
    rl.replaceChildren();let me=age==null;
    const meRow=()=>{const li=el("li","bs-me");li.append(el("span","bs-ring"),el("b",null,"وُلدت هنا"),el("small",null,bsMonth(bt)));return li;};
    near.forEach(s=>{
      if(!me&&s[3]>age){me=true;rl.append(meRow());}
      const li=row(s,s[3].toFixed(1),"سنة "+bsYear(now-s[3]*BS_YR));if(pick===s)li.className="on";rl.append(li);
    });
    if(!me)rl.append(meRow());
  }
  function show(){
    out.replaceChildren();
    const v=inp.value,bt=v?Date.parse(v+"T00:00:00Z"):NaN,age=(Date.now()-bt)/BS_YR;
    if(!isFinite(age)){out.append(el("p","bs-hint","اختر تاريخ ميلادك لترى نجمك."));ruler(null);return;}
    if(age<0){out.append(el("p","bs-err","هذا التاريخ في المستقبل! اختر تاريخ ميلادك."));ruler(null);return;}
    if(age>120){out.append(el("p","bs-err","تأكد من السنة: هذا عمر يزيد على 120 سنة."));ruler(null);return;}
    let pick=near[0];near.forEach(s=>{if(Math.abs(s[3]-age)<Math.abs(pick[3]-age))pick=s;});
    const diff=age-pick[3],dur=bsDur(diff),when=!dur?"في الشهر الذي وُلدت فيه تقريبًا":(diff>0?"بعد ولادتك بنحو ":"قبل ولادتك بنحو ")+dur;
    const card=el("div","bs-res"),hd=el("div","bs-hd"),tt=el("div");
    tt.append(el("span","kick","نجم يوم ميلادك"),el("h2",null,pick[0]),bsIau(pick[1]));hd.append(bsDot(pick),tt);
    const facts=el("ul","bs-facts");
    [`يبعد ${pick[3].toFixed(1)} سنة ضوئية`,`في كوكبة ${pick[2]}`,pick[5]<=3.5?"يُرى بالعين المجردة":"خافت: يحتاج سماء مظلمة بعيدة عن أضواء المدن"]
      .concat(pick[8]===1?["لا يظهر إلا في جنوب العالم العربي، منخفضًا فوق الأفق الجنوبي"]:pick[8]===2?["يظهر منخفضًا فوق الأفق الجنوبي في أغلب العالم العربي"]:[])
      .forEach(t=>facts.append(el("li",null,t)));
    card.append(hd,el("p","bs-say",`النور الذي يصلنا اليوم من «${pick[0]}» خرج منه في ${bsMonth(Date.now()-pick[3]*BS_YR)}، ${when}.`),facts);
    if(pick[4]>=.5)card.append(el("p","bs-note",`قياس بُعد هذا النجم أقل دقة من غيره، فقد يتقدم هذا التاريخ أو يتأخر نحو ${bsN(Math.max(1,Math.round(pick[4])),BS_Y)}.`));
    /* أول نجم يصير نوره الواصل خارجًا يوم ميلادك: قد يكون نجمك نفسه إن كان أبعد قليلًا من عمرك */
    const nx=near.find(s=>s[3]>age+1/12);
    if(nx)card.append(el("p","bs-next",nx===pick?`وفي سنة ${bsYear(bt+nx[3]*BS_YR)} سيصلنا من «${nx[0]}» نفسه نور خرج منه يوم وُلدت.`:`نجمك القادم: في سنة ${bsYear(bt+nx[3]*BS_YR)} سيصلنا من «${nx[0]}» نور خرج منه يوم وُلدت.`));
    const act=el("div","bs-act");
    if(SK_STARS.some(x=>x[0]===pick[0])){const a=el("a","btn btn-ghost","متى يظهر في سمائك؟");a.href="#sky";act.append(a);}
    const sh=el("button","btn btn-accent","شارك نجمك");sh.type="button";
    sh.onclick=async()=>{const url="https://ufuq-ai.github.io/#birthstar",text=`نجم يوم ميلادي «${pick[0]}»: النور الذي يصلنا منه اليوم خرج منه ${when.replace("ولادتك","ولادتي")}. اعرف نجمك في أفق الذكاء:`;
      if(navigator.share){try{await navigator.share({title:"نجم يوم ميلادك",text,url});return;}catch(e){if(e&&e.name==="AbortError")return;}}
      try{await navigator.clipboard.writeText(text+" "+url);sh.textContent="نُسخ، الصقه حيث تشاء";}catch(_){sh.textContent="لم نستطع النسخ";}};
    act.append(sh);
    const src=el("p","bs-src"),a=el("a",null,"مصدر المسافة: قياسات وكالة الفضاء الأوروبية في قاعدة SIMBAD");
    a.href="https://simbad.cfa.harvard.edu/simbad/sim-id?Ident="+encodeURIComponent(pick[7]);a.target="_blank";a.rel="noopener";src.append(a);
    card.append(act,src);out.append(card);ruler(age,pick,bt);
  }
  inp.addEventListener("change",show);inp.addEventListener("input",show);
  ruler(null);
  /* كيف عرفنا هذا؟ من معلومتي الموسوعة K312 وK313 */
  const how=$("#bs-how"),g=el("div","pt-grid");how.append(el("h2",null,"كيف عرفنا هذا؟"));
  [["K312","كيف قاس العلماء بُعد هذه النجوم؟","مدّ إصبعك أمام عينيك، وأغمض عينًا ثم الأخرى: يبدو إصبعك كأنه يقفز أمام ما خلفه. هذا هو «اختلاف المنظر». والعلماء يرصدون النجم من جهتين متقابلتين من مدار الأرض حول الشمس بدل عينيك، فيحسبون بُعده من مقدار قفزته."],
   ["K313","هل ما زال النجم كما نراه؟","نحن نرى كل نجم كما كان حين خرج منه نوره، لا كما هو الآن. فالنجوم التي تراها الليلة صور قديمة، وبعضها خرج نوره قبل مئات السنين."]]
    .forEach(([id,h,t])=>{const e=KB_BY_ID[id],c=el("div","pt-card"),row=el("div","pt-row");row.append(ptSrc(e),ptRead(e));c.append(el("h3",null,h),el("p",null,t),row);g.append(c);});
  how.append(g);
}
function renderMyths(){''')

rep('''  else if(h==="path") renderPath();''','''  else if(h==="path") renderPath();
  else if(h==="birthstar") renderBirth();''')

rep('''أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، والمجموعة الشمسية الآن،''','''أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، ونجم يوم ميلادك، والمجموعة الشمسية الآن،''')
rep('''    <div id="t-sky" class="sk-cta"></div>
''','''    <div id="t-sky" class="sk-cta"></div>
    <div id="t-birth" class="bs-cta"></div>
''')
i=s.index('''  $("#t-sky").replaceWith(skyCta(''');j=s.index('\n',i)
s=s[:j]+'''
  $("#t-birth").replaceWith(bsCta("جديد","نجم يوم ميلادك","النور الذي يصلنا الليلة من النجوم خرج منها قبل سنين. اكتب تاريخ ميلادك، واعرف أي نجم خرج نوره قرب يوم ميلادك."));'''+s[j:]
assert s.count('href="#birthstar"')==1
open(P,'w',encoding='utf-8').write(s);print('patch60 ok')
