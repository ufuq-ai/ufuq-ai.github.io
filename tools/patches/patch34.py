# v1.6 (3/3): install the site on the phone, and say when it runs offline.
#  - settings › الرصد: «ثبّت أفق على جوالك» (only on the public site, which has manifest.webmanifest and sw.js):
#    Android/desktop Chrome shows its install prompt; iPhone shows how (Share › Add to Home Screen); once installed it says so
#  - when the internet drops while sw.js serves the site, a short note says it keeps working from the saved copy
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('<div class="set-row"><div><label for="set-city">مدينتك</label><small>لحساب أماكن الكواكب في «سماء الليلة».</small></div><select class="set-sel" id="set-city"></select></div>',
    '''<div class="set-row"><div><label for="set-city">مدينتك</label><small>لحساب أماكن الكواكب في «سماء الليلة».</small></div><select class="set-sel" id="set-city"></select></div>
      <div class="set-row" id="set-app-row" hidden><div><b>ثبّت أفق على جوالك</b><small id="set-app-note">يعمل بعدها دون إنترنت، حتى وأنت ترصد في البر.</small></div><button class="btn btn-ghost" id="set-app" type="button">ثبّت</button></div>''')
rep('function setOpen(){setDisarm();setSync();','function setOpen(){setDisarm();setSync();appSync();')
rep('''applySet();
try{if(sessionStorage.getItem("ufuq-cleared"))''','''/* ثبّت أفق: في الموقع العام فقط (فيه manifest.webmanifest و sw.js) */
let installEvt=null;
addEventListener("beforeinstallprompt",ev=>{ev.preventDefault();installEvt=ev;appSync();});
addEventListener("appinstalled",()=>{installEvt=null;appSync();toast("ثُبّت «أفق» على جهازك.");});
function appSync(){
  const row=$("#set-app-row"),btn=$("#set-app"),note=$("#set-app-note");if(!row)return;
  row.hidden=!document.querySelector('link[rel="manifest"]');if(row.hidden)return;
  if(matchMedia("(display-mode: standalone)").matches||navigator.standalone===true){btn.hidden=true;note.textContent="مثبّت على جهازك، ويعمل دون إنترنت.";return;}
  const ios=/iPhone|iPad|iPod/.test(navigator.userAgent)||(/Macintosh/.test(navigator.userAgent)&&navigator.maxTouchPoints>1);
  btn.hidden=false;btn.textContent=installEvt?"ثبّت":"كيف؟";note.textContent="يعمل بعدها دون إنترنت، حتى وأنت ترصد في البر.";
  btn.onclick=async()=>{
    if(installEvt){const e=installEvt;installEvt=null;e.prompt();try{await e.userChoice;}catch(_){}appSync();return;}
    note.textContent=ios?"في سفاري: افتح زر المشاركة (قد يكون داخل زر «…»)، ثم اختر «إضافة إلى الشاشة الرئيسية».":"من قائمة المتصفح اختر «تثبيت» أو «إضافة إلى الشاشة الرئيسية».";
  };
}
/* إذا انقطع الإنترنت والموقع محفوظ في الجهاز */
const swOn=()=>!!(navigator.serviceWorker&&navigator.serviceWorker.controller);
addEventListener("offline",()=>{if(swOn())toast("انقطع الإنترنت، و«أفق» يعمل من النسخة المحفوظة في جهازك.");});
addEventListener("online",()=>{if(swOn())toast("عاد الإنترنت.");});
if(navigator.onLine===false&&swOn())setTimeout(()=>toast("أنت دون إنترنت الآن، وتتصفح النسخة المحفوظة."),600);
applySet();
try{if(sessionStorage.getItem("ufuq-cleared"))''')
open(P,'w',encoding='utf-8').write(s);print('patch34 ok')
