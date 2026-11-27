# 1.1 «تطوير أفق»، الخطوة 1: «اسأل أفق» يعتذر عن السؤال الذي ليس في الموسوعة بدل أن يعرض معلومة لا تخصه.
#  المشكلة: كان يكفي أن تطابق كلمة واحدة من السؤال (3 نقاط، والحد 2) ليعرض المعلومة كأنها الجواب.
#   «من فاز بكأس العالم 2022» ← صورة ثقب مجرتنا (بسبب 2022)، و«وش أحسن جوال» ← «المركبة الجوالة».
#  الحل: searchKB يحسب لكل نتيجة «التغطية» cov: كم تغطي من وزن كلمات السؤال.
#   وزن الكلمة = log(عدد المعلومات / عدد المعلومات التي فيها الكلمة): النادرة أثقل، وغير الموجودة في الموسوعة أثقل شيء،
#   لأنها غالبًا موضوع السؤال (نيبيرو، ستارلينك). وكلمات صياغة السؤال العامية (KFILL: ياخذ، عشان، يصير…) وزنها صفر.
#  kbPick: يجيب أفق من المعلومة الأعلى درجة فقط إذا كانت درجتها 2 أو أكثر وتغطيتها نصف الوزن على الأقل (KCOV).
#   ولا ينزل إلى المعلومة التالية إن لم تغطِّ الأولى، لأن ذلك كان يأتي بمعلومات أبعد.
#  الترتيب نفسه لم يتغير (score كما هو)، ولا البحث في الرئيسية، ولا السياق الذي يُرسل للنموذج في نسخة Claude.
#  اختبار: tools/tests/ask.js يستدعي kbPick نفسها.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# 1) كلمات الصياغة + التغطية في searchKB + kbPick
rep('''function ktoks(s){return knorm(s).split(/[^\\p{L}\\p{N}.]+/u).filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1);}
''','''function ktoks(s){return knorm(s).split(/[^\\p{L}\\p{N}.]+/u).filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1);}
/* كلمات تصوغ السؤال ولا تحدد موضوعه (أغلبها عامية). تبقى في الدرجة كما هي، لكن وزنها صفر في «التغطية» */
const KFILL=new Set(ktoks("ماهو ماهي مااهو وشلون شلون وين مين ليه عشان علشان ياخذ يصير صار وقت الجاي الجايه عندنا عندي حقي حقنا اللي الي بالضبط طيب بس شي شيء نقدر اقدر يقدر نشوف اشوف يشوف سالفه قصه مصطلح مثال تجي يجي يوصل يوصلنا قولي ودي كذا مو"));
''')
rep('''  const qt=[...new Set(ktoks(q))]; if(!qt.length) return [];
  const out=[];
  for(const {e,f} of KB_INDEX){
    let score=0;
    for(const w of qt){
      let best=0;
      for(const [set,wt] of f){
        if(set.has(w)){best=Math.max(best,wt);continue;}
        if(w.length>=3) for(const x of set){ if(x.length>=3&&(x.startsWith(w)||w.startsWith(x))){best=Math.max(best,wt*.6);break;} }
      }
      score+=best;
    }
    if(score>0){
      /* tie-break only (scores step by 0.2): prefer the entry whose own question is closest to the query */
      const ts=f[1][0];let hit=0;for(const w of qt) if(ts.has(w)) hit++;
      out.push({e,score:score+(ts.size?0.1*hit/ts.size:0)});
    }
  }
  return out.sort((a,b)=>b.score-a.score);
}''','''  const qt=[...new Set(ktoks(q))]; if(!qt.length) return [];
  const out=[],df=qt.map(()=>0);
  for(const {e,f} of KB_INDEX){
    let score=0;const mt=[];
    qt.forEach((w,i)=>{
      let best=0;
      for(const [set,wt] of f){
        if(set.has(w)){best=Math.max(best,wt);continue;}
        if(w.length>=3) for(const x of set){ if(x.length>=3&&(x.startsWith(w)||w.startsWith(x))){best=Math.max(best,wt*.6);break;} }
      }
      score+=best;
      if(best>0){mt.push(i);df[i]++;}
    });
    if(score>0){
      /* tie-break only (scores step by 0.2): prefer the entry whose own question is closest to the query */
      const ts=f[1][0];let hit=0;for(const w of qt) if(ts.has(w)) hit++;
      out.push({e,score:score+(ts.size?0.1*hit/ts.size:0),mt});
    }
  }
  /* التغطية cov: نصيب كلمات السؤال التي وجدتها المعلومة من وزنها كله. الكلمة النادرة في الموسوعة أثقل،
     والكلمة غير الموجودة فيها أبدًا أثقل شيء، وكلمات الصياغة (KFILL) وزنها صفر */
  const N=KB_INDEX.length+1,wq=qt.map((w,i)=>KFILL.has(w.replace(/^\\.+|\\.+$/g,""))?0:Math.log(N/(df[i]+1))),tot=wq.reduce((a,b)=>a+b,0);
  for(const h of out){h.cov=tot?h.mt.reduce((a,i)=>a+wq[i],0)/tot:0;delete h.mt;}
  return out.sort((a,b)=>b.score-a.score);
}
/* «اسأل أفق» يجيب من المعلومة الأعلى درجة فقط إذا كانت درجتها 2 أو أكثر وغطّت نصف وزن كلمات السؤال على الأقل، وإلا اعتذر */
const KCOV=.5;
function kbPick(hits){const h=hits[0];return h&&h.score>=2&&h.cov>=KCOV?h:null;}''')

