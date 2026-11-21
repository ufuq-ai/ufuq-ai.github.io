# v1.5: settings (gear in the top bar).
#  - font size (4 steps): scales every rem on the page through --fs on <html>; body text moves from 17px to 1.0625rem
#  - red observing mode: html.red-mode turns on the dark palette and lays a red multiply veil over everything
#    (html.red-mode::after), so the screen keeps your eyes dark-adapted outdoors
#  - explanation level (ufuq-level) and the «سماء الليلة» city (ufuq-sky-city), gathered in one place
#  - show the «ابدأ من هنا» tour again; clear my data (every ufuq-* key, two taps, then reload)
# A tiny script before the top bar applies font size and red mode before the first paint, so nothing flashes bright.
import math
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

def gear(cx=12,cy=12,R=10.6,r=7.7,teeth=8,tip=8.5,base=14,hole=3.3):
    pts=[]
    for i in range(teeth):
        a=i*360/teeth
        for ang,rad in ((a-base,r),(a-tip,R),(a+tip,R),(a+base,r)):
            t=math.radians(ang-90)
            pts.append((cx+rad*math.cos(t),cy+rad*math.sin(t)))
    d='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+'Z'
    d+=f'M{cx+hole:.2f} {cy:.2f}A{hole} {hole} 0 1 0 {cx-hole:.2f} {cy:.2f}A{hole} {hole} 0 1 0 {cx+hole:.2f} {cy:.2f}Z'
    return d

# ---------- styles ----------
# red mode borrows the dark palette (both palettes' dark blocks)
rep(':root[data-theme="dark"]{',':root[data-theme="dark"],:root.red-mode{',count=2)
rep('body{background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:17px;line-height:1.9;direction:rtl}',
    'html{font-size:calc(100% * var(--fs,1))}\nbody{background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:1.0625rem;line-height:1.9;direction:rtl}')
rep('/* ===== AI lab ===== */','''/* ===== settings ===== */
.set-btn{flex:none;display:grid;place-items:center;width:38px;height:38px;padding:0;border-radius:50%;border:1px solid var(--sky-line);background:rgba(255,255,255,.06);color:var(--sky-fg);cursor:pointer;transition:background .2s,border-color .2s}
.set-btn:hover{border-color:var(--sky-accent);background:rgba(255,255,255,.12)}
.set-btn svg{width:20px;height:20px;transition:transform .5s}
.set-btn:hover svg{transform:rotate(45deg)}
.set{inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;background:transparent;color:var(--sky-fg);overflow:hidden;overscroll-behavior:contain;touch-action:none;touch-action:pinch-zoom}
.set[open]{display:flex;align-items:center;justify-content:center}
.set::backdrop{background:rgba(4,2,14,.66)}
.set-card{width:min(460px,calc(100% - 32px));max-height:calc(100% - 32px);overflow-y:auto;overscroll-behavior:contain;touch-action:pan-y;background:radial-gradient(100% 34% at 100% 0%,rgba(140,80,255,.38),transparent 72%),var(--sky);border:1px solid var(--sky-line);border-radius:20px;padding:16px 18px 18px;display:flex;flex-direction:column;gap:12px;box-shadow:0 24px 60px rgba(0,0,0,.5);animation:setin .22s ease-out}
@keyframes setin{from{transform:translateY(14px);opacity:0}}
@keyframes setup{from{transform:translateY(48px);opacity:.4}}
.set-head{display:flex;align-items:center;gap:10px}
.set-head h2{flex:1;margin:0;font-family:var(--f-display);font-size:1.3rem;color:#fff}
.set-sec{display:flex;flex-direction:column;gap:12px;padding-top:12px;border-top:1px solid var(--sky-line)}
.set-sec h3{margin:0;font-size:.8rem;font-weight:700;color:#ffd796}
.set-row{display:flex;align-items:center;justify-content:space-between;gap:10px 14px;flex-wrap:wrap}
.set-row>div:first-child{flex:1 1 150px;min-width:0}
.set-row b,.set-row label{display:block;font-weight:600;color:var(--sky-fg);font-size:.98rem;line-height:1.6}
.set-row small{display:block;color:var(--sky-muted);font-size:.8rem;line-height:1.7}
.set-card .seg{background:rgba(255,255,255,.08);flex-wrap:wrap}
.set-card .seg button{color:var(--sky-muted);padding:6px 13px;cursor:pointer}
.set-card .seg button[aria-pressed="true"]{color:#fff}
.set-sel{background:rgba(255,255,255,.08);color:var(--sky-fg);border:1px solid var(--sky-line);border-radius:12px;padding:8px 12px;font:inherit;font-size:.95rem;min-width:150px}
.set-sel option{color:#111;background:#fff}
.sw{position:relative;flex:none;width:52px;height:30px;padding:0;border-radius:999px;border:1px solid var(--sky-line);background:rgba(255,255,255,.12);cursor:pointer;transition:background .2s,border-color .2s}
.sw::after{content:"";position:absolute;top:3px;inset-inline-start:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.35);transition:inset-inline-start .2s}
.sw[aria-checked="true"]{background:#d32f2f;border-color:#ff6b6b}
.sw[aria-checked="true"]::after{inset-inline-start:25px}
.set-danger[data-armed]{background:#c62828;border-color:#ff6b6b;color:#fff}
.set-note{margin:0;font-size:.8rem;color:var(--sky-muted)}
.set-row small.set-tip{color:#ffd796}
html.red-mode::after{content:"";position:fixed;inset:0;background:#b30000;mix-blend-mode:multiply;pointer-events:none;z-index:2147483647}
html.red-mode .set-card{filter:url(#red-only)}
html.red-mode .set::backdrop{background:rgba(0,0,0,.72)}
html:has(.set[open]){overflow:hidden}
@media (max-width:560px){
  .top .wrap{gap:12px}
  .set[open]{align-items:flex-end}
  .set-card{width:100%;max-height:calc(100% - 20px);border-radius:22px 22px 0 0;border-bottom:0;padding-bottom:calc(20px + env(safe-area-inset-bottom,0px));animation-name:setup}
}
@media (prefers-reduced-motion:reduce){.set-card{animation:none}.set-btn svg{transition:none}}

/* ===== AI lab ===== */''')

