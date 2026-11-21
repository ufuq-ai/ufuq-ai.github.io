# v1.6 (2/3): «أضف إلى تقويمك» on sky events.
#  - buttons: every upcoming event in «أحداث قادمة», the 2027 eclipse countdown card, under «حدث الأسبوع»,
#    and on the Saudi page under the eclipse countdown
#  - iPhone/iPad: opens the real calendar file the build publishes in cal/ (Safari ignores files made in the page),
#    Android: Google Calendar, computers: downloads an .ics,
#    the Claude copy: saves the .ics through its downloads capability. Each event carries a reminder
#    (1 hour before; 9 am on the day for all-day events like «حدث الأسبوع»).
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- styles ----------
rep('.share-btn[aria-busy="true"]{opacity:.5;cursor:progress}','''.share-btn[aria-busy="true"]{opacity:.5;cursor:progress}
.cal-btn{display:inline-flex;align-items:center;gap:6px;min-height:32px;margin-top:8px;padding:4px 13px;border-radius:999px;border:1px solid currentColor;background:transparent;color:var(--accent);font:inherit;font-size:.82rem;font-weight:600;cursor:pointer;transition:background .2s}
.cal-btn svg{width:16px;height:16px;flex:none}
.cal-btn:hover{background:var(--accent-soft)}
.wk-cal{display:flex;justify-content:center;margin-top:10px}
.sa-cal{margin-top:16px}
.wk-cal .cal-btn,.sa-cal .cal-btn{color:var(--sky-accent);margin-top:0}
.wk-cal .cal-btn:hover,.sa-cal .cal-btn:hover{background:rgba(196,171,255,.14)}''')

# ---------- helpers ----------
rep('const upcoming=()=>allEvents().filter(e=>e.d.getTime()>Date.now());','''const upcoming=()=>allEvents().filter(e=>e.d.getTime()>Date.now());

/* ---------- أضف إلى تقويمك ----------
   ev={t,note,d:Date} لحدث بوقت، أو {t,note,day:"YYYY-MM-DD"} لحدث يوم كامل، و hash لرابط الحدث في الموقع.
   آيفون وآيباد: ملف .ics يفتح في تقويم آبل. أندرويد: تقويم Google. الكمبيوتر: تنزيل ملف .ics. نسخة Claude: حفظ الملف. */
const CAL_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg>';
const z2=n=>String(n).padStart(2,"0");
const icsUTC=d=>d.getUTCFullYear()+z2(d.getUTCMonth()+1)+z2(d.getUTCDate())+"T"+z2(d.getUTCHours())+z2(d.getUTCMinutes())+"00Z";
const icsDay=(y,m,d)=>{const t=new Date(Date.UTC(y,m-1,d));return t.getUTCFullYear()+z2(t.getUTCMonth()+1)+z2(t.getUTCDate());};
const icsTxt=t=>cleanTxt(t).replace(/\\\\/g,"\\\\\\\\").replace(/\\r?\\n/g,"\\\\n").replace(/([,;])/g,"\\\\$1");
function icsFold(line){const enc=new TextEncoder(),out=[];let cur="",n=0,lim=75;for(const ch of line){const b=enc.encode(ch).length;if(n+b>lim){out.push(cur);cur="";n=0;lim=74;}cur+=ch;n+=b;}out.push(cur);return out.join("\\r\\n ");}
function calSpan(ev){
  if(ev.day){const [y,m,d]=ev.day.split("-").map(Number);return [icsDay(y,m,d),icsDay(y,m,d+1)];}
  return [icsUTC(ev.d),icsUTC(new Date(ev.d.getTime()+(ev.mins||60)*6e4))];
}
// the file name the build uses: the event's date in Saudi time (cal/YYYYMMDD.ics)
const calKey=ev=>ev.day?ev.day.replace(/-/g,""):ev.d.toLocaleDateString("en-CA",{timeZone:"Asia/Riyadh"}).replace(/-/g,"");
function calICS(ev){
  const [a,b]=calSpan(ev),link=SITE+(ev.hash||""),uid=[...(cleanTxt(ev.t)+a)].reduce((h,c)=>(h*31+c.charCodeAt(0))>>>0,7).toString(36);
  return ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Ufuq AI//Arabic//AR","CALSCALE:GREGORIAN","METHOD:PUBLISH","BEGIN:VEVENT",
    "UID:"+uid+"-"+a+"@ufuq-ai.github.io","DTSTAMP:"+icsUTC(new Date()),
    (ev.day?"DTSTART;VALUE=DATE:":"DTSTART:")+a,(ev.day?"DTEND;VALUE=DATE:":"DTEND:")+b,
    "SUMMARY:"+icsTxt(ev.t),"DESCRIPTION:"+icsTxt((ev.note?ev.note+"\\n\\n":"")+"من «أفق الذكاء»: "+link),"URL:"+link,
    "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:"+icsTxt(ev.t),"TRIGGER:"+(ev.day?"PT9H":"-PT1H"),"END:VALARM",
    "END:VEVENT","END:VCALENDAR"].map(icsFold).join("\\r\\n")+"\\r\\n";
}
async function addToCal(ev){
  const ics=calICS(ev),name="ufuq-"+calSpan(ev)[0].slice(0,8)+".ics",ua=navigator.userAgent;
  let dl=null;try{dl=await Promise.race([use("downloads"),new Promise(r=>setTimeout(()=>r(null),1200))]);}catch(_){}
  if(dl){try{await dl.save({filename:name,data:new Blob([ics],{type:"text/calendar"})});toast("حفظنا ملف الحدث. افتحه ليُضاف إلى تقويمك.");}catch(e){if(!(e&&e.code==="declined"))toast("تعذّر حفظ ملف الحدث.");}return;}
  if(/Android/i.test(ua)){const [a,b]=calSpan(ev);
    window.open("https://calendar.google.com/calendar/render?action=TEMPLATE&text="+encodeURIComponent(cleanTxt(ev.t))+"&dates="+a+"/"+b+"&details="+encodeURIComponent((ev.note?cleanTxt(ev.note)+"\\n\\n":"")+SITE+(ev.hash||"")),"_blank","noopener");return;}
  if(/iPhone|iPad|iPod/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1)){
    // Safari on iPhone ignores calendar files made inside the page, so open the real file the build publishes in cal/
    const u=SITE+"cal/"+calKey(ev)+".ics";
    if(window.top!==window||navigator.standalone===true||matchMedia("(display-mode: standalone)").matches)window.open(u,"_blank");else location.href=u;
    return;}
  const u=URL.createObjectURL(new Blob([ics],{type:"text/calendar"})),a=document.createElement("a");a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),5000);
  toast("حفظنا ملف الحدث في جهازك. افتحه ليُضاف إلى تقويمك.");
}
function calBtn(ev){const b=el("button","cal-btn");b.type="button";b.innerHTML=CAL_SVG+"<span>أضف إلى تقويمك</span>";b.setAttribute("aria-label","أضف «"+cleanTxt(ev.t)+"» إلى تقويمك");b.onclick=e=>{e.preventDefault();e.stopPropagation();addToCal(ev);};return b;}''')

