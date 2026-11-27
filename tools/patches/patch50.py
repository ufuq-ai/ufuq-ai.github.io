# 1.1 «تطوير أفق»: اقتراحات حين لا يجد «اسأل أفق» جوابًا («تقصد…؟»).
#  حين يعتذر أفق، يعرض أقرب ثلاث معلومات فيها كلمات من السؤال (kbSuggest: درجتها 2 فأكثر، بترتيب rank)،
#  أزرارًا يفتح كل منها جواب تلك المعلومة.
#  الصياغة تقول إنها ليست جوابًا («أقرب ما فيها لكلمات سؤالك»)، لا «هل تقصد؟»: في الاختبار لم يفصل أي حد تغطية
#  بين اقتراح مفيد واقتراح بلا داع، فالأسئلة التي ليست في الموسوعة تظهر لها اقتراحات بأي حد (32 من 37 بلا حد).
#  وفي المقابل: من 21 سؤالًا لها جواب واعتذر عنها أفق، المعلومة الصحيحة بين الاقتراحات في 16.
#  ask.js يقيس ذلك («misses rescued by suggestions»).
#  ومعه: أزرار الرسائل في «اسأل أفق» صار ارتفاعها 44 بكسل على الأقل (كان 32).
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''function kbPick(hits){const h=hits[0];return h&&h.score>=2&&h.cov>=KCOV?h:null;}''','''function kbPick(hits){const h=hits[0];return h&&h.score>=2&&h.cov>=KCOV?h:null;}
/* حين لا يجيب: أقرب ثلاث معلومات فيها كلمات من السؤال، تُعرض اقتراحات لا جوابًا */
function kbSuggest(hits){return hits.filter(h=>h.score>=2).slice(0,3);}''')

rep('''  if(!pick){bubble.append(el("p",null,"لم أجد هذا في الموسوعة بعد. جرّب كلمات أخرى، أو تصفّح المواضيع والقاموس."));}''',
'''  if(!pick){const sg=kbSuggest(hits);
    if(!sg.length)bubble.append(el("p",null,"لم أجد هذا في الموسوعة بعد. جرّب كلمات أخرى، أو تصفّح المواضيع والقاموس."));
    else{bubble.append(el("p",null,"لم أجد جوابًا لسؤالك في الموسوعة بعد. هذه أقرب معلوماتها لكلمات سؤالك، وقد لا تكون ما تبحث عنه:"));
      const more=el("div","schips");more.style.marginTop="8px";
      sg.forEach(({e})=>{const c=el("button","schip",e.t);c.type="button";c.onclick=()=>ask(e.t);more.append(c);});bubble.append(more);}}''')

rep('''فاعتذر بدل أن يعرض معلومة لا تخص سؤالك.`''','''فاعتذر بدل أن يعرض معلومة لا تخص سؤالك، ثم اقترح أقرب المعلومات لكلماتك دون أن يقول إنها الجواب.`''')
# مساحة اللمس: أزرار الرسائل («قد يهمك أيضًا» والاقتراحات) كانت بارتفاع 32 بكسل، والحد المقبول 44
rep('''.schip:hover{border-color:var(--sky-accent)}''','''.schip:hover{border-color:var(--sky-accent)}
.msg .schip{min-height:44px;padding:8px 14px}''')
open(P,'w',encoding='utf-8').write(s);print('patch50 ok')