# ---------- markup ----------
# apply saved font size and red mode before anything is drawn (no bright flash at night)
rep('<header class="top">','''<script>try{var u=JSON.parse(localStorage.getItem("ufuq-set")||"{}")||{},r=document.documentElement;if([.9,1.15,1.3].indexOf(u.fs)>-1)r.style.setProperty("--fs",u.fs);if(u.red)r.classList.add("red-mode");}catch(e){}</script>
<header class="top">''')
rep('''    </nav>
''',f'''    </nav>
    <button class="set-btn" id="set-open" type="button" aria-label="الإعدادات" title="الإعدادات" aria-haspopup="dialog"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{gear()}"/></svg></button>
''')
rep('''</aside>
''','''</aside>
<dialog class="set" id="settings" aria-labelledby="set-title">
  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><filter id="red-only" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.702 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0"/></filter></svg>
  <div class="set-card">
    <div class="set-head"><h2 id="set-title">الإعدادات</h2><button class="d-close" id="set-x" type="button" aria-label="إغلاق الإعدادات">✕</button></div>
    <section class="set-sec" aria-labelledby="set-h-read">
      <h3 id="set-h-read">القراءة</h3>
      <div class="set-row"><div><b id="set-fs-l">حجم الخط</b></div><div class="seg" id="set-fs" role="group" aria-labelledby="set-fs-l"></div></div>
      <div class="set-row"><div><b id="set-lv-l">مستوى الشرح</b><small>في صفحات المواضيع.</small></div><div class="seg" id="set-lv" role="group" aria-labelledby="set-lv-l"><button type="button" data-v="easy">مبسّط</button><button type="button" data-v="deep">متعمق</button></div></div>
    </section>
    <section class="set-sec" aria-labelledby="set-h-sky">
      <h3 id="set-h-sky">الرصد</h3>
      <div class="set-row"><div><b id="set-red-l">وضع الرصد الأحمر</b><small>أحمر خافت يحافظ على رؤية عينيك للنجوم في الظلام.</small><small class="set-tip" id="set-red-tip" hidden>خفّف سطوع شاشتك أيضًا لترى النجوم أوضح.</small></div><button class="sw" id="set-red" type="button" role="switch" aria-checked="false" aria-labelledby="set-red-l"></button></div>
      <div class="set-row"><div><label for="set-city">مدينتك</label><small>لحساب أماكن الكواكب في «سماء الليلة».</small></div><select class="set-sel" id="set-city"></select></div>
    </section>
    <section class="set-sec" aria-labelledby="set-h-data">
      <h3 id="set-h-data">بياناتك</h3>
      <div class="set-row"><div><b>جولة «ابدأ من هنا»</b><small>أعدها إلى الرئيسية من البداية.</small></div><button class="btn btn-ghost" id="set-tour" type="button">أظهرها</button></div>
      <div class="set-row"><div><b>امسح بياناتي</b><small>تقدّمك وعلاماتك ونتائجك وإعداداتك.</small></div><button class="btn btn-ghost set-danger" id="set-clear" type="button">امسح</button></div>
      <p class="set-note">كل هذا محفوظ في متصفحك فقط.</p>
    </section>
  </div>
</dialog>
''')

