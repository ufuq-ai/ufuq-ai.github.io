# v1.3: «اليوم في تاريخ الفضاء» on home: 87 dated events (each tied to an encyclopedia entry or an official source),
# shows today's anniversary or the nearest one, with arrows to browse. Static list: no scheduled task needed.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)

N,B,HB,Z,J='n','b','h','z','p'
EV=[
# [month, day, year, text, related entry id, source key in HSRC ('' = the entry's own source)]
(1,1,2019,"مرّت نيو هورايزنز بالجرم أروكوث في حزام كايبر، فصار أبعد جرم يُستكشف عن قرب.","K149",""),
(1,2,1959,"انطلق المسبار السوفيتي لونا 1، أول مركبة تفلت من جاذبية الأرض وتمر قرب القمر.","",N),
(1,12,2005,"انطلقت «ديب إمباكت» التي أطلقت قذيفة على المذنب تمبل 1 لتكشف ما تحت سطحه.","",N),
(1,14,2025,"وصلت إلى الأرض الإشارة GW250114، أوضح إشارة موجات جاذبية سجّلها مرصد ليغو حتى إعلانها.","K242",""),
(1,19,2006,"انطلقت نيو هورايزنز في رحلتها الطويلة إلى بلوتو.","K148",N),
(1,31,1966,"انطلق لونا 9 الذي حقق بعد ثلاثة أيام أول هبوط سلس على القمر.","",N),
(2,8,1985,"أُطلق «عربسات 1A»، أول قمر صناعي عربي.","K256",""),
(2,17,1996,"انطلقت المركبة NEAR، التي صارت أول مركبة تدور حول كويكب ثم تهبط عليه.","",N),
(2,20,1962,"دار جون غلين حول الأرض، أول أمريكي يفعل ذلك.","",B),
(3,2,2004,"انطلقت روزيتا، أول مركبة تدور حول مذنب وتُنزل عليه مسبارًا.","",N),
(3,3,1972,"انطلق بايونير 10، أول مركبة تعبر حزام الكويكبات وتزور المشتري.","",N),
(3,7,2009,"انطلق تلسكوب كبلر الذي اكتشف آلاف الكواكب خارج المجموعة الشمسية.","K137",N),
(3,18,1965,"خرج أليكسي ليونوف من مركبته في أول سير في الفضاء.","",B),
(4,1,2026,"انطلقت أرتميس 2 بأربعة رواد في رحلة حول القمر.","K51",""),
(4,10,2026,"عاد رواد أرتميس 2 بسلام إلى الأرض بعد رحلة دامت نحو 10 أيام.","K264",""),
(4,12,1961,"صار يوري غاغارين أول إنسان في الفضاء.","",B),
(4,14,2023,"انطلقت مهمة «جوس» الأوروبية إلى أقمار المشتري الجليدية.","K268",N),
(4,16,2024,"أعلنت وكالة الفضاء الأوروبية اكتشاف Gaia BH3، أضخم ثقب أسود نجمي معروف في مجرتنا.","K239",""),
(4,19,2021,"حلّقت المروحية إنجينيويتي، فكان أول طيران آلي على كوكب آخر.","K146",""),
(4,20,2025,"مرّت المركبة لوسي بالكويكب دونالدجوهانسون.","K270",""),
(4,24,1990,"انطلق تلسكوب هابل الفضائي على متن المكوك ديسكفري.","K145",HB),
(4,28,2023,"سار سلطان النيادي في الفضاء، أول إماراتي يفعل ذلك.","K260",""),
(5,4,1989,"انطلقت ماجلان التي رسمت خريطة سطح الزهرة بالرادار.","",N),
(5,5,1961,"صار آلان شيبرد أول أمريكي في الفضاء.","",B),
(5,10,2024,"ضربت الأرض أول عاصفة مغناطيسية شديدة منذ أكثر من عقدين، فرُئي الشفق بعيدًا عن القطبين.","K285",""),
(5,12,2022,"كُشفت أول صورة للثقب الأسود في مركز مجرتنا.","K236",""),
(5,21,2023,"انطلقت ريانة برناوي وعلي القرني في رحلة «أكسيوم 2» إلى محطة الفضاء الدولية.","K191",""),
(5,28,1971,"انطلق المسبار السوفيتي مارس 3 الذي حقق أول هبوط سلس على المريخ.","",N),
(5,30,1966,"انطلق سيرفيور 1، أول مركبة أمريكية تهبط هبوطًا سلسًا على القمر.","",N),
(6,3,1965,"صار إد وايت أول أمريكي يسير في الفضاء.","",B),
(6,10,2003,"انطلقت العربة الجوالة «سبيريت» إلى المريخ.","",N),
(6,16,1963,"صارت فالنتينا تيريشكوفا أول امرأة في الفضاء.","",B),
(6,17,1985,"انطلق سلطان بن سلمان، أول رائد فضاء عربي ومسلم.","K255",""),
(6,25,2024,"عادت تشانغ إي-6 بأول عينات في التاريخ من الجانب البعيد للقمر.","K272",""),
(6,30,2026,"أُعلن بدء مرصد فيرا روبين رسميًا مسحه الكبير للسماء، ويستمر 10 سنوات.","K296",""),
(7,1,2023,"انطلق تلسكوب إقليدس ليكشف طبيعة المادة المظلمة والطاقة المظلمة.","K154",""),
(7,1,2025,"أُعلن اكتشاف المذنب 3I/ATLAS، الزائر القادم من خارج المجموعة الشمسية.","K230",""),
(7,2,1985,"انطلق المسبار الأوروبي جيوتو الذي صوّر نواة مذنب هالي عن قرب.","",N),
(7,8,2003,"انطلقت العربة الجوالة «أوبورتشونيتي» التي عملت على المريخ قرابة 15 عامًا.","",N),
(7,14,2015,"مرّت نيو هورايزنز ببلوتو، فرأينا سطحه بوضوح لأول مرة.","K148",""),
(7,14,2023,"انطلقت المهمة الهندية تشاندرايان-3 إلى القمر.","K152",N),
(7,16,1969,"انطلقت أبولو 11 نحو القمر.","K50",""),
(7,20,1969,"هبطت أبولو 11 على القمر، ومشى عليه الإنسان لأول مرة.","K50",""),
(7,23,2020,"انطلقت تيانوين-1، أول مهمة صينية إلى المريخ.","",N),
(7,28,1964,"انطلق رينجر 7 الذي أرسل آلاف الصور القريبة لسطح القمر قبل أن يصطدم به.","",N),
(7,30,2020,"انطلقت العربة الجوالة «بيرسيفيرانس» إلى المريخ.","K295",N),
(8,3,2004,"انطلقت ميسنجر، أول مركبة تدور حول عطارد.","",N),
(8,5,2011,"انطلقت المركبة جونو إلى المشتري.","",N),
(8,12,2018,"انطلق مسبار باركر الشمسي، أقرب مركبة وصلت إلى الشمس.","K147",N),
(8,17,1970,"انطلقت فينيرا 7 التي صارت أول مركبة ترسل بيانات من سطح كوكب آخر، هو الزهرة.","",N),
(8,17,2017,"رُصد حدث واحد بموجات الجاذبية والضوء معًا لأول مرة: اندماج نجمين نيوترونيين.","K249",""),
(8,20,1977,"انطلق فوييجر 2، المركبة الوحيدة التي زارت أورانوس ونبتون.","K54",N),
(8,23,2023,"هبطت تشاندرايان-3 الهندية قرب القطب الجنوبي للقمر.","K152",""),
(8,27,1962,"انطلق مارينر 2، أول مركبة تمر بكوكب آخر بنجاح، هو الزهرة.","",N),
(9,5,1977,"انطلق فوييجر 1، الذي صار أبعد جسم صنعه الإنسان.","K54",N),
(9,12,1959,"انطلق لونا 2، أول جسم من صنع الإنسان يصل إلى القمر.","",N),
(9,14,2015,"التقط مرصد ليغو موجات الجاذبية لأول مرة.","K253",""),
(9,15,2017,"أنهت كاسيني مهمتها بالغوص في الغلاف الجوي لزحل.","K151",""),
(9,25,2019,"انطلق هزاع المنصوري، أول رائد فضاء إماراتي.","K259",""),
(9,27,2007,"انطلقت المركبة داون التي دارت حول جرمين: الكويكب فيستا والكوكب القزم سيريس.","",N),
(10,4,1957,"أُطلق سبوتنيك 1، أول قمر صناعي في التاريخ.","K197",""),
(10,4,1959,"انطلق لونا 3 الذي التقط أول صور للجانب البعيد من القمر.","",N),
(10,6,1995,"أُعلن اكتشاف أول كوكب حول نجم يشبه الشمس: 51 Pegasi b.","K135",J),
(10,13,2023,"انطلقت المركبة سايكي إلى كويكب غني بالمعادن.","K269",N),
(10,14,2024,"انطلقت يوروبا كليبر إلى قمر المشتري يوروبا.","K267",""),
(10,15,1997,"انطلقت كاسيني ومعها المسبار هويغنز إلى زحل.","K151",N),
(10,16,2021,"انطلقت المركبة لوسي إلى كويكبات طروادة.","K270",N),
(10,18,1989,"انطلقت غاليليو، أول مركبة تدور حول المشتري.","",N),
(10,22,2008,"انطلقت تشاندرايان-1 الهندية التي ساهمت في كشف الماء على القمر.","",N),
(11,10,1970,"انطلق لونا 17 حاملًا «لونوخود 1»، أول عربة جوالة على جرم آخر.","",N),
(11,15,2018,"ظهر المساعد الطائر «سايمون» لأول مرة على محطة الفضاء الدولية، وهو يعمل بالذكاء الاصطناعي.","K299",""),
(11,16,2022,"انطلقت أرتميس 1 غير المأهولة في رحلة حول القمر.","K51",N),
(11,18,2013,"انطلقت المركبة مافن لدراسة الغلاف الجوي للمريخ.","",N),
(11,18,2026,"بلغ فوييجر 1 مسافة يوم ضوئي كامل عن الأرض.","K54",""),
(11,20,1998,"أُطلقت «زاريا»، أول وحدة في محطة الفضاء الدولية.","K49",Z),
(11,23,2023,"رُصدت الإشارة GW231123 من أضخم اندماج لثقبين أسودين عند الإعلان عنه.","K241",""),
(11,24,2021,"انطلقت DART، أول تجربة لتغيير مسار كويكب بالاصطدام به.","K271",N),
(11,26,2011,"انطلقت العربة الجوالة «كيوريوسيتي» إلى المريخ.","K292",N),
(11,28,1964,"انطلق مارينر 4 الذي أرسل أول صور قريبة للمريخ.","",N),
(12,3,2014,"انطلقت هايابوسا2 اليابانية التي جلبت عينات من الكويكب ريوغو.","K275",N),
(12,4,1996,"انطلق «مارس باثفايندر» حاملًا «سوجورنر»، أول عربة جوالة على المريخ.","",N),
(12,8,2025,"قطعت بيرسيفيرانس على المريخ مسارًا خططه ذكاء اصطناعي توليدي.","K183",""),
(12,21,1968,"انطلقت أبولو 8، أول رحلة بشرية تدور حول القمر.","",B),
(12,21,2015,"هبطت المرحلة الأولى من صاروخ فالكون 9 بعد إطلاق مداري، لأول مرة في التاريخ.","K190",""),
(12,24,2024,"مرّ مسبار باركر الشمسي على بُعد نحو 6.1 مليون كيلومتر من سطح الشمس.","K147",""),
(12,25,2021,"انطلق تلسكوب جيمس ويب الفضائي.","K55",""),
]
import json
rows=",\n".join("["+",".join([str(m),str(d),str(y),json.dumps(t,ensure_ascii=False),json.dumps(k),json.dumps(u)])+"]" for m,d,y,t,k,u in EV)

