# v1.7: «سجل التحديثات» (changelog) page.
#  - #changelog: every release from 1.0 to now, newest first, with its fixes/updates, written from the git history
#    for visitors (no technical detail), plus «قبل الإصدار 1.0» (16–19 Nov build-up) and how versions are numbered
#  - the footer version line links to it (its text stays exactly «الإصدار X · آخر تحديث …» so version bumps still match)
#  - CHANGELOG is data the scheduled tasks extend: every x.y.z bump adds one line to the newest release's fixes;
#    tools/tests/data.js checks that the footer version and the newest changelog entry match
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- styles ----------
rep('.ver{display:block;margin-top:6px;opacity:.85}','''.ver{display:block;margin-top:6px;opacity:.85}
.ver-link{display:block;width:fit-content;margin:6px auto 0;color:inherit;text-decoration:none;border-radius:8px}
.ver-link .ver{margin-top:0;text-decoration:underline dotted;text-underline-offset:4px}
.ver-link:hover .ver{opacity:1;color:var(--sky-accent)}
/* ===== changelog ===== */
.cl{padding-block:8px 64px}
.cl-sum{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 26px}
.cl-sum div{flex:1 1 150px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.cl-sum b{display:block;font-family:var(--f-display);font-size:1.45rem;line-height:1.4;color:var(--accent)}
.cl-sum span{font-size:.85rem;color:var(--muted)}
.cl-list{list-style:none;margin:0;padding:0;position:relative}
.cl-list::before{content:"";position:absolute;top:10px;bottom:10px;inset-inline-start:11px;width:2px;background:var(--line)}
.cl-item{position:relative;padding-inline-start:38px;margin-bottom:18px}
.cl-dot{position:absolute;inset-inline-start:4px;top:22px;width:16px;height:16px;border-radius:50%;background:var(--surface);border:3px solid var(--accent)}
.cl-item.latest .cl-dot{background:var(--accent);box-shadow:0 0 0 5px var(--accent-soft)}
.cl-card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:16px 18px}
.cl-top{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}
.cl-v{font-family:var(--f-mono);font-weight:500;font-size:.95rem;padding:1px 12px;border-radius:999px;background:var(--grad);color:#fff;direction:ltr}
.cl-new{font-size:.75rem;font-weight:700;padding:2px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.cl-top time{font-size:.85rem;color:var(--muted)}
.cl-card h2{margin:6px 0 8px;font-family:var(--f-display);font-size:1.2rem;line-height:1.5}
.cl-card ul{margin:0;padding-inline-start:20px;display:flex;flex-direction:column;gap:4px}
.cl-card li{line-height:1.8}
.cl-fix{margin-top:12px;padding-top:12px;border-top:1px dashed var(--line)}
.cl-fix h3{margin:0 0 8px;font-size:.85rem;font-weight:700;color:var(--muted)}
.cl-fix ul{list-style:none;padding:0;gap:8px}
.cl-fix li{display:grid;grid-template-columns:auto 1fr;gap:0 10px;font-size:.93rem;line-height:1.7}
.cl-fix b{font-family:var(--f-mono);font-weight:500;font-size:.85rem;color:var(--accent);direction:ltr;padding-top:2px}
.cl-fix small{grid-column:2;font-size:.78rem;color:var(--muted)}
.cl-pre{margin-top:6px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:14px 18px}
.cl-pre summary{cursor:pointer;font-family:var(--f-display);font-weight:700}
.cl-pre ul{margin:12px 0 0;padding-inline-start:20px;display:flex;flex-direction:column;gap:6px}
.cl-pre li{line-height:1.8}
.cl-pre li b{color:var(--accent)}
.cl-how{margin-top:18px}
.cl-how h2{margin:0 0 8px;font-family:var(--f-display);font-size:1.15rem}
.cl-how ul{margin:8px 0;padding-inline-start:20px}''')

# ---------- footer: the version line opens the changelog ----------
rep('    <small class="ver">الإصدار 1.6 · آخر تحديث 22 نوفمبر 2026</small>',
    '    <a class="ver-link" href="#changelog" title="سجل التحديثات"><small class="ver">الإصدار 1.7 · آخر تحديث 22 نوفمبر 2026</small><span class="sr-only"> (سجل التحديثات)</span></a>')

