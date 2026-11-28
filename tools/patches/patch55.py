# 1.2: صفحة «طريقك إلى الفضاء» (#path)، وبطاقة عريضة تدل عليها في الرئيسية.
#  الدافع: أكثر سؤال تكرر في 60 سؤالًا حقيقيًا من Quora العربي (5 أسئلة عن كيف تصبح رائد فضاء أو تدرس الفلك).
#  وزوار الموقع من العالم العربي كله (عدّاد الزوار: السعودية 35%، مصر 24%، العراق 13%، فلسطين 11%)، فالصفحة لكل العرب.
#  كل جملة فيها مأخوذة من نص معلومة موثقة في الموسوعة، والمعلومة مذكورة بجانبها (العمود الأخير)، ومعها مصدرها:
#  رواد عرب سبقوك (K255، K259، K311، K260، K191)، وشروط الوكالات (K309، K310، K311، K52)، وما تدرسه (K309، K310)،
#  وما تبدأ به الآن من أي مكان (K177، K298، K291، K168). data.js يتحقق أن كلها موجودة، و flows.js يجرّب الصفحة.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''.my-done p{margin:0}''','''.my-done p{margin:0}
/* طريقك إلى الفضاء */
.path h1{font-size:clamp(1.6rem,5vw,2.2rem)}
.pt-sec{margin-top:30px}
.pt-sec h2{font-size:clamp(1.2rem,3.6vw,1.45rem);margin-bottom:4px}
.pt-sec>p{margin:0 0 12px}
.pt-src{font-size:.84rem;color:var(--muted)}
.pt-src a{color:inherit}
.pt-tl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.pt-tl li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 14px;align-items:start;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:14px 16px}
.pt-yr{grid-row:span 3;font-family:var(--f-display);font-weight:700;font-size:1.05rem;color:var(--accent);background:var(--accent-soft);border-radius:12px;padding:6px 10px;min-width:64px;text-align:center}
.pt-tl b{font-family:var(--f-display);font-size:1.05rem}
.pt-tl p{margin:0;line-height:1.8}
.pt-row{display:flex;flex-wrap:wrap;align-items:center;gap:4px 14px;min-height:44px}
.pt-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.pt-card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 18px;display:flex;flex-direction:column;gap:6px}
.pt-card h3{font-size:1.08rem}
.pt-card p{margin:0;line-height:1.8;flex:1}
.pt-note{background:var(--accent-soft);border-radius:16px;padding:14px 18px;margin:0 0 12px;line-height:1.85}
.pt-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px;padding:0;list-style:none}
.pt-chips li{border:1.5px solid var(--line);background:var(--surface-2);border-radius:999px;padding:8px 16px;font-weight:600}
.pt-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.pt-links a{min-height:44px;display:inline-flex;align-items:center}
.pt-tease{margin-top:14px}
@media (max-width:640px){.pt-grid{grid-template-columns:minmax(0,1fr)}}''')

rep('''function renderMyths(){''','''/* «طريقك إلى الفضاء»: كل سطر مأخوذ من نص المعلومة المذكورة بجانبه */
const PATH_ARABS=[
 ["1985","سلطان بن سلمان","أول رائد فضاء عربي ومسلم، انطلق على متن المكوك الأمريكي ديسكفري.","K255"],
 ["2019","هزاع المنصوري","أول رائد فضاء إماراتي، انطلق إلى محطة الفضاء الدولية.","K259"],
 ["2021","نورا المطروشي ومحمد الملا","الفوج الثاني من رواد الإمارات، اختيرا من بين 4,305 متقدمين.","K311"],
 ["2023","سلطان النيادي","أول رائد فضاء إماراتي يسير في الفضاء.","K260"],
 ["2023","ريانة برناوي وعلي القرني","انطلقا إلى محطة الفضاء الدولية في رحلة «أكسيوم 2».","K191"],
];
const PATH_AGENCIES=[
 ["ناسا","تختار من المواطنين الأمريكيين، بماجستير في مجال علمي أو تقني أو بشهادة طب، وثلاث سنوات خبرة بعد الشهادة.","K309"],
 ["وكالة الفضاء الأوروبية","تختار من مواطني دولها الأعضاء، بماجستير في العلوم الطبيعية أو الطب أو الهندسة أو الرياضيات والحاسب، وثلاث سنوات خبرة، وعمر لا يتجاوز 50 عامًا.","K310"],
 ["الإمارات","برنامج لتأهيل الكوادر الإماراتية منذ 2017، اختار فوجه الأول من بين 4,000 متقدم.","K311"],
 ["السعودية","أرسلت وكالة الفضاء السعودية ريانة برناوي وعلي القرني إلى محطة الفضاء الدولية في مايو 2023.","K52"],
];
const PATH_NOW=[
 ["صنّف مجرات حقيقية","في مشروع Galaxy Zoo يصنّف عامة الناس صور المجرات عبر الإنترنت، وفيه لاحظت معلمة هولندية سحابة غريبة صارت تُعرف باسمها.","K177"],
 ["ابحث عن كويكبات في صور هابل","تصنيفات متطوعين على منصة Zooniverse درّبت نموذجًا وجد 1,031 أثرًا يُرجَّح أنها كويكبات لم تكن معروفة.","K298"],
 ["ساعد مرصد موجات الجاذبية","في مشروع Gravity Spy يصنّف متطوعون صور الضجيج في بيانات مرصد LIGO، فتتعلم منهم الخوارزميات.","K291"],
 ["ارصد سماءك","التلوث الضوئي حرم أكثر من ثلث البشر من رؤية درب التبانة، فكلما ابتعدت عن أضواء المدن ظهرت لك نجوم أكثر.","K168"],
];
function ptSrc(e){const d=el("span","pt-src");if(e.url){const a=el("a",null,"المصدر: "+e.src);a.href=e.url;a.target="_blank";a.rel="noopener";d.append(a);}else d.textContent="المصدر: "+e.src;return d;}
function ptRead(e,t){const b=el("button","link-btn",t||"اقرأ المعلومة ←");b.type="button";b.onclick=()=>goTo(e);return b;}
function renderPath(){
  setNav("path");
  view.replaceChildren();
  const w=el("section","wrap narrow path");
  w.append(el("span","kick","صفحة خاصة"),el("h1",null,"طريقك إلى الفضاء"),
    el("p","muted","كيف يصبح الإنسان رائد فضاء؟ وماذا تستطيع أن تفعل من الآن، من أي بلد كنت؟ كل ما في هذه الصفحة من معلومات الموسوعة الموثقة، ومع كل معلومة مصدرها."));
  const sec=(t,sub)=>{const s=el("section","pt-sec");s.append(el("h2",null,t));if(sub)s.append(el("p","muted",sub));w.append(s);return s;};
  /* رواد عرب سبقوك */
  const s1=sec("رواد عرب سبقوك"),tl=el("ol","pt-tl");
  PATH_ARABS.forEach(([y,n,t,id])=>{const e=KB_BY_ID[id],li=el("li"),row=el("div","pt-row");row.append(ptSrc(e),ptRead(e));li.append(el("span","pt-yr",y),el("b",null,n),el("p",null,t),row);tl.append(li);});
  s1.append(tl);
  /* ماذا تشترط وكالات الفضاء؟ */
  const s2=sec("ماذا تشترط وكالات الفضاء؟","كل وكالة تختار روادها من مواطنيها، وتعلن شروطها حين تفتح باب التقديم.");
  s2.append(el("p","pt-note","ما يجمع ناسا ووكالة الفضاء الأوروبية: ماجستير في العلوم أو الهندسة أو الطب أو الرياضيات والحاسب، وثلاث سنوات خبرة بعد الشهادة، وفحص طبي. ولا تشترط وكالة الفضاء الأوروبية أن تكون طيارًا أو عسكريًا."));
  const g=el("div","pt-grid");
  PATH_AGENCIES.forEach(([n,t,id])=>{const e=KB_BY_ID[id],c=el("div","pt-card"),row=el("div","pt-row");row.append(ptSrc(e),ptRead(e));c.append(el("h3",null,n),el("p",null,t),row);g.append(c);});
  s2.append(g);
  /* ماذا تدرس؟ */
  const s3=sec("ماذا تدرس؟","هذه المجالات التي تقبلها ناسا ووكالة الفضاء الأوروبية لرواد الفضاء:"),ch=el("ul","pt-chips");
  ["الهندسة","العلوم الطبيعية","الطب","الرياضيات والحاسب"].forEach(t=>ch.append(el("li",null,t)));
  const r3=el("div","pt-row");r3.append(ptRead(KB_BY_ID.K309,"شروط ناسا ←"),ptRead(KB_BY_ID.K310,"شروط وكالة الفضاء الأوروبية ←"));
  s3.append(ch,el("p",null,"ومن آخر من اختارتهم ناسا: طيارو اختبار ومهندسون وأطباء ومختص في الجيولوجيا."),r3);
  /* ابدأ الآن، من أي مكان */
  const s4=sec("ابدأ الآن، من أي مكان","لست مضطرًا لانتظار الجامعة: هذه مشاريع علمية حقيقية يشارك فيها عامة الناس، وسماء تنتظرك.");
  const g4=el("div","pt-grid");
  PATH_NOW.forEach(([n,t,id])=>{const e=KB_BY_ID[id],c=el("div","pt-card"),row=el("div","pt-row");row.append(ptSrc(e),ptRead(e));c.append(el("h3",null,n),el("p",null,t),row);g4.append(c);});
  const lk=el("div","pt-links");
  [["#sky","سماء الليلة"],["#lab","مختبر الذكاء"],["#build","ورشة الصواريخ"],["#myths","حقيقة أم خرافة؟"]].forEach(([h,t])=>{const a=el("a","btn btn-soft",t);a.href=h;lk.append(a);});
  s4.append(g4,el("p","muted","وفي أفق نفسه تجرّب بيدك:"),lk);
  w.append(el("p","pt-src","تتغير شروط الوكالات مع كل دفعة جديدة، فارجع إلى موقعها الرسمي حين تفتح باب التقديم."));
  view.append(w);
}
function renderMyths(){''')

rep('''  else if(h==="myths") renderMyths();''','''  else if(h==="myths") renderMyths();
  else if(h==="path") renderPath();''')

# بطاقة عريضة في الرئيسية بعد «ما الذي يميز أفق؟»
rep('''      <a class="feat" href="#rocket"><span class="ic" style="--h:${HUE.exploration}">${icon("exploration",24)}</span><h3>تشريح الصاروخ</h3>''','''      <a class="feat" href="#rocket"><span class="ic" style="--h:${HUE.exploration}">${icon("exploration",24)}</span><h3>تشريح الصاروخ</h3>''')
i=s.index('''      <a class="feat" href="#rocket">''');j=s.index('''    </div>\n  </div></section>''',i)
s=s[:j]+'''    </div>
    <a class="feat pt-tease" href="#path"><span class="ic" style="--h:${HUE.exploration}">${icon("exploration",24)}</span><h3>جديد: طريقك إلى الفضاء</h3><p>كيف يصبح الإنسان رائد فضاء؟ وماذا تستطيع أن تفعل من الآن، من أي بلد كنت؟</p><span class="link-btn">ابدأ الطريق ←</span></a>
  </div></section>'''+s[j+len('''    </div>\n  </div></section>'''):]
assert s.count('href="#path"')==1
open(P,'w',encoding='utf-8').write(s);print('patch55 ok')
