# 1.1 «تطوير أفق»: صفحة «حقيقة أم خرافة؟» (#myths).
#  16 ادعاءً منتشرًا عن الفضاء (12 خرافة و4 حقائق تبدو غريبة). يختار الزائر «حقيقة» أو «خرافة»، ثم يظهر التصحيح
#  ومصدره، ورابط المعلومة كاملة. كل تصحيح مأخوذ من نص معلومة موثقة في الموسوعة (العمود الرابع في MYTHS)،
#  فلا مصادر جديدة هنا، والمصدر المعروض هو مصدر المعلومة نفسها (metaFor).
#  الدافع: أسئلة حقيقية في Quora العربي عن الأرض المسطحة (3 من 60)، والهبوط على القمر، والأبراج.
#  الوصول إليها من «اختبر نفسك» (وضع رابع)، والقائمة العلوية تبرز «اختبر نفسك» فيها.
#  data.js يتحقق أن كل معلومة في MYTHS موجودة، و flows.js يجرّب الصفحة.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# التنسيق: بخصائص منطقية، وأحجام rem، وأزرار 44 بكسل، وألوان النظام (ok/bad/accent)
rep('''@media (max-width:640px){.q-modes{grid-template-columns:minmax(0,1fr)}}''','''@media (max-width:640px){.q-modes{grid-template-columns:minmax(0,1fr)}}
/* حقيقة أم خرافة؟ */
.myths h1{font-size:clamp(1.6rem,5vw,2.2rem)}
.my-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 16px;margin:6px 0 16px}
.my-score{font-family:var(--f-display);font-weight:700;font-size:1.05rem;margin:0}
.my-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.my-item{background:var(--surface);border:1px solid var(--line);border-inline-start:4px solid var(--line);border-radius:16px;padding:16px 18px;display:grid;gap:12px}
.my-item.is-fact{border-inline-start-color:var(--ok)}
.my-item.is-myth{border-inline-start-color:var(--bad)}
.my-top{display:flex;gap:12px;align-items:flex-start}
.my-top .ic{width:38px;height:38px;border-radius:11px}
.my-claim{font-family:var(--f-display);font-size:1.12rem;font-weight:600;line-height:1.75;margin:0;padding-top:2px}
.my-act{display:flex;flex-wrap:wrap;gap:8px}
.my-act button{min-height:44px;min-width:96px;padding:8px 18px;border-radius:999px;border:1.5px solid var(--line);background:var(--surface-2);color:var(--fg);font:inherit;font-weight:600;cursor:pointer}
.my-act button:hover:not([disabled]){border-color:var(--accent)}
.my-act button[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft)}
.my-act button[disabled]{cursor:default}
.my-ans{border-top:1px dashed var(--line);padding-top:12px;display:grid;gap:8px}
.my-ans p{margin:0;line-height:1.85}
.my-head{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px}
.my-badge{display:inline-flex;align-items:center;font-weight:700;font-size:.9rem;padding:2px 14px;border-radius:999px}
.my-badge.fact{color:var(--ok);background:var(--ok-soft)}
.my-badge.myth{color:var(--bad);background:var(--bad-soft)}
.my-res{font-size:.9rem;color:var(--muted)}
.my-more{display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px}
.my-more .meta{margin:0}
.my-done{background:var(--accent-soft);border-radius:16px;padding:16px 18px;display:grid;gap:10px;margin-top:16px}
.my-done p{margin:0}''')
rep('''.q-modes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}''','''.q-modes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}''')