rep('const TOUR_K="ufuq-tour",TOUR_OFF="ufuq-tour-off";','''/* اليوم في تاريخ الفضاء: [شهر، يوم، سنة، النص، رقم المعلومة المرتبطة، مفتاح المصدر في HSRC].
   بلا مفتاح: المصدر هو مصدر المعلومة المرتبطة. التواريخ المأخوذة من HSRC يتطابق فيها اليوم بالتوقيت العالمي وبتوقيت السعودية. */
const HSRC={"n":["https://nssdc.gsfc.nasa.gov/planetary/chronology.html","ناسا: سجل المهمات القمرية والكوكبية"],"b":["https://britannica.com/science/space-exploration/Chronology-of-crewed-spaceflights","بريتانيكا: سجل الرحلات المأهولة"],"h":["https://www.nasa.gov/mission/sts-31","ناسا"],"z":["https://www.nasa.gov/history/20-years-ago-space-station-construction-begins","ناسا"],"p":["https://jpl.nasa.gov/news/exoplanets-2020-looking-back-to-the-future/","مختبر الدفع النفاث التابع لناسا"]};
const SPACE_DAYS=[
'''+rows+'''
];
function spaceDay(){
  const box=$("#hist");if(!box)return;
  const L=SPACE_DAYS.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]||a[2]-b[2]);
  const now=new Date();now.setHours(0,0,0,0);const Y=now.getFullYear(),M=now.getMonth()+1,D=now.getDate();
  const delta=e=>{let x=Math.round((new Date(Y,e[0]-1,e[1])-now)/864e5);if(x>182)x-=365;if(x<-182)x+=365;return x;};
  let i=0;L.forEach((e,j)=>{const a=Math.abs(delta(e)),b=Math.abs(delta(L[i]));if(a<b||(a===b&&delta(e)>=0&&delta(L[i])<0))i=j;});
  const W_YR=["عام واحد","عامين","أعوام","عامًا"];
  const dm=d=>{try{return d.toLocaleDateString("ar-SA-u-ca-gregory-nu-latn",{day:"numeric",month:"long"});}catch(_){return d.getDate()+"/"+(d.getMonth()+1);}};
  const rel=x=>x===0?"اليوم":x===1?"غدًا":x===-1?"أمس":x===2?"بعد يومين":x===-2?"قبل يومين":x>0?`بعد ${x} أيام`:`قبل ${-x} أيام`;
  const prevB='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
  const nextB='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>';
  box.innerHTML=`<div class="hist-top"><span class="kick" id="hist-k"></span><div class="hist-nav"><button type="button" id="hist-prev" aria-label="الحدث السابق">${prevB}</button><button type="button" id="hist-next" aria-label="الحدث التالي">${nextB}</button></div></div>
   <div class="hist-body" id="hist-body" aria-live="polite"></div><p class="hist-foot">${L.length} حدثًا من تاريخ الفضاء، ولكل حدث مصدره.</p>`;
  function draw(swap){
    const e=L[i],x=delta(e),ev=new Date(e[2],e[0]-1,e[1]);
    const yrs=Y-e[2]-((M<e[0]||(M===e[0]&&D<e[1]))?1:0);
    const ago=yrs>=1?"قبل "+arN(yrs,W_YR):e[2]===Y?"هذا العام":"قبل أقل من عام";
    $("#hist-k").textContent=x===0?"في مثل هذا اليوم":Math.abs(x)<=3?"هذا الأسبوع في تاريخ الفضاء":"من تاريخ الفضاء";
    const k=e[4]?KB_BY_ID[e[4]]:null,sr=e[5]?HSRC[e[5]]:(k&&k.url?[k.url,k.src]:null);
    const b=$("#hist-body");b.replaceChildren();
    const yr=el("div","hist-year");yr.append(el("b",null,String(e[2])),el("small",null,ago));
    const tx=el("div","hist-tx");
    tx.append(el("span","hist-date",dm(ev)+(Math.abs(x)<=3?" · "+rel(x):"")),el("p",null,e[3]));
    const acts=el("div","hist-acts");
    if(k){const g=el("button","link-btn","اقرأ عنه في الموسوعة ←");g.type="button";g.onclick=()=>goTo(k);acts.append(g);}
    if(sr){const a=el("a",null,"المصدر: "+sr[1]);a.href=sr[0];a.target="_blank";a.rel="noopener";acts.append(a);}
    tx.append(acts);b.append(yr,tx);
    if(swap){b.classList.remove("swap");void b.offsetWidth;b.classList.add("swap");}
  }
  $("#hist-prev").onclick=()=>{i=(i-1+L.length)%L.length;draw(true);};
  $("#hist-next").onclick=()=>{i=(i+1)%L.length;draw(true);};
  draw(false);
}
const TOUR_K="ufuq-tour",TOUR_OFF="ufuq-tour-off";''')

