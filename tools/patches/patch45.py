# 1.1 «تطوير أفق»، الخطوة 3: ترتيب نتائج البحث.
#  1) التنوين: «كم قمرًا للمشتري؟» كانت تُقطّع «قمرا» فلا تطابق «قمر». ktn يحذف ألف تنوين الفتح («ًا»/«اً») قبل التقطيع،
#     في ktoks و KB_VOCAB و«كيف فكّر أفق؟». فلاتر الصفحات (knorm) لم تتغير.
#  2) searchKB يرتب النتائج بـ rank بدل score:
#     rank = الدرجة + نقطتان × نسبة ما غطّته كلمات السؤال من عنوان المعلومة (كان 0.1 للتعادل فقط)،
#     لأن أسئلة الناس تشبه عناوين المعلومات: «من وين تجي المذنبات» ← «من أين تأتي المذنبات؟».
#     ومصطلح القاموس يأخذ 70% من rank، إلا إذا سأل الزائر عن معنى كلمة (معنى/يعني/تعريف/مصطلح)،
#     أو كتب المصطلح نفسه بلا أداة سؤال (KASK: ليش، كيف، وين…). فلا يغلب تعريفُ «المذنب» المعلومةَ «من أين تأتي المذنبات؟».
#  score بقي كما هو (الحد 2 في kbPick، و1.5 في بحث الرئيسية، و3 في «معلومات مرتبطة» بالقاموس)، فلم تتغير معاني الحدود.
#  «كيف فكّر أفق؟» يعرض rank ويشرح النقطتين الإضافيتين ونسبة القاموس.
#  جُرّبت قبله طريقة BM25 (وزن الندرة + طول قائمة الكلمات المفتاحية) فأضرّت: 276 عنوانًا فقط من 301 يجد نفسه أولًا.
#  اختبار: ask.js من 37 إلى 40 من 50، وكل عنوان يجد معلومته أولًا (301/301).
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# 1) التنوين
rep('''function knorm(s){return String(s).replace(/[\\u200B\\u2060-\\u2064]/g,"")''','''/* ألف تنوين الفتح لا تدخل في الكلمة عند البحث: «قمرًا» ← «قمر» */
const ktn=s=>String(s).replace(/[\\u200B\\u2060-\\u2064]/g,"").replace(/\\u064Bا|ا\\u064B/g,"");
function knorm(s){return String(s).replace(/[\\u200B\\u2060-\\u2064]/g,"")''')
rep('''KB.forEach(e=>[e.k,e.t,e.a].forEach(x=>knorm(x).split(''','''KB.forEach(e=>[e.k,e.t,e.a].forEach(x=>knorm(ktn(x)).split(''')
rep('''function ktoks(s){return knorm(s).split(''','''function ktoks(s){return knorm(ktn(s)).split(''')
rep('''  const raw=knorm(q).split(/[^\\p{L}\\p{N}.]+/u).map(''','''  const raw=knorm(ktn(q)).split(/[^\\p{L}\\p{N}.]+/u).map(''')

# 2) rank
rep('''      const ts=f[1][0];let hit=0;for(const w of qt) if(ts.has(w)) hit++;
      out.push({e,score:score+(ts.size?0.1*hit/ts.size:0),mt});''','''      const ts=f[1][0];let hit=0;for(const w of qt) if(ts.has(w)) hit++;
      const tf=ts.size?hit/ts.size:0;
      out.push({e,score:score+0.1*tf,rank:score+2*tf,mt,f});''')
rep('''  for(const h of out){h.cov=tot?h.mt.reduce((a,i)=>a+wq[i],0)/tot:0;delete h.mt;}
  return out.sort((a,b)=>b.score-a.score);
}''','''  /* الترتيب rank: الدرجة + نقطتان × نسبة ما غطّته كلماتك من عنوان المعلومة. ومصطلح القاموس يأخذ 70% منه،
     إلا إذا سألت عن معنى كلمة، أو كتبت المصطلح نفسه دون أداة سؤال */
  const raw=knorm(q).split(/[^\\p{L}\\p{N}]+/u),askQ=raw.some(w=>KASK.has(w)),defW=/معني|يعني|تعريف|مصطلح/.test(raw.join(" "));
  const content=qt.filter((w,i)=>wq[i]>0);
  for(const h of out){h.cov=tot?h.mt.reduce((a,i)=>a+wq[i],0)/tot:0;
    if(h.e.c==="glossary"&&!defW){const ks=[...h.f[0][0]];
      const isTerm=!askQ&&content.length&&content.every(w=>ks.some(x=>x===w||(w.length>=3&&x.length>=3&&(x.startsWith(w)||w.startsWith(x)))));
      if(!isTerm)h.rank*=.7;}
    delete h.mt;delete h.f;}
  return out.sort((a,b)=>b.rank-a.rank||b.score-a.score);
}''')
rep('''/* كلمات تصوغ السؤال ولا تحدد موضوعه''','''/* أدوات السؤال بعد توحيد الحروف: إن وُجدت فالزائر لا يطلب تعريف كلمة من القاموس */
const KASK=new Set(["لماذا","ليش","ليه","كيف","شلون","وشلون","متي","كم","اين","وين","هل","مين","منين"]);
/* كلمات تصوغ السؤال ولا تحدد موضوعه''')

# 3) «كيف فكّر أفق؟»
rep('''الكلمة التي تطابق الكلمات المفتاحية لمعلومة تأخذ 3 نقاط، وعنوانَها نقطتين، ونصَّها نقطة واحدة، وجزء الكلمة يأخذ 60% من ذلك.`);''',
'''الكلمة التي تطابق الكلمات المفتاحية لمعلومة تأخذ 3 نقاط، وعنوانَها نقطتين، ونصَّها نقطة واحدة، وجزء الكلمة يأخذ 60% من ذلك. وإذا غطّت كلماتك عنوان المعلومة كله أخذت نقطتين زيادة، وإن غطّت بعضه أخذت جزءًا منهما. ومصطلحات القاموس تأخذ 70% من درجتها، إلا إذا سألت عن معنى كلمة.`);''')
rep('''    const mx=top[0].score;
    top.forEach(h=>{const r=el("div","hit"+(h.score<2?" weak":""));r.append(el("span",null,h.e.t),el("b",null,fmt1(h.score)));const b=el("span","bar2"),i=el("i");i.style.width=Math.max(4,h.score/mx*100)+"%";b.append(i);r.append(b);l3.append(r);});
    if(top.some(h=>h.score<2))l3.append(el("small",null,"الباهتة درجتها أقل من 2، فاعتبرها تطابقًا ضعيفًا وتجاهلها."));''',
'''    const mx=top[0].rank;
    top.forEach(h=>{const r=el("div","hit"+(h.score<2?" weak":""));r.append(el("span",null,h.e.t),el("b",null,fmt1(h.rank)));const b=el("span","bar2"),i=el("i");i.style.width=Math.max(4,h.rank/mx*100)+"%";b.append(i);r.append(b);l3.append(r);});
    if(top.some(h=>h.score<2))l3.append(el("small",null,"الباهتة درجتها قبل نقاط العنوان أقل من 2، فاعتبرها تطابقًا ضعيفًا وتجاهلها."));''')
open(P,'w',encoding='utf-8').write(s);print('patch45 ok')