# ---------- data + page ----------
rep('function renderAbout(){','''/* سجل التحديثات: الأحدث أولًا. v رقم الإصدار، date يومه بتوقيت السعودية (YYYY-MM-DD)، title عنوان قصير، items نقاط قصيرة للزائر.
   كل إصدار برقم ثانٍ جديد (مثل 1.8) عنصر جديد في أول القائمة. والتصليحات والتحديثات (مثل 1.7.1) سطر في fixes داخل عنصر رقمها
   الثاني، الأحدث أولًا: {v:"1.7.1",date:"YYYY-MM-DD",text:"سطر واحد بالفصحى البسيطة يقول ما تغيّر للزائر"}.
   أحدث رقم هنا يجب أن يطابق رقم الإصدار في أسفل الموقع، ويتحقق من ذلك اختبار tools/tests/data.js. */
const CHANGELOG=[
 {v:"1.7",date:"2026-11-22",title:"سجل التحديثات",items:[
  "صفحة جديدة تعرض كل إصدارات «أفق الذكاء» وما تغيّر في كل منها، من الأحدث إلى الأقدم.",
  "رقم الإصدار في أسفل الموقع صار رابطًا إلى هذه الصفحة."]},
 {v:"1.6",date:"2026-11-22",title:"شارك، واعمل دون إنترنت، وأضف إلى تقويمك",items:[
  "زر «شارك» في كل معلومة يصنع منها بطاقة صورة جاهزة للإرسال، مع رابط يفتح المعلومة نفسها.",
  "يعمل الموقع دون إنترنت بعد أول زيارة، ويمكن تثبيته على شاشة الجوال الرئيسية.",
  "زر «أضف إلى تقويمك» لأحداث السماء ولكسوف 2027، مع تذكير قبل الموعد."]},
 {v:"1.5",date:"2026-11-21",title:"الإعدادات",items:[
  "زر الإعدادات في الشريط العلوي، وفيه حجم الخط بأربع درجات.",
  "وضع الرصد الأحمر: يحوّل الشاشة إلى أحمر خافت يحافظ على رؤية عينيك للنجوم في الظلام.",
  "مستوى الشرح ومدينتك في مكان واحد، وإعادة جولة «ابدأ من هنا»، ومسح بياناتك من الجهاز."]},
 {v:"1.4",date:"2026-11-21",title:"حماية المحتوى",items:[
  "حماية لحقوق محتوى الموسوعة، وتنبيه يظهر لمن يفتح نسخة منقولة من الموقع على عنوان آخر."],
  fixes:[
  {v:"1.4.2",date:"2026-11-21",text:"نافذة «اسأل أفق» صارت تأخذ الشاشة كلها في الجوال، فلا تظهر الصفحة خلفها ولا تتحرك أثناء الكتابة."},
  {v:"1.4.1",date:"2026-11-21",text:"محاولة أولى لتثبيت نافذة «اسأل أفق» فوق لوحة المفاتيح في الآيفون."}]},
 {v:"1.3",date:"2026-11-20",title:"اليوم في تاريخ الفضاء",items:[
  "بطاقة في الرئيسية تعرض حدثًا من تاريخ الفضاء وقع في مثل هذا اليوم، مع 86 حدثًا يمكن التنقل بينها، ولكل حدث مصدره.",
  "فحص تلقائي كل أسبوع لروابط مصادر الموسوعة، وتحديث أسبوعي لأحداث «سماء الشهر»."],
  fixes:[
  {v:"1.3.1",date:"2026-11-20",text:"إخفاء بطاقة «ابدأ من هنا» لم يعد يفتح لوحة المفاتيح في الآيفون."}]},
 {v:"1.2",date:"2026-11-20",title:"حدث الأسبوع",items:[
  "شريط في الرئيسية لأبرز حدث فلكي أو فضائي في الأسبوع، مع عدّ تنازلي بالأيام، ويتجدد كل أسبوع.",
  "أول حدث فيه: دخول مركبة بيبي كولومبو مدار عطارد."]},
 {v:"1.1",date:"2026-11-19",title:"ابدأ من هنا",items:[
  "بطاقة «ابدأ من هنا» لأول زيارة، تقترح ثلاث محطات وتتذكر ما جرّبته منها.",
  "سطر في «اسأل أفق» يوضح أنه يجيب من 301 معلومة موثقة و99 مصطلحًا، ولا يخترع إجابات."],
  fixes:[
  {v:"1.1.3",date:"2026-11-20",text:"تحديث أسبوعي: مسبار فوييجر 1 بلغ مسافة يوم ضوئي كامل من الأرض في 18 نوفمبر 2026."},
  {v:"1.1.2",date:"2026-11-20",text:"شعار جديد: كوكب يطل منه أفق، وتشرق فوقه شمس."},
  {v:"1.1.1",date:"2026-11-20",text:"صورة معاينة تظهر عند مشاركة رابط الموقع، وأيقونة جديدة للموقع."}]},
 {v:"1.0",date:"2026-11-19",title:"الإطلاق الرسمي الأول",items:[
  "موسوعة من 301 معلومة موثقة بمصادرها في ثمانية مواضيع، و99 مصطلحًا.",
  "«اسأل أفق»: مساعد يجيب من معلومات الموسوعة، ومع كل جواب مصدره.",
  "مختبر الذكاء الاصطناعي بثلاث تجارب: صيد الكواكب، وتدريب نموذج على تصنيف المجرات، ونموذج لغوي صغير.",
  "أدوات «جرّب بنفسك»: سماء الليلة، والمجموعة الشمسية الآن، وتشريح الصاروخ، وورشة الصواريخ.",
  "صفحة «السعودية والفضاء»، واختبار من 90 سؤالًا بثلاثة مستويات وشهادة إنجاز."]}
];
const BUILD_LOG=[
 ["2026-11-16","أول نسخة عامة من الموسوعة، ثم 99 معلومة جديدة موثقة بمصادرها، وألوان أكثر حيوية."],
 ["2026-11-17","قسم «الذكاء الاصطناعي في الفلك» ومختبر صيد الكواكب، وتجربة تدريب نموذج على المجرات، والنموذج اللغوي الصغير، وصفحتا «تشريح الصاروخ» و«سماء الليلة»، وتوضيح حقوق الفريق وما ساعد فيه Claude."],
 ["2026-11-17","نمو الموسوعة إلى 301 معلومة بعد مراجعة دقتها، و«المجموعة الشمسية الآن»، و99 مصطلحًا، وصفحة «السعودية والفضاء»، واختبار من 90 سؤالًا مع لعبة التوصيل."],
 ["2026-11-18","«ورشة الصواريخ» لتركيب صاروخك وإطلاقه، ومراجعة شاملة لكل الصفحات، وانتقال الموقع إلى عنوانه ufuq-ai.github.io."],
 ["2026-11-19","الإصدار 1.0."]
];
function renderChangelog(){
  setNav("");
  const day=v=>{const [y,m,d]=v.split("-").map(Number);return dateText(new Date(y,m-1,d));};
  const word=(n,w)=>n===1?w[0]:n===2?w[1]:(n%100>=3&&n%100<=10?w[2]:w[3]);
  const nFix=CHANGELOG.reduce((n,r)=>n+(r.fixes||[]).length,0);
  view.innerHTML=`
  <section class="page-head"><div class="wrap"><h1>سجل التحديثات</h1><p class="muted">كل ما أضفناه إلى «أفق الذكاء» وما أصلحناه، من الأحدث إلى الأقدم. ويتحدث الموقع تلقائيًا كل أسبوع.</p></div></section>
  <section class="wrap narrow cl">
    <div class="cl-sum">
      <div><b>${CHANGELOG.length}</b><span>${word(CHANGELOG.length,["إصدار بميزة جديدة","إصداران بميزات جديدة","إصدارات بميزات جديدة","إصدارًا بميزات جديدة"])}</span></div>
      <div><b>${nFix}</b><span>${word(nFix,["تحديث أو إصلاح","تحديثان وإصلاحات","تحديثات وإصلاحات","تحديثًا وإصلاحًا"])}</span></div>
      <div><b>${day(CHANGELOG[CHANGELOG.length-1].date)}</b><span>تاريخ أول إصدار رسمي</span></div>
    </div>
    <ol class="cl-list" id="cl-list"></ol>
    <details class="cl-pre"><summary>قبل الإصدار 1.0: بناء الموقع (16 – 19 نوفمبر 2026)</summary><ul id="cl-pre"></ul></details>
    <div class="card cl-how"><h2>كيف نرقّم الإصدارات؟</h2>
      <p>لكل إصدار رقم من ثلاثة أجزاء، مثل 1.6.1:</p>
      <ul><li><b>الجزء الأول</b>: تغيير كبير في الموقع كله، مثل إعادة بنائه.</li><li><b>الجزء الثاني</b>: ميزة أو صفحة جديدة.</li><li><b>الجزء الثالث</b>: إصلاح صغير أو تحديث للمعلومات.</li></ul>
      <p class="muted">وحين يزيد جزء يعود ما بعده إلى الصفر، ولا نكتب الصفر: بعد 1.4.2 جاء 1.5. والأرقام ليست كسورًا عشرية، فبعد 1.9 يأتي 1.10.</p>
    </div>
  </section>`;
  const ol=$("#cl-list");
  CHANGELOG.forEach((r,i)=>{
    const li=el("li","cl-item"+(i===0?" latest":""));li.append(el("span","cl-dot"));
    const c=el("div","cl-card"),top=el("div","cl-top"),t=el("time",null,day(r.date));t.dateTime=r.date;
    top.append(el("span","cl-v",r.v));if(i===0)top.append(el("span","cl-new","الأحدث"));top.append(t);
    const ul=el("ul");r.items.forEach(x=>ul.append(el("li",null,x)));
    c.append(top,el("h2",null,r.title),ul);
    if(r.fixes&&r.fixes.length){
      const f=el("div","cl-fix"),fu=el("ul");f.append(el("h3",null,"تحديثات وإصلاحات"));
      r.fixes.forEach(x=>{const l=el("li");l.append(el("b",null,x.v),el("span",null,x.text),el("small",null,day(x.date)));fu.append(l);});
      f.append(fu);c.append(f);
    }
    li.append(c);ol.append(li);
  });
  const pre=$("#cl-pre");BUILD_LOG.forEach(([d,x])=>{const l=el("li");l.append(el("b",null,day(d)+": "),x);pre.append(l);});
}
function renderAbout(){''')

# ---------- route ----------
rep('  else if(h==="panel") renderPanel();','  else if(h==="panel") renderPanel();\n  else if(h==="changelog") renderChangelog();')
open(P,'w',encoding='utf-8').write(s);print('patch35 ok')
