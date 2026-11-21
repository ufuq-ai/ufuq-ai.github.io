# v1.6 (1/3): share a fact as an image.
#  - a «شارك» button in every fact's meta row (topic pages, search results, fact of the day, «اسأل أفق» answers)
#  - it draws a 1080×1350 card (logo, topic, question, answer, source, link) and opens the phone's share sheet;
#    where sharing files isn't possible it saves the image instead (the Claude copy uses its downloads capability)
#  - direct links to one fact: https://ufuq-ai.github.io/#k-K123 (or #k-G12 for a glossary term) open that fact
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- styles ----------
rep('.meta{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:.8rem;color:var(--muted)}',
    '''.meta{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:.8rem;color:var(--muted)}
.share-btn{display:inline-flex;align-items:center;gap:5px;min-height:30px;margin-inline-start:auto;padding:3px 12px;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;font:inherit;font-size:.78rem;font-weight:600;cursor:pointer;opacity:.85;transition:opacity .2s,background .2s}
.share-btn:hover{opacity:1;background:rgba(127,127,127,.12)}
.share-btn svg{width:15px;height:15px;flex:none}
.share-btn[aria-busy="true"]{opacity:.5;cursor:progress}''')

# ---------- the button in every fact's meta row ----------
rep('''  if(e.tag) m.append(el("span",tagCls(e.tag),e.tag));
  return m;
}
let pendingOpen=null;''','''  if(e.tag) m.append(el("span",tagCls(e.tag),e.tag));
  const sb=el("button","share-btn");sb.type="button";sb.setAttribute("aria-label","شارك هذه المعلومة صورة");sb.innerHTML=SHARE_SVG+"<span>شارك</span>";
  sb.onclick=ev=>{ev.preventDefault();ev.stopPropagation();shareFact(e,sb);};m.append(sb);
  return m;
}

/* ---------- شارك المعلومة صورة ----------
   يرسم بطاقة 1080×1350 ثم يفتح نافذة المشاركة في الجوال، وإن لم تتوفر يحفظ الصورة. الرابط يفتح المعلومة نفسها (#k-رقمها). */
const SITE="https://ufuq-ai.github.io/";
const SHARE_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3"/><path d="M7 8l5-5 5 5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';
const cleanTxt=t=>String(t||"").replace(/[\\u200B\\u2060-\\u2064]/g,"");
const factLink=e=>e.custom?SITE:SITE+"#k-"+e.id;
function wrapLines(x,text,maxW,maxLines){
  const words=cleanTxt(text).split(/\\s+/).filter(Boolean),lines=[];let cur="";
  for(const w of words){const t=cur?cur+" "+w:w;if(!cur||x.measureText(t).width<=maxW)cur=t;else{lines.push(cur);cur=w;}}
  if(cur)lines.push(cur);
  if(lines.length<=maxLines)return {lines,cut:false};
  // too long: end at the last full sentence if one is close, otherwise cut with «…»
  const kept=lines.slice(0,maxLines).join(" ").split(" ");let k=kept.length-1;
  while(k>0&&!/[.؟!]$/.test(kept[k]))k--;
  if(k>=kept.length*.6){const r=wrapLines(x,kept.slice(0,k+1).join(" "),maxW,maxLines);return {lines:r.lines,cut:true};}
  const out=lines.slice(0,maxLines);let last=out[maxLines-1];
  while(last.includes(" ")&&x.measureText(last+" …").width>maxW)last=last.slice(0,last.lastIndexOf(" "));
  out[maxLines-1]=last+" …";return {lines:out,cut:true};
}
let cardLogo=null;
async function cardLogoImg(){
  if(cardLogo)return cardLogo;
  const svg=document.querySelector("svg.logo");if(!svg)return null;
  const c=svg.cloneNode(true);c.setAttribute("width","192");c.setAttribute("height","192");c.setAttribute("xmlns","http://www.w3.org/2000/svg");
  const img=new Image();img.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(new XMLSerializer().serializeToString(c));
  try{await img.decode();cardLogo=img;}catch(_){}
  return cardLogo;
}
async function factCard(e){
  const W=1080,H=1350,c=document.createElement("canvas");c.width=W;c.height=H;const x=c.getContext("2d");
  try{await Promise.race([Promise.all([document.fonts.load('700 64px Cairo'),document.fonts.load('400 42px "IBM Plex Sans Arabic"')]),new Promise(r=>setTimeout(r,800))]);}catch(_){}
  const D='Cairo,"IBM Plex Sans Arabic",Tahoma,sans-serif',B='"IBM Plex Sans Arabic",Tahoma,sans-serif',M=84,R=W-M,TW=W-2*M;
  const g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,"#0b0822");g.addColorStop(.55,"#1d1150");g.addColorStop(1,"#3a1a6e");x.fillStyle=g;x.fillRect(0,0,W,H);
  const glow=x.createRadialGradient(W*.9,0,0,W*.9,0,760);glow.addColorStop(0,"rgba(140,80,255,.42)");glow.addColorStop(1,"rgba(140,80,255,0)");x.fillStyle=glow;x.fillRect(0,0,W,H);
  let a=(parseInt(String(e.id).replace(/\\D/g,""),10)||7)*977+3;const rnd=()=>(a=(a*16807)%2147483647)/2147483647;
  for(let i=0;i<150;i++){x.globalAlpha=rnd()*.55+.15;x.fillStyle="#fff";x.beginPath();x.arc(rnd()*W,rnd()*H,rnd()*1.7+.4,0,7);x.fill();}x.globalAlpha=1;
  x.direction="rtl";x.textAlign="right";x.textBaseline="alphabetic";
  const lg=await cardLogoImg();if(lg)x.drawImage(lg,R-92,74,92,92);
  x.fillStyle="#fff";x.font=`700 46px ${D}`;x.fillText("أفق الذكاء",R-(lg?114:0),134);
  const cat=CAT_NAMES[e.c]||"";
  if(cat){x.font=`600 30px ${B}`;const cw=x.measureText(cat).width+48;x.fillStyle="rgba(196,171,255,.18)";x.beginPath();if(x.roundRect)x.roundRect(M,94,cw,56,28);else x.rect(M,94,cw,56);x.fill();x.fillStyle="#c4abff";x.textAlign="center";x.fillText(cat,M+cw/2,132);x.textAlign="right";}
  x.fillStyle="#ffd796";x.font=`700 62px ${D}`;let y=300;
  wrapLines(x,e.t,TW,4).lines.forEach(l=>{x.fillText(l,R,y);y+=92;});
  y+=4;x.strokeStyle="rgba(255,215,150,.5)";x.lineWidth=4;x.beginPath();x.moveTo(R,y);x.lineTo(R-150,y);x.stroke();y+=78;
  x.fillStyle="#ece8ff";x.font=`400 41px ${B}`;
  const ans=wrapLines(x,e.a,TW,Math.max(3,Math.floor((H-262-y)/66)+1));ans.lines.forEach(l=>{x.fillText(l,R,y);y+=66;});
  x.strokeStyle="rgba(196,171,255,.28)";x.lineWidth=2;x.beginPath();x.moveTo(M,H-176);x.lineTo(R,H-176);x.stroke();
  x.fillStyle="#d8d0ff";x.font=`500 32px ${B}`;x.fillText(e.src?"المصدر: "+cleanTxt(e.src):"من موسوعة «أفق الذكاء»",R,H-112);
  x.fillStyle="#a99fd6";x.font=`400 28px ${B}`;x.fillText(ans.cut?"أكمل القراءة في الموقع":"موسوعة عربية للفلك والفضاء",R,H-64);
  x.direction="ltr";x.textAlign="left";x.fillStyle="#c4abff";x.font=`600 32px ${B}`;x.fillText("ufuq-ai.github.io",M,H-64);
  return c;
}
async function shareFact(e,btn){
  if(btn.getAttribute("aria-busy")==="true")return;
  const name="ufuq-"+e.id+".png",title=cleanTxt(e.t),text=title+"\\nمن موسوعة «أفق الذكاء»: "+factLink(e);
  const send=async file=>{
    if(!(navigator.canShare&&navigator.canShare({files:[file]})))return false;
    try{await navigator.share({files:[file],title,text});return true;}
    catch(err){const n=err&&err.name;if(n==="AbortError")return true;if(n==="NotAllowedError"){btn._file=file;toast("الصورة جاهزة، اضغط «شارك» مرة أخرى.");return true;}return false;}
  };
  if(btn._file){const f=btn._file;btn._file=null;if(await send(f))return;}
  btn.setAttribute("aria-busy","true");
  try{
    const cv=await factCard(e);
    const blob=await new Promise((ok,no)=>cv.toBlob(b=>b?ok(b):no(new Error("jpg")),"image/jpeg",.9));
    if(await send(new File([blob],name.replace(/png$/,"jpg"),{type:"image/jpeg"})))return;
    toast(await qSaveImage(cv.toDataURL("image/png"),name)?"حفظنا صورة المعلومة في جهازك.":"تعذّر حفظ الصورة.");
  }catch(_){toast("تعذّر تجهيز الصورة. جرّب مرة أخرى.");}
  finally{btn.removeAttribute("aria-busy");}
}
let pendingOpen=null;''')

# ---------- direct link to one fact: #k-K123 / #k-G12 ----------
rep('''function route(){
  stopStars();stopStars=()=>{};''','''function route(){
  const dk=/^#k-([KG]\\d+)$/.exec(location.hash),de=dk&&KB_BY_ID[dk[1]];
  if(de){if(de.c==="glossary")glossPending=de.t;else pendingOpen=de.id;history.replaceState(null,"",de.c==="glossary"?"#glossary":"#topic-"+de.c);}
  stopStars();stopStars=()=>{};''')

# ---------- version 1.6 (new features) ----------
rep('<small class="ver">الإصدار 1.5 · آخر تحديث 21 نوفمبر 2026</small>','<small class="ver">الإصدار 1.6 · آخر تحديث 22 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch32 ok')
