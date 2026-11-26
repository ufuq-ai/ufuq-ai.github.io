# v1.0.1: the «اسأل أفق» send button did not send on the first click/tap.
#  Cause: pressing the button blurs the question box, the blur handler removes .typing from the drawer,
#  the layout shifts (footer note reappears), so the release lands outside the button and no click fires.
#  Fix: mousedown on the send/stop buttons and the starter chips keeps focus in the box (preventDefault),
#  so nothing moves until the click has happened. Enter still works as before.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)
rep('''input.addEventListener("blur",()=>{drawer.classList.remove("typing");if(chatY!==null)scrollTo(0,0);});''',
    '''input.addEventListener("blur",()=>{drawer.classList.remove("typing");if(chatY!==null)scrollTo(0,0);});
drawer.addEventListener("mousedown",e=>{if(document.activeElement===input&&e.target.closest("#send-btn,#stop-btn,#starter .schip"))e.preventDefault();});''')
rep(''' {v:"1.0",date:"2026-11-27",title:"الإطلاق الرسمي",items:[
  "أفق الذكاء متاح للجميع: 301 معلومة فلكية موثقة، ومع كل معلومة رابط لمصدرها.",
  "شكرًا لكل من حلّ ألغاز «قبل الشروق» قبل الإطلاق."]},''',
    ''' {v:"1.0",date:"2026-11-27",title:"الإطلاق الرسمي",items:[
  "أفق الذكاء متاح للجميع: 301 معلومة فلكية موثقة، ومع كل معلومة رابط لمصدرها.",
  "شكرًا لكل من حلّ ألغاز «قبل الشروق» قبل الإطلاق."],
  fixes:[{v:"1.0.1",date:"2026-11-27",text:"إصلاح: زر الإرسال في «اسأل أفق» صار يرسل سؤالك من أول ضغطة."}]},''')
rep('<small class="ver">الإصدار 1.0 · آخر تحديث 27 نوفمبر 2026</small>','<small class="ver">الإصدار 1.0.1 · آخر تحديث 27 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch42 ok')
