# v1.0: the public launch (Friday 27 Nov 2026, 1:00 AM Riyadh).
#  - CHANGELOG: new top entry 1.0 «الإطلاق الرسمي» (no «قبل الإطلاق» tag; the summary now shows «تاريخ الإطلاق»)
#  - footer: version 1.0 · 27 نوفمبر 2026, and a line linking to the team's Substack publication (ufuqai.substack.com)
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('const CHANGELOG=[\n',
    '''const CHANGELOG=[
 {v:"1.0",date:"2026-11-27",title:"الإطلاق الرسمي",items:[
  "أفق الذكاء متاح للجميع: 301 معلومة فلكية موثقة، ومع كل معلومة رابط لمصدرها.",
  "صارت لأفق نشرة على سابستك، فيها جديد الموقع ومكان للنقاش، ورابطها في أسفل كل صفحة.",
  "شكرًا لكل من حلّ ألغاز «قبل الشروق» قبل الإطلاق."]},
''')
rep('<small class="ver">الإصدار 0.8.2 · آخر تحديث 24 نوفمبر 2026</small>',
    '<small class="ver">الإصدار 1.0 · آخر تحديث 27 نوفمبر 2026</small>')
rep('''    <small>المعلومات مبسطة لأغراض تعليمية، ومع كل معلومة رابط لمصدرها.</small>''',
    '''    <p class="copy">تابع جديد أفق وناقشنا في <a href="https://ufuqai.substack.com" target="_blank" rel="noopener">نشرة أفق على سابستك</a>.</p>
    <small>المعلومات مبسطة لأغراض تعليمية، ومع كل معلومة رابط لمصدرها.</small>''')
open(P,'w',encoding='utf-8').write(s);print('patch38 ok')
