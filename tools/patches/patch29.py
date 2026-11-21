# v1.4.1: on iPhone, opening «اسأل أفق» and tapping the input raised the keyboard, which pushed the whole window up:
# its header left the screen and the home page showed (and scrolled) in a gap under it.
# Now, when the window covers the screen (phones), the page behind is pinned in place, and the window always matches
# the part of the screen above the keyboard (visualViewport). While the keyboard is up, the disclaimer hides and the
# starter suggestions fold into one row that scrolls sideways, so the conversation keeps room on small phones.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- styles ----------
rep('.log{flex:1;min-height:0;overflow-y:auto;display:flex;',
    '.log{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;display:flex;')
rep('.d-foot{font-size:.75rem;color:var(--sky-muted);line-height:1.7}',
    '.d-foot{font-size:.75rem;color:var(--sky-muted);line-height:1.7}\n.drawer.kb{padding-bottom:10px}\n.drawer.kb .d-foot{display:none}\n'
    '.drawer.kb #starter{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;scrollbar-width:none;padding-bottom:2px}\n'
    '.drawer.kb #starter::-webkit-scrollbar{display:none}\n.drawer.kb #starter .schip{flex:none;white-space:nowrap}')

# ---------- behaviour ----------
rep('''function openDrawer(q){drawer.hidden=false;fab.hidden=true;if(q)ask(q);else input.focus();}
function closeDrawer(){drawer.hidden=true;fab.hidden=false;fab.focus();}''',
'''/* على الجوال تغطي نافذة «اسأل أفق» الشاشة كلها: نثبّت الصفحة خلفها فلا تتحرك، ونجعل النافذة دائمًا بحجم الجزء الظاهر فوق لوحة المفاتيح. */
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
function closeDrawer(){drawer.hidden=true;fab.hidden=false;const st=drawer.style;st.top=st.bottom=st.height="";drawer.classList.remove("kb");lockPage(false);fab.focus();}''')

# opening a topic from an answer: close first (this restores the page), then navigate, so the page lands on the topic
rep('a.onclick=ev=>{ev.preventDefault();goTo(e);if(innerWidth<560)closeDrawer();};',
    'a.onclick=ev=>{ev.preventDefault();if(fullMQ.matches)closeDrawer();goTo(e);};')

# ---------- version 1.4.1 (fix) ----------
rep('<small class="ver">الإصدار 1.4 · آخر تحديث 21 نوفمبر 2026</small>','<small class="ver">الإصدار 1.4.1 · آخر تحديث 21 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch29 ok')
