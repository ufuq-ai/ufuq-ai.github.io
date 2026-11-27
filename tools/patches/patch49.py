# 1.1 «تطوير أفق»، الخطوة 7: ثماني معلومات جديدة من أسئلة الناس الحقيقية (K302–K309).
#  الأسئلة من 60 سؤالًا حقيقيًا في Quora العربي (مجموعتا QUORA و QUORA2 في tools/tests/ask.js)، لم يكن لها جواب في الموسوعة.
#  كل جملة منقولة من صفحة المصدر بعد فتحها فعلًا (27 نوفمبر 2026). الأدلة الحرفية ودرجة الثقة في
#  tools/research/notes/real_questions_1_1.json و .md، ومعها سؤالان لم يُضافا لعدم وجود مصدر يُفتح.
import os,json
D=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(D,'..','src','ai-horizon.html')
N=os.path.join(D,'..','research','notes','real_questions_1_1.json')
s=open(P,encoding='utf-8').read()
cards=json.load(open(N,encoding='utf-8'))['entries']
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)
i=s.index('\n["K301", ');j=s.index('\n',i+1)
assert s[j+1:j+3]=='];',s[j+1:j+10]
rows=''.join('\n'+json.dumps([c['id'],c['section'],c['q'],c['keywords'],c['a'],c['tag'],c['source_name']],ensure_ascii=False)+',' for c in cards)
s=s[:j]+rows+s[j:]
k=s.index('\n/* تصحيحات نوفمبر 2026 */\n');k=s.index('\n',k+1);k=s.index('\n',k+1)
src='\n/* 1.1: معلومات من أسئلة الناس الحقيقية (Quora العربي) */\nObject.assign(SRC,'+json.dumps({c['id']:[c['url'],c['source_name']] for c in cards},ensure_ascii=False)+');'
s=s[:k]+src+s[k:]
for c in cards: assert len(c['a'])<=700,(c['id'],len(c['a']))
open(P,'w',encoding='utf-8').write(s);print('patch49 ok',len(cards),'entries')
