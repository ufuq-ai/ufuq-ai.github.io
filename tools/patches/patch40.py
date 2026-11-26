# v1.0 (same release, before the public launch): visit counting on the public site.
#  - the counter itself (GoatCounter) is added by tools/build_public.py to index.html only
#  - here: a privacy line in the «الحقوق وشروط الاستخدام» card on #about
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('''          <li>المعلومات العلمية مأخوذة من المصادر المذكورة مع كل معلومة، وحقوق تلك المصادر لأصحابها.</li>
        </ul>''',
    '''          <li>المعلومات العلمية مأخوذة من المصادر المذكورة مع كل معلومة، وحقوق تلك المصادر لأصحابها.</li>
          <li><b>الخصوصية:</b> نعدّ زيارات الموقع وأكثر صفحاته زيارة بأداة GoatCounter، دون ملفات تعريف الارتباط (الكوكيز)، ودون أن تُحفظ أي بيانات شخصية عن الزائر.</li>
        </ul>''')
open(P,'w',encoding='utf-8').write(s);print('patch40 ok')
