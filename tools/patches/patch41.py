# v1.0 (launch night): remove the school name everywhere, and put Khalid's name before Turki's.
# حُذف اسم المدرسة من هذا الملف نفسه بطلب خالد (نوفمبر 2026)، وحلّ محله «اسم المدرسة». النص الأصلي في تاريخ git (b5fdf43).
import re
def fix(path, reps, regex=()):
    s=open(path,encoding='utf-8').read()
    for o,n,c in reps:
        assert s.count(o)==c,(path,s.count(o),o[:60]); s=s.replace(o,n)
    for pat,n,c in regex:
        s,k=re.subn(pat,n,s); assert k==c,(path,k,pat)
    open(path,'w',encoding='utf-8').write(s)
SRC='/home/claude/ai-horizon.html'
fix(SRC,[
 ('    <p class="school">«اسم المدرسة»</p>\n','',1),
 ('، «اسم المدرسة». جميع','. جميع',1),
 ('مشروع طلابي · «اسم المدرسة»','مشروع طلابي',1),
 ('x.fillText("«اسم المدرسة»",800,985);','',1),
 ('، طالبان في «اسم المدرسة».','.',1),
 ('تركي عبدالكريم الدغيمان وخالد يزيد العنزي','خالد يزيد العنزي وتركي عبدالكريم الدغيمان',4),
],[(r'(<div class="team">)(<div><b>تركي عبدالكريم الدغيمان</b>.*?</div>)(<div><b>خالد يزيد العنزي</b>.*?</div>)',r'\1\3\2',1)])
s=open(SRC,encoding='utf-8').read(); assert '«اسم المدرسة»' not in s; assert 'تركي عبدالكريم الدغيمان وخالد' not in s
print('src ok')
