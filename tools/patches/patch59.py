# 1.3: معلومتان لصفحة «نجم يوم ميلادك» (K312 كيف يعرف العلماء بُعد النجوم، K313 هل نرى النجوم كما هي الآن).
#  كل جملة منقولة من صفحة المصدر بعد فتحها (28 نوفمبر 2026). الأدلة الحرفية في tools/research/notes/birth_star_1_3.json.
import os,json
D=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(D,'..','src','ai-horizon.html')
N=os.path.join(D,'..','research','notes','birth_star_1_3.json')
s=open(P,encoding='utf-8').read()
cards=json.load(open(N,encoding='utf-8'))['entries']
assert all(('\n["'+c['id']+'", ') not in s for c in cards),'already applied'
i=s.index('\n["K311", ');j=s.index('\n',i+1)
assert s[j+1:j+3]=='];',s[j+1:j+10]
s=s[:j]+''.join('\n'+json.dumps([c['id'],c['section'],c['q'],c['keywords'],c['a'],c['tag'],c['source_name']],ensure_ascii=False)+',' for c in cards)+s[j:]
k=s.index('\n/* 1.2: صفحة «طريقك إلى الفضاء» */\n');k=s.index('\n',k+1);k=s.index('\n',k+1)
s=s[:k]+'\n/* 1.3: صفحة «نجم يوم ميلادك» */\nObject.assign(SRC,'+json.dumps({c['id']:[c['url'],c['source_name']] for c in cards},ensure_ascii=False)+');'+s[k:]
for c in cards: assert len(c['a'])<=700,(c['id'],len(c['a']))
# K110 «أي الكواكب نراها بالعين المجردة؟» وK5 «كم نجمًا نستطيع رؤيته بالعين المجردة؟»: «بدون تلسكوب» و«بعيوننا» صيغتان شائعتان لـ«بالعين المجردة».
#  بدون هذا، ما إن تزيد الموسوعة معلومتين حتى يتغير وزن الكلمات قليلًا فيجيب K144 («كم كوكبًا في مجرتنا؟») عن «هل نقدر نشوف الكواكب بدون تلسكوب».
o='"كواكب بالعين المجرده نرى رؤيه الكواكب naked eye planets"'
assert s.count(o)==1
s=s.replace(o,'"كواكب بالعين المجرده نرى رؤيه الكواكب نشوف الكواكب بدون تلسكوب بدون دربيل بدون منظار naked eye planets"')
o='"عدد نجوم العين المجرده نرى رؤيه naked eye how many stars"'
assert s.count(o)==1
s=s.replace(o,'"عدد نجوم العين المجرده نرى رؤيه نشوف بعيوننا بدون تلسكوب naked eye how many stars"')
open(P,'w',encoding='utf-8').write(s);print('patch59 ok',len(cards),'entries')