# ---------- behaviour ----------
# Escape with the settings open must close the settings, not the chat behind them
rep('addEventListener("keydown",e=>{if(e.key==="Escape"&&!drawer.hidden){e.preventDefault();closeDrawer();}});',
    'addEventListener("keydown",e=>{if(e.key==="Escape"&&!drawer.hidden&&!document.querySelector("dialog[open]")){e.preventDefault();closeDrawer();}});')
rep('''document.querySelectorAll("#starter .schip").forEach(c=>c.onclick=()=>ask(c.textContent));

route();
''','''document.querySelectorAll("#starter .schip").forEach(c=>c.onclick=()=>ask(c.textContent));

/* ===== الإعدادات =====
   حجم الخط والوضع الأحمر في ufuq-set، ومستوى الشرح والمدينة في مفاتيحهما القديمة. «امسح بياناتي» يمسح كل مفتاح يبدأ بـ ufuq- */
const SET_K="ufuq-set",FS=[[.9,"صغير"],[1,"عادي"],[1.15,"كبير"],[1.3,"أكبر"]];
const setDlg=$("#settings"),setFs=$("#set-fs"),setLv=$("#set-lv"),setRed=$("#set-red"),setCity=$("#set-city"),setTour=$("#set-tour"),setClear=$("#set-clear");
function setGet(){const v=store.get(SET_K,{});return v&&typeof v==="object"?v:{};}
function setFsNow(){const v=setGet().fs;return FS.some(f=>f[0]===v)?v:1;}
function applySet(){const H=document.documentElement,fs=setFsNow();
  if(fs===1)H.style.removeProperty("--fs");else H.style.setProperty("--fs",fs);
  H.classList.toggle("red-mode",!!setGet().red);}
function setSync(){const fs=setFsNow();
  [...setFs.children].forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.v===fs)));
  [...setLv.children].forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.v===topicLevel)));
  setRed.setAttribute("aria-checked",String(!!setGet().red));$("#set-red-tip").hidden=!setGet().red;
  const ci=+store.get("ufuq-sky-city",0);setCity.value=SK_CITIES[ci]?ci:0;}
function setPut(p){store.set(SET_K,Object.assign(setGet(),p));applySet();setSync();}
FS.forEach(([v,n])=>{const b=el("button",null,n);b.type="button";b.dataset.v=v;b.onclick=()=>setPut({fs:v});setFs.append(b);});
setLv.querySelectorAll("button").forEach(b=>b.onclick=()=>{
  const v=b.dataset.v,tb=[...document.querySelectorAll("#view .seg button")].find(x=>x.textContent===(v==="easy"?"مبسّط":"متعمق"));
  if(tb)tb.click();else{topicLevel=v;store.set("ufuq-level",v);}
  setSync();});
setRed.onclick=()=>setPut({red:!setGet().red});
SK_CITIES.forEach(([n],i)=>{const o=el("option",null,n);o.value=i;setCity.append(o);});
setCity.onchange=()=>{store.set("ufuq-sky-city",setCity.value);const sk=$("#sk-city");if(sk&&sk.value!==setCity.value){sk.value=setCity.value;sk.dispatchEvent(new Event("change"));}};
function setDisarm(){clearTimeout(setClear._t);delete setClear.dataset.armed;setClear.textContent="امسح";}
setClear.onclick=()=>{
  if(!setClear.dataset.armed){setClear.dataset.armed="1";setClear.textContent="متأكد؟ اضغط مرة ثانية";clearTimeout(setClear._t);setClear._t=setTimeout(setDisarm,5000);return;}
  try{[localStorage,sessionStorage].forEach(st=>Object.keys(st).filter(k=>k.startsWith("ufuq-")).forEach(k=>st.removeItem(k)));sessionStorage.setItem("ufuq-cleared","1");}catch(_){}
  location.reload();};
function setOpen(){setDisarm();setSync();if(typeof setDlg.showModal==="function")setDlg.showModal();else setDlg.setAttribute("open","");}
function setClose(){if(typeof setDlg.close==="function")setDlg.close();else setDlg.removeAttribute("open");}
setTour.onclick=()=>{store.set(TOUR_OFF,false);store.set(TOUR_K,{});setClose();
  if(location.hash&&location.hash!=="#home")location.hash="#home";else route();
  toast("رجعت جولة «ابدأ من هنا» إلى الرئيسية.");};
$("#set-open").onclick=setOpen;$("#set-x").onclick=setClose;
setDlg.addEventListener("click",e=>{if(e.target===setDlg)setClose();});
applySet();
try{if(sessionStorage.getItem("ufuq-cleared")){sessionStorage.removeItem("ufuq-cleared");setTimeout(()=>toast("مسحنا بياناتك من هذا الجهاز."),300);}}catch(_){}

route();
''')

# ---------- version 1.5 (new feature) ----------
rep('<small class="ver">الإصدار 1.4.2 · آخر تحديث 21 نوفمبر 2026</small>','<small class="ver">الإصدار 1.5 · آخر تحديث 21 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch31 ok')