# 2) الجواب المحلي يستخدم kbPick
rep('''  const good=hits.filter(h=>h.score>=2);
  if(!good.length){bubble.append(el("p",null,"لم أجد هذا في الموسوعة بعد. جرّب كلمات أخرى، أو تصفّح المواضيع والقاموس."));}
  else{
    const e=good[0].e;''','''  const good=hits.filter(h=>h.score>=2),pick=kbPick(hits);
  if(!pick){bubble.append(el("p",null,"لم أجد هذا في الموسوعة بعد. جرّب كلمات أخرى، أو تصفّح المواضيع والقاموس."));}
  else{
    const e=pick.e;''')

# 3) «كيف فكّر أفق؟» يشرح الشرط الجديد
rep('''  else l4.append(el("b",null,"اختار الجواب. "),n?"عرض نص المعلومة الأعلى درجة كما هو، دون أن يؤلف شيئًا من عنده.":"لم يجد معلومة قوية، فاعتذر بدل أن يخمّن.");''',
'''  else{const pc=hits[0]?Math.round(hits[0].cov*100)+"%":"";
    l4.append(el("b",null,"اختار الجواب. "),kbPick(hits)?`تأكد أن المعلومة الأعلى درجة تغطي نصف وزن كلماتك على الأقل (غطّت ${pc})، فعرض نصها كما هو، دون أن يؤلف شيئًا من عنده.`
      :n?`المعلومة الأعلى درجة لا تغطي إلا ${pc} من وزن كلماتك، والمطلوب النصف على الأقل. والكلمة النادرة في الموسوعة أثقل، والكلمة غير الموجودة فيها أثقل شيء. فاعتذر بدل أن يعرض معلومة لا تخص سؤالك.`
      :"لم يجد معلومة قوية، فاعتذر بدل أن يخمّن.");}''')

# 4) معلومة «كيف يعمل أفق» (K187) تصف الطريقة نفسها
rep('''ثم يعرض لك المعلومة الأعلى درجة كما هي، أو يرسل أفضل المعلومات إلى نموذج لغوي ليكتب منها جوابًا ويذكر أرقامها.''',
'''ثم يعرض لك المعلومة الأعلى درجة كما هي إذا غطّت نصف كلمات سؤالك المهمة على الأقل، وإلا أخبرك أنه لم يجد الجواب. أو يرسل أفضل المعلومات إلى نموذج لغوي ليكتب منها جوابًا ويذكر أرقامها.''')
# 5) زر «اسأل أفق عنه» في القاموس يرسل جملة ثابتة («… بمثال بسيط من الحياة اليومية.»): ذيلها موجه للنموذج اللغوي،
#    فلا يدخل في البحث، وإلا ثقلت كلماته («بسيط»، «الحياة») وغطّت على المصطلح نفسه. الجملة تُرسل كاملة كما هي.
rep('''/* «اسأل أفق» يجيب من المعلومة الأعلى درجة فقط''','''const GLOSS_TAIL=" بمثال بسيط من الحياة اليومية.";
/* «اسأل أفق» يجيب من المعلومة الأعلى درجة فقط''')
rep('''openDrawer(`اشرح لي مصطلح «${t.ar}» (${t.en}) بمثال بسيط من الحياة اليومية.`)''','''openDrawer(`اشرح لي مصطلح «${t.ar}» (${t.en})`+GLOSS_TAIL)''')
rep('''  const hits=searchKB(q);
  const bubble=addMsg("bot thinking");''','''  const hits=searchKB(q.replace(GLOSS_TAIL,""));
  const bubble=addMsg("bot thinking");''')
open(P,'w',encoding='utf-8').write(s);print('patch43 ok')
