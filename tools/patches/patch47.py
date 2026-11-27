# 1.1 «تطوير أفق»، الخطوة 5: تصحيح الأخطاء الإملائية في البحث.
#  kfix: كلمة السؤال التي من 5 حروف فأكثر (بعد التقطيع)، ولا توجد في الموسوعة هي ولا أخواتها في المعنى،
#  ولا هي بداية كلمة في الموسوعة، ولا كلمة فيها من 5 حروف فأكثر بزيادة حرفين على الأكثر (فـ«اقلدس» ليست «اقل» وزيادة)،
#  تُجرّب بأقرب كلمات الموسوعة إليها بفرق حرف واحد: حرف زائد أو ناقص أو مختلف، أو حرفان متجاوران مقلوبان (kd1).
#  والحروف التي يخلط الناس بينها فرقها صفر (KCONF): س/ص، ض/ظ، ذ/ز، ت/ط، ج/غ/ق (الأسماء الأجنبية: هوكينج/هوكينغ).
#  أقرب 3 كلمات، والأكثر ورودًا في الموسوعة أولًا. وتأخذ وزن أخوات المعنى (KSYNW = 70%).
#  الكلمات القصيرة لا تُصحَّح، لأن الفرق بحرف واحد فيها يغيّر المعنى كثيرًا (قمر/قدر).
#  مفردات الموسوعة (kbToks) تُبنى مرة من KB_INDEX، وتُعاد إن تغيّر.
#  وشرط القاموس («كتب المصطلح نفسه؟» في searchKB) صار يرى أخوات الكلمة وتصحيحها.
#  «كيف فكّر أفق؟» يعرض التصحيح.
#  اختبار: ask.js، وأسئلة جديدة فيها أخطاء إملائية كُتبت قبل التصحيح.
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''/* «اسأل أفق» يجيب من المعلومة الأعلى درجة فقط''','''/* تصحيح الإملاء: كلمة من 5 حروف فأكثر لا توجد في الموسوعة (لا هي ولا أخواتها) تُجرّب بأقرب كلماتها إليها بفرق حرف واحد.
   والحروف التي يخلط الناس بينها فرقها صفر */
const KCONF=["سص","ضظ","ذز","تط","جغق"];
const kcls=s=>[...s].map(c=>{for(const g of KCONF) if(g.includes(c)) return g[0];return c;}).join("");
function kd1(a,b){ /* هل الفرق بين الكلمتين حرف واحد على الأكثر (زائد، ناقص، مختلف، أو متجاوران مقلوبان)؟ */
  a=kcls(a);b=kcls(b);if(a===b)return true;
  const m=a.length,n=b.length;if(Math.abs(m-n)>1)return false;
  let i=0;while(i<m&&i<n&&a[i]===b[i])i++;
  if(m===n) return a.slice(i+1)===b.slice(i+1)||(a[i]===b[i+1]&&a[i+1]===b[i]&&a.slice(i+2)===b.slice(i+2));
  return m>n?a.slice(i+1)===b.slice(i):a.slice(i)===b.slice(i+1);
}
let KB_TOKS=null,KB_TOKS_OF=null;
function kbToks(){ /* كل كلمات الموسوعة بعد التقطيع، ومع كل كلمة عدد المعلومات التي وردت فيها */
  if(KB_TOKS_OF!==KB_INDEX){KB_TOKS=new Map();
    KB_INDEX.forEach(({f})=>{const seen=new Set();f.forEach(([set])=>set.forEach(x=>seen.add(x)));seen.forEach(x=>KB_TOKS.set(x,(KB_TOKS.get(x)||0)+1));});
    KB_TOKS_OF=KB_INDEX;}
  return KB_TOKS;}
function kfix(w,alts){
  if(w.length<5||/^[a-z0-9.]+$/.test(w))return [];
  const V=kbToks();
  /* موجودة إن وردت هي أو أختها، أو كانت بداية كلمة في الموسوعة، أو كلمة في الموسوعة (5 حروف فأكثر) بزيادة حرفين على الأكثر
     في آخرها؛ لا بداية قصيرة بالصدفة: «اقلدس» ليست «اقل»، و«اورانص» ليست «اورا» */
  for(const a of alts){if(V.has(a))return [];
    for(const x of V.keys())if(x.startsWith(a)||(x.length>=5&&a.length-x.length<=2&&a.startsWith(x)))return [];}
  const c=[];for(const [x,n] of V)if(x.length>=4&&!/^[a-z0-9.]+$/.test(x)&&kd1(w,x))c.push([x,n]);
  return c.sort((p,q)=>q[1]-p[1]).slice(0,3).map(p=>p[0]);
}
/* «اسأل أفق» يجيب من المعلومة الأعلى درجة فقط''')

rep('''  const out=[],df=qt.map(()=>0),qa=qt.map(kalts);''','''  const out=[],df=qt.map(()=>0),qa=qt.map(w=>{const a=kalts(w),fx=kfix(w,a);return fx.length?[...a,...fx]:a;});''')

rep('''  if(syn.length)l1.append(el("small",null,"وبحث معها عن كلمات بمعناها: "+syn.map(([w,a])=>w+" ← "+a.slice(0,4).join("، ")).join(" · ")));''',
'''  if(syn.length)l1.append(el("small",null,"وبحث معها عن كلمات بمعناها: "+syn.map(([w,a])=>w+" ← "+a.slice(0,4).join("، ")).join(" · ")));
  const fix=kept.map(w=>[w,kfix(w,kalts(w))]).filter(x=>x[1].length);
  if(fix.length)l1.append(el("small",null,(syn.length?" ":"")+"وصحّح إملاء كلمات لم يجدها في الموسوعة: "+fix.map(([w,a])=>w+" ← "+a.join(" أو ")).join(" · ")));''')
rep('''والكلمة التي بمعنى كلمتك 70%.''','''والكلمة التي بمعنى كلمتك أو تصحيحها 70%.''')
# شرط القاموس («كتب المصطلح نفسه؟») يرى أخوات الكلمة وتصحيحها: «ماهو الثقب الاسوود» تعريف «الثقب الأسود»
rep('''  const content=qt.filter((w,i)=>wq[i]>0);''','''  const content=qa.filter((al,i)=>wq[i]>0);''')
rep('''      const isTerm=!askQ&&content.length&&content.every(w=>ks.some(x=>x===w||(w.length>=3&&x.length>=3&&(x.startsWith(w)||w.startsWith(x)))));''',
    '''      const isTerm=!askQ&&content.length&&content.every(al=>al.some(w=>ks.some(x=>x===w||(w.length>=3&&x.length>=3&&(x.startsWith(w)||w.startsWith(x))))));''')
open(P,'w',encoding='utf-8').write(s);print('patch47 ok')
