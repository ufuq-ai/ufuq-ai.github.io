# 1.1 «تطوير أفق»، الخطوة 2: إصلاح تقطيع الكلمات في البحث.
#  1) kstem كان يحذف أول حرف من أي كلمة من 4 حروف فأكثر تبدأ بـ و/ل/ب/ف/ك، ظنًّا أنه حرف عطف أو جر:
#     «كوكب» ← «وكب»، «بلوتو» ← «لوتو»، «بارد» ← «ارد»، «بكرة» ← «كره».
#     الآن لا يحذفه إلا إذا كان الباقي كلمة موجودة في الموسوعة (KB_VOCAB): «وكوكب» ← «كوكب»، أما «كوكب» فتبقى.
#     ولا يحذفه إذا جاءت الكلمة نفسها في الموسوعة بـ«ال» («الفلكي»، «الكتلة»)، لأنها حينئذ كلمة أصلية لا حرف جر أو عطف:
#     فتصير «فلكي» و«الفلكي» كلتاهما «فلك» بدل «لكي» (كلمة «لكي» نفسها في النصوص).
#     KB_VOCAB يُبنى مرة واحدة من كلمات المعلومات والمصطلحات (بعد توحيد الحروف)، ومعها الكلمة بلا «ال» وأخواتها.
#  2) ktoks كان يُبقي النقطة في آخر الكلمة (لأن النقطة مسموحة للأرقام مثل 3.26)، فكلمة آخر الجملة «أحمر.»
#     لا تطابق «أحمر» إلا مطابقة جزئية. الآن تُحذف النقطة من طرفي الكلمة، وتبقى داخل الأرقام.
#  اختبار: tools/tests/ask.js، و data.js (selfMiss)، و flows.js.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''const KB_WORDS=new Set(["فالكون"]);
function kstem(t){
  if(/^[a-z0-9.]+$/.test(t)) return t.replace(/s$/,"");
  if(KB_WORDS.has(t)) return t;
  let cut=false;
  for(const p of ["وال","بال","كال","فال","لل","ال"]) if(t.startsWith(p)&&t.length-p.length>=2){t=t.slice(p.length);cut=true;break;}
  if(!cut&&t.length>=4&&/^[ولبفك]/.test(t)&&!KB_WORDS.has(t)) t=t.slice(1);''','''const KB_WORDS=new Set(["فالكون"]);
/* كل كلمات الموسوعة بعد توحيد الحروف، ومعها الكلمة بلا «ال» وأخواتها: به يعرف kstem هل الحرف الأول زائد */
const KPRE=["وال","بال","كال","فال","لل","ال"];
const KB_VOCAB=new Set();
KB.forEach(e=>[e.k,e.t,e.a].forEach(x=>knorm(x).split(/[^\\p{L}\\p{N}]+/u).forEach(w=>{if(!w)return;KB_VOCAB.add(w);
  for(const p of KPRE) if(w.startsWith(p)&&w.length-p.length>=2){KB_VOCAB.add(w.slice(p.length));break;}})));
function kstem(t){
  if(/^[a-z0-9.]+$/.test(t)) return t.replace(/s$/,"");
  if(KB_WORDS.has(t)) return t;
  let cut=false;
  for(const p of KPRE) if(t.startsWith(p)&&t.length-p.length>=2){t=t.slice(p.length);cut=true;break;}
  /* و/ل/ب/ف/ك في أول الكلمة: تُحذف فقط إذا كان الباقي كلمة في الموسوعة («وكوكب» ← «كوكب»)، ولم ترد الكلمة نفسها بـ«ال»
     في الموسوعة («الكوكب»، «الفلكي»)؛ فتبقى «كوكب» و«فلكي» و«بلوتو» و«بارد» كما هي */
  if(!cut&&t.length>=4&&/^[ولبفك]/.test(t)&&!KB_VOCAB.has("ال"+t)&&KB_VOCAB.has(t.slice(1))) t=t.slice(1);''')

rep('''function ktoks(s){return knorm(s).split(/[^\\p{L}\\p{N}.]+/u).filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1);}''',
'''function ktoks(s){return knorm(s).split(/[^\\p{L}\\p{N}.]+/u).map(w=>w.replace(/^\\.+|\\.+$/g,"")).filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1);}''')
# «كيف فكّر أفق؟» يعرض الكلمات بالتقطيع نفسه
rep('''  const raw=knorm(q).split(/[^\\p{L}\\p{N}.]+/u).filter(Boolean);''','''  const raw=knorm(q).split(/[^\\p{L}\\p{N}.]+/u).map(w=>w.replace(/^\\.+|\\.+$/g,"")).filter(Boolean);''')
open(P,'w',encoding='utf-8').write(s);print('patch44 ok')
