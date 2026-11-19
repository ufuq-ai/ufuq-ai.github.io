import json,re
P='/home/claude/ai-horizon.html';s=open(P,encoding='utf-8').read()
def kw(kid,add='',drop=()):
    global s
    m=re.search(r'^\["%s",.*$'%kid,s,re.M);line=m.group(0);comma=line.endswith(',')
    r=json.loads(line.rstrip(','));k=r[3]
    for d in drop: assert d in k,(kid,d); k=k.replace(d,' ')
    r[3]=re.sub(r'\s+',' ',(k+' '+add).strip())
    s=s[:m.start()]+json.dumps(r,ensure_ascii=False)+(',' if comma else '')+s[m.end():]
kw('K50','وصل الانسان وصول الانسان كيف وصلنا الى القمر اول هبوط')
kw('K56','رواد الفضاء يطفو المحطه')
kw('K76','الدورة الشمسية الدوره الشمسيه دورة النشاط الشمسي البقع الشمسيه ذروه')
kw('K240','توجد وجود')
kw('K38','الاقزام البيضاء',drop=('قزم ابيض',))
kw('K241','',drop=('موجات الجاذبية','gravitational waves'))
kw('K260','اول رائد فضاء اماراتي يسير يمشي')
open(P,'w',encoding='utf-8').write(s);print('ok')
