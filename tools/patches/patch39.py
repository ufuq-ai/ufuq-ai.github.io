# v1.0 (same release, before the public launch): the team dropped the separate Substack publication «أفق الذكاء».
#  - footer: remove the line linking to ufuqai.substack.com (added in patch38)
#  - CHANGELOG 1.0: remove the item announcing that publication
#  - the version stays 1.0: nothing was launched yet
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''    <p class="copy">تابع جديد أفق وناقشنا في <a href="https://ufuqai.substack.com" target="_blank" rel="noopener">نشرة أفق على سابستك</a>.</p>\n''','')
rep('''  "صارت لأفق نشرة على سابستك، فيها جديد الموقع ومكان للنقاش، ورابطها في أسفل كل صفحة.",\n''','')
assert 'substack' not in s.lower(),'substack still mentioned'
open(P,'w',encoding='utf-8').write(s);print('patch39 ok')
