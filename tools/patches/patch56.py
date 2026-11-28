# 1.2: تحسينات صغيرة في «اسأل أفق» عرفناها من الاختبار.
#  1) كلمات عامية: «يشتغل» بمعنى «يعمل»، و«راح/يروح» بمعنى «ذهب/وصل/زار» (KSYN).
#     ظهرتا في ask.js («كيف يشتغل التليسكوب»، «هل احد راح المريخ»)، وهما من أشيع كلام الناس.
#  2) الأرقام من خانة واحدة لا تُحذف من السؤال بعد الآن: كان ktoks يحذف كل كلمة من حرف واحد،
#     فصار «أرتميس 3» مثل «أرتميس 2»، و«فالكون 9» مثل «فالكون».
#  3) كتابات اسم «هوكينغ» (هوكينج، هوكنج، هوكنغ) كلمات بمعنى واحد: كانت «هوكنج» في كلمات K242 وحدها.
#  قيس بأسئلة جديدة كُتبت قبل التعديل (في ask.js مجموعة CHECK2).
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','ai-horizon.html')
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)
rep(''' "ينخسف انخسف خسوف","ينكسف انكسف كسوف",''',''' "ينخسف انخسف خسوف","ينكسف انكسف كسوف",
 "يشتغل تشتغل اشتغل شغال يعمل تعمل",
 "راح راحت راحوا يروح تروح يروحون رحت ذهب ذهبت ذهبوا يذهب وصل وصلت وصلوا زار زارت",
 // كتابات أسماء الأعلام
 "هوكينغ هوكينج هوكنج هوكنغ",''')
# الأرقام من خانة واحدة تبقى
rep('''.filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1);}''','''.filter(w=>w&&!KSTOP.has(w)).map(kstem).filter(w=>w.length>1||/^\\d$/.test(w));}''')
rep('''  const kept=[...new Set(raw.filter(w=>!KSTOP.has(w)).map(kstem).filter(w=>w.length>1))];''','''  const kept=[...new Set(raw.filter(w=>!KSTOP.has(w)).map(kstem).filter(w=>w.length>1||/^\\d$/.test(w)))];''')
open(P,'w',encoding='utf-8').write(s);print('patch56 ok')