# ---------- «أحداث قادمة»: every upcoming event ----------
rep('const what=el("div");what.append(el("b",null,e.t),el("p",null,e.note));r.append(when,what);ul.append(r);});',
    'const what=el("div");what.append(el("b",null,e.t),el("p",null,e.note));if(!past)what.append(calBtn({t:e.t,note:e.note,d:e.d,hash:e.big?"#saudi":"#tools"}));r.append(when,what);ul.append(r);});')

# ---------- eclipse countdown card: the countdown repaints every 30 s, the button stays outside it ----------
rep('const evs=allEvents(),big=evs.find(e=>e.big),te=$("#t-eclipse");',
    'const evs=allEvents(),big=evs.find(e=>e.big),teBox=$("#t-eclipse"),te=el("div");teBox.replaceChildren(te);\n  if(big&&big.d.getTime()>Date.now())teBox.append(calBtn({t:big.t,note:big.note,d:big.d,hash:"#saudi"}));')

# ---------- «حدث الأسبوع»: a calendar link under the strip (the strip itself is a button) ----------
rep('''  if(e)b.onclick=()=>goTo(e);
  box.replaceWith(b);
}''','''  if(e)b.onclick=()=>goTo(e);
  box.replaceWith(b);
  if(!past){const w=el("div","wk-cal");w.append(calBtn({t:E.title,note:E.note,day:E.date,hash:E.entry?"#k-"+E.entry:""}));b.after(w);}
}''')

# ---------- Saudi page: under the eclipse countdown ----------
rep('''        <div><b>${daysLeft.toLocaleString("en-US")}</b><span>يومًا على الكسوف الكلي</span></div>
      </div>''','''        <div><b>${daysLeft.toLocaleString("en-US")}</b><span>يومًا على الكسوف الكلي</span></div>
      </div>
      <div class="sa-cal" id="sa-cal"></div>''')
rep('''  /* timeline */
  const tl=$("#sa-tl");''','''  const saCal=$("#sa-cal");if(saCal&&big&&big.d.getTime()>Date.now())saCal.append(calBtn({t:big.t,note:big.note,d:big.d,hash:"#saudi"}));
  /* timeline */
  const tl=$("#sa-tl");''')
open(P,'w',encoding='utf-8').write(s);print('patch33 ok')
