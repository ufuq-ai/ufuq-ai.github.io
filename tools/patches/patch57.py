# 1.2: عدّاد «اسأل أفق» في GoatCounter (بموافقة خالد).
#  نافذة «اسأل أفق» ليست صفحة، فلم يكن العدّاد يراها. الآن يُرسل ثلاثة أحداث فقط، بلا نص السؤال:
#  ask-open (انفتحت النافذة)، ask-answer (وجد جوابًا في الموسوعة)، ask-decline (اعتذر لأنه لم يجد).
#  askCount لا تفعل شيئًا إن لم يكن العدّاد موجودًا (الاختبارات ونسخة Claude)، فالعدّاد يُضاف في النسخة العامة فقط.
#  وسطر الخصوصية في «عن المشروع» يذكر ذلك. flows.js يتحقق من الأحداث وأنها لا تحمل نص السؤال.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)
rep('''function openDrawer(q){drawer.hidden=false;''','''/* عدّاد «اسأل أفق» (GoatCounter في الموسوعة العامة فقط): انفتح، وجاوب، واعتذر. لا يُرسل نص السؤال أبدًا */
const ASK_EV={open:"اسأل أفق: انفتح",answer:"اسأل أفق: جاوب",decline:"اسأل أفق: اعتذر"};
function askCount(what){try{const g=window.goatcounter;if(ASK_EV[what]&&g&&typeof g.count==="function")g.count({path:"ask-"+what,title:ASK_EV[what],event:true});}catch(_){}}
function openDrawer(q){askCount("open");drawer.hidden=false;''')
rep('''  const good=hits.filter(h=>h.score>=2),pick=kbPick(hits);
  if(!pick){''','''  const good=hits.filter(h=>h.score>=2),pick=kbPick(hits);
  askCount(pick?"answer":"decline");
  if(!pick){''')
rep('''<li><b>الخصوصية:</b> نعدّ زيارات الموقع وأكثر صفحاته زيارة بأداة GoatCounter، دون ملفات تعريف الارتباط (الكوكيز)، ودون أن تُحفظ أي بيانات شخصية عن الزائر.</li>''',
'''<li><b>الخصوصية:</b> نعدّ زيارات الموقع وأكثر صفحاته زيارة بأداة GoatCounter، دون ملفات تعريف الارتباط (الكوكيز)، ودون أن تُحفظ أي بيانات شخصية عن الزائر. ونعدّ كذلك كم مرة فُتح «اسأل أفق» وكم مرة وجد جوابًا أو اعتذر، دون أن نحفظ نص أي سؤال.</li>''')
open(P,'w',encoding='utf-8').write(s);print('patch57 ok')