rep('''      <div class="row"><a class="btn btn-accent" href="#quiz">ابدأ الاختبار</a></div>
    </div>
  </div></section>`;''','''      <div class="row"><a class="btn btn-accent" href="#quiz">ابدأ الاختبار</a></div>
    </div>
  </div></section>
  <section class="sec" style="padding-top:0"><div class="wrap"><div class="hist" id="hist"></div></div></section>`;''')
rep('''  weekEvent();
''','''  weekEvent();
  spaceDay();
''')
rep('/* home first impression */','''/* home: this day in space history */
.hist{border-radius:18px;padding:22px 24px;color:var(--sky-fg);border:1px solid var(--sky-line);background:radial-gradient(80% 120% at 100% 0%,rgba(255,215,150,.16),transparent 60%),radial-gradient(80% 120% at 0% 100%,rgba(140,80,255,.42),transparent 62%),var(--sky-2)}
.hist-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
.hist .kick{color:#ffd796;font-size:.85rem}
.hist-nav{display:flex;gap:8px}
.hist-nav button{width:40px;height:40px;border-radius:12px;border:1px solid var(--sky-line);background:rgba(255,255,255,.07);color:var(--sky-fg);display:grid;place-items:center}
.hist-nav button:hover{border-color:var(--sky-accent);background:rgba(255,255,255,.12)}
.hist-body{display:grid;grid-template-columns:auto minmax(0,1fr);gap:24px;align-items:center;margin-top:12px;min-height:118px}
.hist-body.swap{animation:histIn .35s ease}
@keyframes histIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.hist-year{text-align:center;padding-inline-end:24px;border-inline-end:1px solid var(--sky-line);min-width:120px}
.hist-year b{display:block;font-family:var(--f-display);font-size:3rem;line-height:1.15;color:#ffd796;font-variant-numeric:tabular-nums}
.hist-year small{display:block;color:var(--sky-muted);font-size:.85rem}
.hist-date{display:inline-block;font-size:.8rem;font-weight:600;color:#ffd796;border:1px solid rgba(255,215,150,.4);border-radius:999px;padding:1px 12px}
.hist-tx p{font-family:var(--f-display);font-size:1.25rem;font-weight:600;line-height:1.7;margin-top:6px}
.hist-acts{display:flex;flex-wrap:wrap;gap:4px 18px;align-items:center;margin-top:8px;font-size:.88rem}
.hist-acts .link-btn{color:var(--sky-accent)}
.hist-acts a{color:var(--sky-muted);text-underline-offset:3px}
.hist-foot{margin-top:12px;font-size:.76rem;color:var(--sky-muted)}
@media (max-width:560px){.hist{padding:18px}.hist-body{grid-template-columns:minmax(0,1fr);gap:8px}.hist-year{display:flex;align-items:baseline;gap:10px;text-align:start;padding:0;border:0;min-width:0}.hist-year b{font-size:2.3rem}.hist-tx p{font-size:1.1rem}}

/* home first impression */''')
rep('<small class="ver">الإصدار 1.2 · آخر تحديث 20 نوفمبر 2026</small>','<small class="ver">الإصدار 1.3 · آخر تحديث 20 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch26 ok',len(EV),'events')
