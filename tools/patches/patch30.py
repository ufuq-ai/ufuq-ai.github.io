# v1.4.2: replaces the v1.4.1 approach. On iOS 26 the visualViewport numbers around the keyboard are unreliable
# (WebKit bugs 297779 / 300523), and making the window follow them made it jump while the screen was dragged:
# the page peeked out above and below it, and a pull from the top reloaded the page.
# New approach, no measuring at all:
#  - on phones the chat takes over the screen: the page behind it is hidden (display:none), so nothing can show
#    through or scroll, and the reading position is restored on close;
#  - drags on the window don't move the screen (touch-action); only the conversation, the long-question box and the
#    suggestion row scroll, and they don't hand the scroll to the page (overscroll-behavior), so no pull-to-refresh;
#  - opening the chat on a phone no longer pops the keyboard by itself, and after an answer the keyboard stays down
#    so the answer can be read; while typing, the disclaimer hides, the suggestions fold into one row, and the
#    conversation sits right above the input.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- styles: drop the v1.4.1 keyboard-fitting rules, add phone chat mode ----------
rep('''.drawer.kb{padding-bottom:10px}
.drawer.kb .d-foot{display:none}
.drawer.kb #starter{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:none;padding-bottom:2px}
.drawer.kb #starter::-webkit-scrollbar{display:none}
.drawer.kb #starter .schip{flex:none;white-space:nowrap}''',
'''@media (max-width:560px){
  /* «اسأل أفق» on phones takes over the screen: the page behind is hidden, and drags don't move the screen */
  html.chat-on,html.chat-on body{overflow:hidden;overscroll-behavior:none;background:var(--sky)}
  html.chat-on header.top,html.chat-on #view,html.chat-on footer.foot{display:none!important}
  .drawer{touch-action:none;touch-action:pinch-zoom}
  .drawer .log{touch-action:pan-y;touch-action:pan-y pinch-zoom}
  .drawer textarea{touch-action:pan-y;overscroll-behavior:contain}
  .drawer.typing{padding-bottom:10px}
  .drawer.typing .d-foot{display:none}
  .drawer.typing .log>:first-child{margin-top:auto}
  .drawer.typing #starter{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:none;touch-action:pan-x;padding-bottom:2px}
  .drawer.typing #starter::-webkit-scrollbar{display:none}
  .drawer.typing #starter .schip{flex:none;white-space:nowrap}
}''')

# ---------- behaviour: drop visualViewport following and the body pinning ----------
rep('''/* على الجوال تغطي نافذة «اسأل أفق» الشاشة كلها: نثبّت الصفحة خلفها فلا تتحرك، ونجعل النافذة دائمًا بحجم الجزء الظاهر فوق لوحة المفاتيح. */
const VV=window.visualViewport,fullMQ=matchMedia("(max-width:560px)");let lockY=null;
function lockPage(on){
  const b=document.body.style;
  if(on&&lockY===null){lockY=scrollY;Object.assign(b,{position:"fixed",top:-lockY+"px",left:"0",right:"0",width:"100%"});}
  else if(!on&&lockY!==null){const y=lockY;lockY=null;Object.assign(b,{position:"",top:"",left:"",right:"",width:""});scrollTo(0,y);}
}
function fitDrawer(){
  if(drawer.hidden)return;
  lockPage(fullMQ.matches);
  const st=drawer.style;
  if(!VV||Math.abs(VV.scale-1)>.01){st.top=st.bottom=st.height="";drawer.classList.remove("kb");return;}
  st.top=VV.offsetTop+"px";st.bottom="auto";st.height=VV.height+"px";
  drawer.classList.toggle("kb",document.documentElement.clientHeight-VV.height>120);
}
if(VV){VV.addEventListener("resize",fitDrawer);VV.addEventListener("scroll",fitDrawer);}
if(fullMQ.addEventListener)fullMQ.addEventListener("change",fitDrawer);
function openDrawer(q){drawer.hidden=false;fab.hidden=true;fitDrawer();if(q)ask(q);else input.focus();}
function closeDrawer(){drawer.hidden=true;fab.hidden=false;const st=drawer.style;st.top=st.bottom=st.height="";drawer.classList.remove("kb");lockPage(false);fab.focus();}''',
'''/* على الجوال تأخذ «اسأل أفق» الشاشة كلها: نخفي الصفحة خلفها فلا يظهر منها شيء ولا تتحرك، ونرجعها لنفس المكان عند الإغلاق.
   ولا تنفتح لوحة المفاتيح وحدها في الجوال: تظهر عندما يضغط الزائر على مربع الكتابة، وتبقى مقفلة بعد الجواب ليقرأه. */
const fullMQ=matchMedia("(max-width:560px)");let chatY=null;
function chatMode(){
  const on=!drawer.hidden&&fullMQ.matches,H=document.documentElement;
  if(on&&chatY===null){chatY=scrollY;H.classList.add("chat-on");}
  else if(!on&&chatY!==null){const y=chatY;chatY=null;H.classList.remove("chat-on");scrollTo(0,y);}
}
if(fullMQ.addEventListener)fullMQ.addEventListener("change",chatMode);
input.addEventListener("focus",()=>drawer.classList.add("typing"));
input.addEventListener("blur",()=>{drawer.classList.remove("typing");if(chatY!==null)scrollTo(0,0);});
function refocus(){if(!fullMQ.matches)input.focus();}
function openDrawer(q){drawer.hidden=false;fab.hidden=true;chatMode();if(q)ask(q);else if(fullMQ.matches){const h=drawer.querySelector("h2");h.tabIndex=-1;h.focus({preventScroll:true});}else input.focus();}
function closeDrawer(){drawer.hidden=true;fab.hidden=false;drawer.classList.remove("typing");chatMode();fab.focus();}''')

# after an answer: refocus the input only where it doesn't pop a keyboard over the answer
rep('if(!sample){setAIOff();answerLocal(bubble,hits,q);setBusy(false);input.focus();log.scrollTop=log.scrollHeight;return;}',
    'if(!sample){setAIOff();answerLocal(bubble,hits,q);setBusy(false);refocus();log.scrollTop=log.scrollHeight;return;}')
rep('}finally{setBusy(false);input.focus();log.scrollTop=log.scrollHeight;}',
    '}finally{setBusy(false);refocus();log.scrollTop=log.scrollHeight;}')

# sending from a phone puts the keyboard down (Safari does it by itself when the box is disabled, Chrome doesn't)
rep('$("#ask-form").addEventListener("submit",e=>{e.preventDefault();const q=input.value;input.value="";autosize();ask(q);});',
    '$("#ask-form").addEventListener("submit",e=>{e.preventDefault();const q=input.value;input.value="";autosize();if(q.trim()&&fullMQ.matches)input.blur();ask(q);});')

# ---------- version 1.4.2 (fix) ----------
rep('<small class="ver">الإصدار 1.4.1 · آخر تحديث 21 نوفمبر 2026</small>','<small class="ver">الإصدار 1.4.2 · آخر تحديث 21 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch30 ok')
