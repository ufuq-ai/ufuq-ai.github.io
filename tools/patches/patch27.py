# v1.3.1: dismissing «ابدأ من هنا» focused the search box; on iPhone that opened the keyboard and scrolled up to it.
# Now focus moves to the next section's heading (no keyboard, no scroll), and the page stays where it was.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)
rep('''sec.querySelector(".start-x").onclick=()=>{store.set(TOUR_OFF,true);const f=$("#q");sec.remove();toast("أخفينا جولة البداية.");if(f)f.focus({preventScroll:true});};''',
    '''sec.querySelector(".start-x").onclick=()=>{store.set(TOUR_OFF,true);const nx=sec.nextElementSibling&&sec.nextElementSibling.querySelector("h2");sec.remove();toast("أخفينا جولة البداية.");if(nx){nx.tabIndex=-1;nx.focus({preventScroll:true});}};''')
rep('<small class="ver">الإصدار 1.3 · آخر تحديث 20 نوفمبر 2026</small>','<small class="ver">الإصدار 1.3.1 · آخر تحديث 20 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch27 ok')