# البيانات والصفحة
rep('''function renderQuiz(){''','''/* «حقيقة أم خرافة؟»: [الادعاء، هل هو صحيح؟، التصحيح، المعلومة الموثقة التي أُخذ منها]. التصحيح من نص المعلومة نفسها */
const MYTHS=[
 ["الأرض مسطحة، وصور كرويتها خداع.",false,"عرف الناس كروية الأرض منذ القدم: ظل الأرض على القمر في الخسوف دائري دائمًا، والسفينة المبتعدة يختفي هيكلها قبل صواريها، وقدّر إراتوستينس محيطها من ظل شمس الظهر في مدينتين.","K306"],
 ["لا توجد جاذبية في الفضاء، ولهذا يطفو رواد الفضاء.",false,"الجاذبية على ارتفاع محطة الفضاء نحو 90% من قيمتها على سطح الأرض. يطفو الرواد لأنهم والمحطة في سقوط حر مستمر حول الأرض.","K56"],
 ["يوم كوكب الزهرة أطول من سنتها.",true,"تدور الزهرة حول نفسها مرة كل 243 يومًا أرضيًا، وتكمل دورتها حول الشمس في 225 يومًا فقط.","K78"],
 ["برجك يحدد شخصيتك ومستقبلك.",false,"ربط الأبراج بالشخصية والمستقبل ليس علمًا، ولم تدعمه أي دراسة علمية. ونجوم الكوكبة الواحدة تبدو متجاورة لكنها قد تبعد عن بعضها مئات السنين الضوئية.","K6"],
 ["للقمر جانب مظلم لا تصله الشمس أبدًا.",false,"نرى من الأرض وجهًا واحدًا للقمر، لكن جانبه البعيد ليس مظلمًا دائمًا، بل تضيئه الشمس مثل الجانب القريب.","K7"],
 ["يأتي الصيف لأن الأرض تقترب من الشمس.",false,"سبب الفصول ميل محور الأرض نحو 23.4 درجة. والدليل أن الأرض تكون في أقرب نقطة من الشمس أوائل يناير، أي في شتاء نصفنا الشمالي.","K9"],
 ["يوجد ماء على القمر.",true,"رصدت المركبة الهندية تشاندرايان-1 أدلة على الماء منتشرًا على سطحه، وفي فوهاته القطبية التي لا تصلها الشمس تراكيز عالية من الجليد.","K89"],
 ["النجم القطبي ألمع نجم في السماء.",false,"النجم القطبي متوسط السطوع، ويُستدل به على الشمال لأنه قريب جدًا من القطب السماوي فيبدو ثابتًا. أما ألمع نجوم الليل فالشعرى اليمانية.","K3"],
 ["الثقب الأسود مكنسة كونية تبتلع كل ما حولها.",false,"من بعيد تؤثر جاذبيته كأي جسم له الكتلة نفسها. ولو صارت الشمس افتراضيًا ثقبًا أسود بكتلتها لبقيت الأرض تدور في مدارها نفسه.","K34"],
 ["الشمس كرة نار تحترق.",false,"الشمس لا تحترق ولا تحتاج إلى أكسجين، بل تتوهج لأن في قلبها اندماجًا نوويًا، فالهيدروجين فيها لا يحترق بل يندمج ليصير هيليوم.","K305"],
 ["القمر يسقط نحو الأرض طوال الوقت.",true,"القمر في سقوط مستمر نحو الأرض، لكنه يتحرك جانبيًا بسرعة كافية فلا يصيبها أبدًا، وهذا هو المدار.","K303"],
 ["الشهب نجوم تتساقط من السماء.",false,"الشهاب خط مضيء نراه حين يحترق جسم صغير في الغلاف الجوي، وأغلب الشهب تحترق تمامًا.","K62"],
 ["القمر يكبر فعلًا حين يكون قرب الأفق.",false,"هذا وهم بصري اسمه «خداع القمر»: الصور تثبت أن عرض القمر قرب الأفق هو نفسه حين يكون عاليًا في السماء.","K214"],
 ["ضوء الشمس الذي تراه الآن غادر سطحها قبل نحو 8 دقائق.",true,"يقطع الضوء المسافة من سطح الشمس إلى الأرض في نحو 8 دقائق و20 ثانية.","K47"],
 ["النظارة الشمسية العادية تكفي لمشاهدة الكسوف.",false,"النظارات الشمسية العادية لا تحمي، والضرر قد يحدث دون ألم. يلزم مرشح شمسي معتمد وفق معيار ISO 12312-2.","K58"],
 ["هبوط الإنسان على القمر لم يحدث، وكان تمثيلًا.",false,"هبطت أبولو 11 على القمر في 20 يوليو 1969، وبين عامي 1969 و1972 مشى على القمر 12 رائدًا في ست رحلات.","K50"],
];
function renderMyths(){
  setNav("quiz");
  view.replaceChildren();
  const w=el("section","wrap narrow myths");
  w.append(el("span","kick","اختبر نفسك"),el("h1",null,"حقيقة أم خرافة؟"),
    el("p","muted",`${MYTHS.length} ادعاءً منتشرًا عن الفضاء. اختر جوابك، ثم اقرأ التصحيح ومصدره من معلومات الموسوعة الموثقة.`));
  const bar=el("div","my-bar"),score=el("p","my-score");score.setAttribute("aria-live","polite");
  const all=el("button","link-btn","أظهر كل الإجابات");all.type="button";bar.append(score,all);
  const list=el("ol","my-list"),done=el("div","my-done");done.hidden=true;
  let answered=0,right=0;
  const upd=()=>{score.textContent=`أجبت عن ${answered.toLocaleString("en-US")} من ${MYTHS.length.toLocaleString("en-US")}، وأصبت في ${right.toLocaleString("en-US")}`;
    if(answered===MYTHS.length){done.hidden=false;done.replaceChildren(el("p",null,right===MYTHS.length?"أصبت فيها كلها! شاركها مع أصدقائك واختبرهم.":`أصبت في ${right.toLocaleString("en-US")} من ${MYTHS.length.toLocaleString("en-US")}. الخرافات منتشرة، ولهذا جمعناها هنا.`));
      const again=el("button","btn btn-soft","أعد المحاولة");again.type="button";again.onclick=()=>{renderMyths();};done.append(again);}};
  const reveal=[];
  MYTHS.forEach(([claim,isTrue,fix,id])=>{
    const e=KB_BY_ID[id],li=el("li","my-item");
    const top=el("div","my-top"),ic=el("span","ic");ic.style.setProperty("--h",HUE[e.c]);ic.innerHTML=icon(e.c,20);top.append(ic,el("p","my-claim",claim));
    const act=el("div","my-act");act.setAttribute("role","group");act.setAttribute("aria-label","اختر جوابك: "+claim);
    const ans=el("div","my-ans");ans.hidden=true;
    const show=pickTrue=>{
      li.classList.add(isTrue?"is-fact":"is-myth");
      const head=el("div","my-head");head.append(el("span","my-badge "+(isTrue?"fact":"myth"),isTrue?"حقيقة":"خرافة"));
      if(pickTrue!=null)head.append(el("span","my-res",pickTrue===isTrue?"أصبت":"لم تُصب"));
      const more=el("div","my-more"),rd=el("button","link-btn","اقرأ المعلومة كاملة ←");rd.type="button";rd.onclick=()=>goTo(e);more.append(metaFor(e),rd);
      ans.replaceChildren(head,el("p",null,fix),more);ans.hidden=false;
      [...act.children].forEach(b=>b.disabled=true);};
    [["حقيقة",true],["خرافة",false]].forEach(([t,v])=>{const b=el("button",null,t);b.type="button";b.setAttribute("aria-pressed","false");
      b.onclick=()=>{b.setAttribute("aria-pressed","true");answered++;if(v===isTrue)right++;show(v);upd();};act.append(b);});
    reveal.push(()=>{if(ans.hidden)show(null);});
    li.append(top,act,ans);list.append(li);});
  all.onclick=()=>{reveal.forEach(f=>f());all.hidden=true;};
  w.append(bar,list,done);view.append(w);upd();
}
function renderQuiz(){''')
rep('''  else if(h==="changelog") renderChangelog();''','''  else if(h==="changelog") renderChangelog();
  else if(h==="myths") renderMyths();''')

# وضع رابع في «اختبر نفسك» يفتح الصفحة
rep('''  cert:\'''','''  myth:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M9.2 9.2a2.9 2.9 0 1 1 4.3 2.5c-.9.5-1.5 1.1-1.5 2.1v.4"/><path d="M12 17.4v.1"/></svg>',
  cert:\'''')
rep('''    mode("cert","شهادة الإنجاز",''','''    mode("myth","حقيقة أم خرافة؟",`${MYTHS.length} ادعاءً منتشرًا عن الفضاء: اختر، ثم اقرأ التصحيح ومصدره`,"",()=>{location.hash="myths";});
    mode("cert","شهادة الإنجاز",''')
open(P,'w',encoding='utf-8').write(s);print('patch51 ok')
