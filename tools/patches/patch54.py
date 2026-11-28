# 1.2: معلومتان لصفحة «طريقك إلى الفضاء» (K310 شروط وكالة الفضاء الأوروبية، K311 برنامج الإمارات لرواد الفضاء).
#  كل جملة منقولة من صفحة المصدر بعد فتحها (28 نوفمبر 2026). الأدلة الحرفية في tools/research/notes/space_path_1_2.json.
import os,json
D=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(D,'..','src','ai-horizon.html')
N=os.path.join(D,'..','research','notes','space_path_1_2.json')
s=open(P,encoding='utf-8').read()
cards=json.load(open(N,encoding='utf-8'))['entries']
assert all(('\n["'+c['id']+'", ') not in s for c in cards),'already applied'
i=s.index('\n["K309", ');j=s.index('\n',i+1)
assert s[j+1:j+3]=='];',s[j+1:j+10]
s=s[:j]+''.join('\n'+json.dumps([c['id'],c['section'],c['q'],c['keywords'],c['a'],c['tag'],c['source_name']],ensure_ascii=False)+',' for c in cards)+s[j:]
k=s.index('\n/* 1.1: معلومات من أسئلة الناس الحقيقية (Quora العربي) */\n');k=s.index('\n',k+1);k=s.index('\n',k+1)
s=s[:k]+'\n/* 1.2: صفحة «طريقك إلى الفضاء» */\nObject.assign(SRC,'+json.dumps({c['id']:[c['url'],c['source_name']] for c in cards},ensure_ascii=False)+');'+s[k:]
for c in cards: assert len(c['a'])<=700,(c['id'],len(c['a']))
open(P,'w',encoding='utf-8').write(s);print('patch54 ok',len(cards),'entries')
