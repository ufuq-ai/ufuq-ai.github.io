/* ---------- rocket workshop page ---------- */
const RW_KEY="ufuq-rw";
const RW_CATS=[["eng","المحركات"],["tank","الخزانات"],["str","الفواصل والأغطية"],["pay","الحمولات"],["extra","إضافات"]];
function rwLoad(){const s=store.get(RW_KEY,{})||{};return {mission:s.mission||"m1",stars:s.stars||{},builds:s.builds||{},legs:s.legs||{},goal:s.goal||"orbit"};}
const rwStars=n=>"★".repeat(n)+"☆".repeat(3-n);
const rwT=t=>{t=Math.max(0,Math.round(t));const h=Math.floor(t/3600),m=Math.floor(t%3600/60),s=t%60,p=x=>String(x).padStart(2,"0");return h?`${h}:${p(m)}:${p(s)}`:`${p(m)}:${p(s)}`;};
const rwNum=(n,d)=>Number(n).toLocaleString("en-US",{maximumFractionDigits:d||0,minimumFractionDigits:d||0});
function rwImg(svg){return new Promise(res=>{const im=new Image();im.onload=()=>res(im);im.onerror=()=>res(null);im.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg);});}
function renderWorkshop(){
  setNav("tools");
  view.innerHTML=`
  <section class="page-head" style="--h:${HUE.exploration}"><div class="wrap">
    <div class="crumb"><a href="#tools">جرّب</a> / ورشة الصواريخ</div>
    <h1>ورشة الصواريخ</h1>
    <p class="muted">ركّب صاروخك قطعة قطعة على المنصة، ثم أطلقه وتابع رحلته لحظة بلحظة: هل يرتفع؟ هل يصل إلى الفضاء؟ هل يدخل المدار أو ينطلق إلى القمر؟</p>
  </div></section>
  <section class="wrap rw" id="rw">
    <svg class="rw-defs" aria-hidden="true" focusable="false" width="0" height="0">${RW_DEFS}</svg>
    <div class="rw-missions" id="rw-missions" role="group" aria-label="المهمات"></div>
    <div class="rw-brief" id="rw-brief"></div>
    <div class="lab-card rw-shop" id="rw-shop">
      <div class="rw-grid">
        <div class="rw-palette"><div class="step-h"><span class="step-n">1</span><h3>القطع</h3></div><div class="seg rw-tabs" id="rw-tabs" role="group" aria-label="أنواع القطع"></div><div class="rw-items" id="rw-items"></div><p class="lab-note" id="rw-hint"></p></div>
        <div class="rw-bay-wrap"><div class="step-h"><span class="step-n">2</span><h3>منصة التركيب</h3></div><div class="rw-bay" id="rw-bay"></div><div class="rw-tools" id="rw-tools"></div></div>
        <div class="rw-panel"><div class="step-h"><span class="step-n">3</span><h3>افحص ثم أطلق</h3></div><div id="rw-panel"></div></div>
      </div>
    </div>
    <div class="lab-card rw-flight" id="rw-flight" hidden>
      <div class="rw-fl-head"><b id="rw-fl-title"></b><div class="rw-ctrl"><button class="btn btn-ghost" id="rw-pause" type="button">إيقاف مؤقت</button><span class="seg" id="rw-speed" role="group" aria-label="سرعة العرض"><button type="button" data-v="1" aria-pressed="true">×1</button><button type="button" data-v="2" aria-pressed="false">×2</button><button type="button" data-v="4" aria-pressed="false">×4</button></span><button class="btn btn-ghost" id="rw-snd" type="button" aria-pressed="true">الصوت: يعمل</button><button class="btn btn-ghost" id="rw-skip" type="button">تخطَّ إلى النتيجة</button></div></div>
      <div class="rw-stage" id="rw-stage">
        <canvas id="rw-cv" aria-hidden="true"></canvas>
        <div class="rw-hud"><div class="rw-clock" id="rw-clock">T−00:05</div><div class="rw-tel"><span>الارتفاع<b id="rw-alt">0 كم</b></span><span>السرعة<b id="rw-vel">0 كم/ث</b></span><span>المرحلة<b id="rw-stg">1</b></span></div><div class="rw-fuel" title="الوقود المتبقي في المرحلة الحالية"><span>الوقود</span><i><b id="rw-fuel"></b></i></div></div>
        <ol class="rw-log" id="rw-log" aria-live="polite"></ol>
        <canvas class="rw-mini" id="rw-mini" aria-hidden="true"></canvas>
        <div class="rw-big" id="rw-big"></div>
      </div>
      <div class="rw-result" id="rw-result" hidden></div>
    </div>
    <div class="card rw-learn">
      <span class="kick">كيف تُحسب؟</span>
      <details><summary>الدفع والوزن</summary><p>كي يرتفع الصاروخ يجب أن يدفعه محركه إلى الأعلى بقوة أكبر من وزنه. نقسم الدفع على الوزن: إذا كان الناتج أقل من 1 لا يتحرك الصاروخ، وإذا كان قريبًا من 1 يصعد ببطء ويضيع كثيرًا من وقوده في مقاومة الجاذبية. والصواريخ الحقيقية تبدأ عادة بين 1.2 و1.6.</p></details>
      <details><summary>التغير في السرعة (Δv)</summary><p>هو أقصى ما يستطيع الصاروخ أن يزيده من سرعته بوقوده، وتحسبه «معادلة الصاروخ» لكل مرحلة: كلما زاد الوقود مقارنة بالكتلة الفارغة، وكانت غازات المحرك أسرع، زادت Δv. ثم نطرح نحو 1.5 كم/ث تضيع في مقاومة الجاذبية والهواء أثناء الصعود.</p></details>
      <details><summary>لماذا المراحل؟</summary><p>حين ينفد وقود المرحلة الأولى يرمي الصاروخ خزاناتها ومحركاتها الفارغة، فيصبح أخف بكثير، وتزيد المرحلة الثانية سرعته بوقود أقل. لهذا تصل الصواريخ ذات المرحلتين إلى المدار، ولا تصل إليه غالبًا ذات المرحلة الواحدة.</p></details>
      <p class="legend">الورشة لعبة تعليمية بأرقام تقريبية مبسطة لصواريخ تحرق الكيروسين مع الأكسجين السائل، مستوحاة من صاروخ فالكون 9. السرعة المدارية نحو 7.8 كم/ث، والانطلاق من المدار نحو القمر يحتاج نحو 3.1 كم/ث إضافية. ومسار الرحلة والأرقام أثناءها تقريبية للتوضيح. ويُعرض الإطلاق مسرّعًا بعد الثواني الأولى، والساعة في أعلى الشاشة تعرض الزمن الحقيقي للرحلة.</p>
    </div>
  </section>`;
  let S=rwLoad(),tab=store.get("ufuq-rw-tab","eng"),sel=null,flight=null,lastAdd=-1;const hist=[];
  const mission=()=>S.mission==="free"?{id:"free",n:"تجربة حرة",goal:S.goal,pay:null}:RW_MISSIONS.find(m=>m.id===S.mission)||RW_MISSIONS[0];
  const stackOf=()=>{const k=S.mission;if(!S.builds[k])S.builds[k]=[];return S.builds[k];};
  const legsOn=()=>!!S.legs[S.mission];
  const save=()=>store.set(RW_KEY,S);
  const unlocked=i=>i===0||(S.stars[RW_MISSIONS[i-1].id]||0)>0;
  function missions(){
    const box=$("#rw-missions");box.replaceChildren();
    RW_MISSIONS.forEach((m,i)=>{const b=el("button","rw-m");b.type="button";const st=S.stars[m.id]||0,lock=!unlocked(i);
      b.setAttribute("aria-pressed",String(S.mission===m.id));b.disabled=lock;
      b.append(el("span","rw-mn",String(i+1)),el("b",null,m.n),el("small",lock?"rw-lock":"rw-st",lock?"مقفلة":rwStars(st)));
      b.setAttribute("aria-label",`المهمة ${i+1}: ${m.n}${lock?"، مقفلة حتى تنجح في السابقة":"، النجوم "+st+" من 3"}`);
      b.onclick=()=>{S.mission=m.id;sel=null;save();all();};box.append(b);});
    const f=el("button","rw-m rw-free");f.type="button";f.setAttribute("aria-pressed",String(S.mission==="free"));f.append(el("span","rw-mn","∞"),el("b",null,"تجربة حرة"),el("small","rw-st","بلا شروط"));
    f.onclick=()=>{S.mission="free";sel=null;save();all();};box.append(f);
  }
  function brief(){
    const M=mission(),b=$("#rw-brief");b.replaceChildren();
    if(M.id==="free"){
      b.append(el("b",null,"تجربة حرة: ركّب ما تشاء واختر هدفك"));
      const seg=el("div","seg");seg.setAttribute("role","group");seg.setAttribute("aria-label","الهدف");
      Object.entries(RW_GOALS).forEach(([k,n])=>{const x=el("button",null,n);x.type="button";x.setAttribute("aria-pressed",String(S.goal===k));x.onclick=()=>{S.goal=k;save();brief();panel();};seg.append(x);});
      const f9=el("button","btn btn-line","ابدأ من تصميم يشبه فالكون 9");f9.type="button";f9.onclick=()=>{push();S.builds.free=["e9","t3","t3","dc","ev","t2","p4"];S.legs.free=false;sel=null;save();bay();panel();};
      b.append(seg,f9);return;
    }
    const i=RW_MISSIONS.indexOf(M);
    b.append(el("span","kick",`المهمة ${i+1} من ${RW_MISSIONS.length}`),el("h3",null,M.n),el("p",null,M.brief));
    const req=el("div","rw-req");
    req.append(el("span",null,"الحمولة: "+RW_PARTS[M.pay].n),el("span",null,"الهدف: "+RW_GOALS[M.goal]));if(M.legs)req.append(el("span",null,"مع أرجل الهبوط"));
    req.append(el("span","rw-sts",`★ نجاح · ★★ كتلة الإقلاع حتى ${rwNum(M.m2)} طن · ★★★ حتى ${rwNum(M.m3)} طن`));
    b.append(req,el("p","muted rw-tip","نصيحة: "+M.tip));
  }
  function tabs(){
    const t=$("#rw-tabs");t.replaceChildren();
    RW_CATS.forEach(([k,n])=>{const b=el("button",null,n);b.type="button";b.setAttribute("aria-pressed",String(tab===k));b.onclick=()=>{tab=k;store.set("ufuq-rw-tab",k);tabs();items();};t.append(b);});
  }
  function items(){
    const box=$("#rw-items"),M=mission();box.replaceChildren();
    if(tab==="extra"){
      const b=el("button","rw-item");b.type="button";b.setAttribute("aria-pressed",String(legsOn()));
      const th=el("span","rw-th");th.innerHTML=rwLegsThumb();
      b.append(th,el("b",null,RW_LEGS.n),el("small",null,legsOn()?"مركّبة على المرحلة الأولى. اضغط لإزالتها":"2 طن · تحجز 10% من وقود المرحلة الأولى"));
      b.title=RW_LEGS.d;b.onclick=()=>{push();S.legs[S.mission]=!legsOn();save();items();bay();panel();};box.append(b);
      box.append(el("p","lab-note",RW_LEGS.d));return;
    }
    Object.entries(RW_PARTS).filter(([,P])=>P.cat===tab).forEach(([id,P])=>{
      const b=el("button","rw-item");b.type="button";
      const th=el("span","rw-th");th.innerHTML=rwThumb(id);
      const stat=P.cat==="eng"?(P.vac?`في الفضاء ${rwNum(P.thr)} كيلونيوتن · ${P.m} طن`:`دفع ${rwNum(P.thr)} كيلونيوتن · ${P.m} طن`):P.cat==="tank"?`وقود ${P.prop} طن · فارغ ${P.m} طن`:`${P.m} طن`;
      b.append(th,el("b",null,P.n),el("small",null,stat));b.title=P.d;
      if(P.cat==="pay"&&M.pay&&M.pay!==id){b.disabled=true;b.title="هذه المهمة تحتاج: "+RW_PARTS[M.pay].n;}
      if(P.cat==="pay"&&M.pay===id)b.append(el("span","rw-need","مطلوبة"));
      b.onclick=()=>add(id);
      b.draggable=true;b.addEventListener("dragstart",e=>{e.dataTransfer.setData("text/plain",id);e.dataTransfer.effectAllowed="copy";});
      box.append(b);});
    const sp=RW_PARTS[stackOf()[sel]];
    $("#rw-hint").textContent=sel!=null&&sp?`محدد: ${sp.n}. اضغط قطعة لتستبدله بها، أو استخدم الأزرار تحت المنصة.`:"اضغط قطعة لتضعها فوق الصاروخ، أو اسحبها إلى المنصة. ابدأ من الأسفل: محرك، ثم خزان، ثم الحمولة.";
  }
  function push(){hist.push(JSON.stringify({b:stackOf().slice(),l:legsOn()}));if(hist.length>40)hist.shift();}
  function add(id,at){
    const st=stackOf(),P=RW_PARTS[id],pi=st.findIndex(x=>RW_PARTS[x].cat==="pay");push();
    if(sel!=null&&st[sel]&&!(P.cat==="pay"||P.fair)&&!(RW_PARTS[st[sel]].cat==="pay"||RW_PARTS[st[sel]].fair)){st[sel]=id;lastAdd=sel;}
    else if(P.cat==="pay"){if(pi>=0){st[pi]=id;lastAdd=pi;}else{st.push(id);lastAdd=st.length-1;}}
    else if(P.fair){if(st.includes("fr")){hist.pop();toast("يوجد غطاء على الصاروخ بالفعل.");return;}if(pi<0){hist.pop();toast("أضف الحمولة أولًا، ثم ضع الغطاء فوقها.");return;}st.splice(pi+1,0,"fr");lastAdd=pi+1;}
    else{let k=at!=null?Math.min(at,pi>=0?pi:st.length):(pi>=0?pi:st.length);st.splice(k,0,id);lastAdd=k;}
    sel=null;save();bay();panel();items();
  }
  function bay(){
    const st=stackOf(),box=$("#rw-bay"),L=rwLayout(st),Hm=Math.max(L.H,12),s=Math.min(14,452/Hm),cx=176,yb=548;
    let g=`<rect width="400" height="600" fill="url(#rwg-bg)"/>`;
    let a=3;const r=()=>(a=(a*16807)%2147483647)/2147483647;for(let i=0;i<46;i++)g+=`<circle cx="${(r()*400).toFixed(0)}" cy="${(r()*380).toFixed(0)}" r="${(r()*.9+.3).toFixed(2)}" fill="#fff" opacity="${(r()*.5+.15).toFixed(2)}"/>`;
    g+=`<rect y="560" width="400" height="40" fill="#2c2440"/><path d="M${cx-46} 560 L${cx-32} 548 L${cx+32} 548 L${cx+46} 560Z" fill="#4a4363"/>`;
    const tw=Math.max(80,yb-(L.H+8)*s);g+=`<g stroke="#6f6890" stroke-width="1.2" fill="none"><rect x="300" y="${tw}" width="20" height="${560-tw}"/>`;
    for(let y=tw;y<556;y+=20)g+=`<path d="M300 ${y} L320 ${y+20} M320 ${y} L300 ${y+20}"/>`;g+=`</g><rect x="296" y="${tw-6}" width="28" height="6" fill="#6f6890"/>`;
    if(!st.length){g+=`<rect x="${cx-15}" y="${yb-120}" width="30" height="120" rx="6" fill="none" stroke="#bdb3e6" stroke-dasharray="5 5" opacity=".6"/><text x="${cx}" y="${yb-140}" class="rw-bt" text-anchor="middle">ابدأ من هنا: اختر محركًا</text>`;}
    let vis="",hits="",fairVis="";
    const pr=rwParse(st,legsOn());
    L.parts.forEach(p=>{const P=RW_PARTS[p.id],b=yb-p.y0*s,t=yb-p.y1*s;
      if(P.fair){if(p.pay)fairVis+=rwFairing(cx,b,s,p.pay,.8);else fairVis+=`<rect x="${cx-RW_D*s*.7}" y="${t}" width="${RW_D*s*1.4}" height="${b-t}" rx="4" fill="url(#rwg-cyl)" opacity=".8"/>`;}
      else vis+=`<g class="${p.i===lastAdd?"rw-new":""}">${rwPart(p.id,cx,b,s)}</g>`;
      const w=(P.fair?RW_D*1.4:P.cat==="pay"&&p.id!=="p4"?3.4:RW_D)*s+8;
      const hit=`<rect class="rw-hit${sel===p.i?" on":""}" x="${(cx-w/2).toFixed(1)}" y="${t.toFixed(1)}" width="${w.toFixed(1)}" height="${Math.max(6,b-t).toFixed(1)}" rx="3" data-i="${p.i}" tabindex="0" role="button" aria-label="${P.n}${sel===p.i?"، محدد":""}"/>`;
      if(P.fair)hits=hit+hits;else hits+=hit;});
    if(legsOn()&&pr.stages.length){const n1=pr.stages[0].length,top=L.parts[n1-1]?L.parts[n1-1].y1:0;vis+=rwLegs(cx,yb,s,top*s)+rwFins(cx,yb-top*s,s);}
    /* stage brackets */
    let k=0,br="";pr.stages.forEach((sg,i)=>{const a0=L.parts[k],a1=L.parts[k+sg.length-1];k+=sg.length;if(!a0||!a1)return;const y0=yb-a0.y0*s,y1=yb-a1.y1*s,x=cx-RW_D*s/2-14;
      br+=`<path d="M${x+6} ${y0-2} H${x} V${y1+2} H${x+6}" stroke="#c4abff" fill="none" stroke-width="1.5"/><text x="${x-4}" y="${(y0+y1)/2+4}" class="rw-bt" text-anchor="start">المرحلة ${i+1}</text>`;});
    box.innerHTML=`<svg viewBox="0 0 400 600" class="rw-bay-svg" role="group" aria-label="الصاروخ على منصة التركيب"><defs><linearGradient id="rwg-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#090620"/><stop offset=".7" stop-color="#1b1446"/><stop offset="1" stop-color="#2b2160"/></linearGradient></defs>${g}${br}${vis}${fairVis}${hits}</svg>`;
    lastAdd=-1;
    box.querySelectorAll(".rw-hit").forEach(h=>{const i=+h.dataset.i;h.addEventListener("click",()=>{sel=sel===i?null:i;bay();tools();items();});h.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();sel=sel===i?null:i;bay();tools();items();const n=$(`#rw-bay .rw-hit[data-i="${i}"]`);if(n)n.focus();}if((e.key==="Delete"||e.key==="Backspace")&&sel!=null){e.preventDefault();del();}});});
    const svg=box.querySelector("svg");
    svg.addEventListener("dragover",e=>{e.preventDefault();e.dataTransfer.dropEffect="copy";});
    svg.addEventListener("drop",e=>{e.preventDefault();const id=e.dataTransfer.getData("text/plain");if(!RW_PARTS[id])return;
      const pt=svg.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;const p=pt.matrixTransform(svg.getScreenCTM().inverse());
      const hm=(yb-p.y)/s;let at=L.parts.filter(q=>!RW_PARTS[q.id].fair&&(q.y0+q.y1)/2<hm).length;sel=null;add(id,at);});
    tools();
  }
  function tools(){
    const t=$("#rw-tools"),st=stackOf();t.replaceChildren();
    const btn=(txt,fn,dis,cls)=>{const b=el("button","btn "+(cls||"btn-ghost"),txt);b.type="button";b.disabled=!!dis;b.onclick=fn;t.append(b);};
    if(sel!=null&&st[sel]){
      t.append(el("span","rw-seltxt",RW_PARTS[st[sel]].n));
      btn("↑ ارفعها",()=>move(1),sel>=st.length-1);btn("↓ أنزلها",()=>move(-1),sel<=0);btn("احذفها",del,false);btn("إلغاء التحديد",()=>{sel=null;bay();items();});
    }else{
      btn("تراجع",()=>{const h=hist.pop();if(!h)return;const o=JSON.parse(h);S.builds[S.mission]=o.b;S.legs[S.mission]=o.l;save();bay();panel();items();},!hist.length);
      btn("أفرغ المنصة",()=>{if(!st.length)return;push();S.builds[S.mission]=[];S.legs[S.mission]=false;sel=null;save();bay();panel();items();},!st.length);
    }
  }
  function move(d){const st=stackOf(),j=sel+d;if(j<0||j>=st.length)return;push();[st[sel],st[j]]=[st[j],st[sel]];sel=j;save();bay();panel();}
  function del(){const st=stackOf();if(sel==null)return;push();st.splice(sel,1);sel=null;save();bay();panel();items();}
  function analysis(){
    const st=stackOf(),pr=rwParse(st,legsOn()),M=mission();
    const errs=pr.errs.slice();if(pr.legsAlone)errs.push("أرجل الهبوط تحتاج صاروخًا بمرحلتين على الأقل، لتعود المرحلة الأولى وحدها.");
    const ph=!errs.length?rwPhysics(pr):null;
    const F=ph?rwFlight(pr,ph,M.goal):null;
    return {st,pr,ph,F,M,errs};
  }
  function panel(){
    const box=$("#rw-panel"),{pr,ph,F,M,errs}=analysis();box.replaceChildren();
    if(ph){
      const big=el("div","rw-big3");
      const it=(n,v,c)=>{const d=el("div",c||"");d.append(el("b",null,v),el("span",null,n));big.append(d);};
      it("كتلة الإقلاع",rwNum(ph.m0,1)+" طن");it("الدفع ÷ الوزن",rwNum(ph.twr,2),ph.twr<1?"bad":ph.twr<1.15?"warn":"ok");it("Δv بعد الخسائر",rwNum(ph.vf,1)+" كم/ث");
      box.append(big);
      const need=M.goal==="moon"?RW_VORB+RW_TLI:M.goal==="orbit"?RW_VORB:null;
      if(need){const bar=el("div","rw-bar"),f=el("i"),mk=el("span","rw-mk");const mx=Math.max(need*1.35,ph.vf*1.05);f.style.width=Math.min(100,ph.vf/mx*100)+"%";f.className=ph.vf>=need?"ok":"";mk.style.left=(need/mx*100)+"%";bar.append(f,mk);box.append(bar,el("small","rw-barl",`العلامة: ${rwNum(need,1)} كم/ث يحتاجها ${M.goal==="moon"?"الذهاب إلى القمر":"المدار"}`));}
      const tb=el("table","rw-tbl");tb.innerHTML=`<thead><tr><th>المرحلة</th><th>الكتلة</th><th>دفع ÷ وزن</th><th>Δv</th><th>الاحتراق</th></tr></thead>`;
      const bd=el("tbody");ph.stages.forEach((s,i)=>{const tr=el("tr");[`${i+1}`,`${rwNum(s.m0,1)} طن`,rwNum(s.twr,2),`${rwNum(s.dv,2)} كم/ث`,`${rwNum(s.tb)} ث`].forEach(v=>tr.append(el("td",null,v)));bd.append(tr);});
      tb.append(bd);box.append(tb);
      const cl=el("ul","rw-check");const c=(ok,t)=>{const li=el("li",ok?"ok":"no");li.append(el("i",null,ok?"✓":"✗"),el("span",null,t));cl.append(li);};
      c(ph.twr>=1,`الدفع أكبر من الوزن عند الإقلاع (${rwNum(ph.twr,2)})`);
      if(M.goal==="space"){const ap=F.apogee0!=null?F.apogee0:F.apogee;c(F.orbit||ap>=100,`يصل إلى ارتفاع 100 كم (المتوقع: ${F.orbit?"المدار":rwNum(ap)+" كم"})`);}
      else if(M.goal==="orbit")c(ph.vf>=RW_VORB,`السرعة تكفي للمدار: ${rwNum(ph.vf,1)} من ${RW_VORB} كم/ث`);
      else c(ph.vf>=RW_VORB+RW_TLI,`السرعة تكفي للقمر: ${rwNum(ph.vf,1)} من ${rwNum(RW_VORB+RW_TLI,1)} كم/ث`);
      if(pr.payload&&RW_PARTS[pr.payload].pay==="sat")c(pr.fair,"الحمولة محمية بغطاء");
      if(M.legs)c(pr.legs,"أرجل الهبوط على المرحلة الأولى");
      box.append(cl);
    }
    if(errs.length){const u=el("ul","rw-errs");errs.forEach(e=>u.append(el("li",null,e)));box.append(el("b","rw-eh","قبل الإطلاق:"),u);}
    if(pr.warns.length&&!errs.length){const u=el("ul","rw-warns");pr.warns.forEach(e=>u.append(el("li",null,e)));box.append(u);}
    const go=el("button","btn btn-accent rw-go","أطلق الصاروخ");go.type="button";go.disabled=!!errs.length;go.onclick=launch;box.append(go);
    if(!stackOf().length)box.append(el("p","lab-note","ركّب صاروخك أولًا، وستظهر هنا كتلته ودفعه وسرعته المتوقعة."));
  }
  function all(){missions();brief();tabs();items();bay();panel();}
  /* ---------- flight ---------- */
  async function launch(){
    const A=analysis();if(A.errs.length)return;
    $("#rw-shop").hidden=true;$("#rw-brief").hidden=true;$("#rw-missions").hidden=true;
    const fl=$("#rw-flight");fl.hidden=false;$("#rw-result").hidden=true;$("#rw-result").replaceChildren();
    $("#rw-fl-title").textContent=A.M.id==="free"?"تجربة حرة: "+RW_GOALS[A.M.goal]:`المهمة: ${A.M.n}`;
    fl.scrollIntoView({block:"start",behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
    if(flight)flight.stop();
    $("#rw-pause").textContent="إيقاف مؤقت";document.querySelectorAll("#rw-speed button").forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.v==="1")));
    flight=await rwFly(A,{done:res=>finish(A,res)});
  }
  function finish(A,res){
    const {ph,F,M,pr}=A,box=$("#rw-result");box.hidden=false;box.replaceChildren();
    const sc=M.id==="free"?{ok:M.goal==="space"?(F.orbit||F.apogee>=100)&&!F.fail&&F.kind!=="pad":M.goal==="orbit"?F.orbit&&!F.fail:F.moon,stars:0}:rwScore(M,pr,ph,F);
    if(M.id!=="free"&&sc.stars>(S.stars[M.id]||0)){S.stars[M.id]=sc.stars;save();}
    let h,why;const tips=[];
    if(F.kind==="pad"){h="لم يرتفع الصاروخ";why=`دفع المحركات ${rwNum(ph.stages[0].thr)} كيلونيوتن، ووزن الصاروخ ${rwNum(ph.m0*RW_G0)} كيلونيوتن. الدفع أقل من الوزن، فبقي على المنصة.`;tips.push("استخدم عنقود محركات أقوى","أو خفّف الصاروخ: خزان أصغر أو مراحل أقل");}
    else if(F.fail==="maxq"){h="تحطّمت الحمولة";why="على ارتفاع نحو 12 كم يكون ضغط الهواء على الصاروخ في أقصاه (Max-Q)، والقمر الصناعي ليس مصممًا لتحمله، فتحطم.";tips.push("ضع «غطاء الحمولة» فوق القمر الصناعي");}
    else if(sc.ok){h=M.goal==="moon"?"انطلق المسبار نحو القمر!":M.goal==="orbit"?"دخلت الحمولة المدار!":"وصل الصاروخ إلى الفضاء!";why=M.goal==="space"?`بلغ ارتفاع ${rwNum(F.orbit?200:F.apogee)} كم، فوق خط كارمان الذي يبدأ عنده الفضاء.`:M.goal==="orbit"?`بلغت سرعته 7.8 كم/ث على ارتفاع نحو 200 كم، فصار يدور حول الأرض بدل أن يسقط.${F.extra>.3?` وبقي في خزاناته ما يكفي ${rwNum(F.extra,1)} كم/ث إضافية.`:""}`:`دخل المدار، ثم أشعل محركه وزاد سرعته 3.1 كم/ث لينطلق نحو القمر على بعد نحو 384,000 كم.`;
      if(F.land)why+=" وهبطت المرحلة الأولى بنجاح لتُستخدم مرة أخرى.";
      if(M.m2&&sc.stars<3)tips.push(`للحصول على نجوم أكثر: اجعل كتلة الإقلاع ${sc.stars<2?"حتى "+rwNum(M.m2)+" طن":"حتى "+rwNum(M.m3)+" طن"}. جرّب خزانات أصغر أو محركًا أخف في المرحلة الثانية.`);}
    else if(F.orbit&&M.goal==="moon"){h="دخل المدار، لكنه لم يصل إلى القمر";why=`بقي له ${rwNum(Math.max(0,F.extra),1)} كم/ث فقط بعد دخول المدار، والانطلاق نحو القمر يحتاج 3.1 كم/ث.`;tips.push("أضف مرحلة ثالثة صغيرة فوق الثانية","أو كبّر خزان المرحلة الثانية");}
    else if(M.legs&&!F.land&&F.orbit){h="دخل المدار، لكن المرحلة الأولى لم تعد";why="هذه المهمة تطلب أن تعود المرحلة الأولى وتهبط، وصاروخك بلا أرجل هبوط.";tips.push("أضف «أرجل الهبوط» من قسم الإضافات");}
    else{h=M.goal==="space"?"لم يصل إلى الفضاء":"لم يدخل المدار";
      why=M.goal==="space"?`أعلى ارتفاع بلغه ${rwNum(F.apogee)} كم، والفضاء يبدأ عند 100 كم.`:`وصل إلى ارتفاع ${rwNum(F.apogee)} كم، لكن سرعته ${rwNum(ph.vf,1)} كم/ث أقل من سرعة المدار 7.8 كم/ث، فجذبته الأرض وعاد.`;
      if(ph.stages.length<2)tips.push("أضف «فاصل مراحل» ثم مرحلة ثانية فوقه: الصاروخ يتخلص من الخزانات الفارغة فيخف");
      if(ph.twr<1.2)tips.push("الدفع قريب من الوزن، فيضيع وقود كثير في مقاومة الجاذبية: استخدم محركات أقوى");
      tips.push("زد الوقود في المرحلة العليا، أو خفّف الحمولة والقطع غير الضرورية");}
    box.append(el("h3",sc.ok?"ok":"no",h));
    if(M.id!=="free")box.append(el("div","rw-stars",rwStars(sc.stars)),el("small","muted",sc.ok?`★ نجاح · ★★ كتلة حتى ${rwNum(M.m2)} طن · ★★★ حتى ${rwNum(M.m3)} طن. كتلة صاروخك ${rwNum(ph.m0,1)} طن.`:"لم تحصل على نجوم هذه المرة."));
    box.append(el("p",null,why));
    if(tips.length){const u=el("ul","rw-tips");tips.forEach(t=>u.append(el("li",null,t)));box.append(u);}
    const g=el("div","rw-rstats");[["أعلى ارتفاع",F.kind==="pad"?"0 كم":F.orbit?"المدار (200 كم)":rwNum(F.apogee)+" كم"],["أعلى سرعة",rwNum(F.kind==="pad"?0:F.maxv,1)+" كم/ث"],["كتلة الإقلاع",rwNum(ph.m0,1)+" طن"],["مدة الرحلة",F.kind==="pad"?"—":F.moon?"نحو 3 أيام":"T+"+rwT(F.tEnd)]].forEach(([a,b])=>{const d=el("div");d.append(el("span",null,a),el("b",null,b));g.append(d);});
    box.append(g);
    const log=el("details","rw-fulllog");log.append(el("summary",null,"سجل الرحلة كاملًا"));const ol=el("ol");F.ev.forEach(e=>{const li=el("li",e.k);li.append(el("b",null,"T+"+rwT(e.t)),el("span",null,e.txt));ol.append(li);});log.append(ol);box.append(log);
    const row=el("div","rw-row");
    const back=el("button","btn btn-accent","عدّل الصاروخ");back.type="button";back.onclick=()=>{if(flight)flight.stop();flight=null;$("#rw-flight").hidden=true;$("#rw-shop").hidden=false;$("#rw-brief").hidden=false;$("#rw-missions").hidden=false;all();$("#rw-shop").scrollIntoView({block:"start"});};
    const again=el("button","btn btn-ghost","أطلق مرة أخرى");again.type="button";again.onclick=launch;row.append(back,again);
    const i=RW_MISSIONS.indexOf(M);if(sc.ok&&i>=0&&i<RW_MISSIONS.length-1){const nx=el("button","btn btn-ghost","المهمة التالية ←");nx.type="button";nx.onclick=()=>{S.mission=RW_MISSIONS[i+1].id;save();back.onclick();};row.append(nx);}
    box.append(row);
    box.scrollIntoView({block:"nearest",behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
  }
  document.querySelectorAll("#rw-speed button").forEach(b=>b.onclick=()=>{document.querySelectorAll("#rw-speed button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));if(flight)flight.speed(+b.dataset.v);});
  $("#rw-pause").onclick=()=>{if(flight)$("#rw-pause").textContent=flight.toggle()?"تابع":"إيقاف مؤقت";};
  $("#rw-skip").onclick=()=>{if(flight)flight.skip();};
  const sndBtn=$("#rw-snd"),sndShow=on=>{sndBtn.textContent=on?"الصوت: يعمل":"الصوت: مطفأ";sndBtn.setAttribute("aria-pressed",String(on));};sndShow(store.get("ufuq-rw-snd",true)!==false);
  sndBtn.onclick=()=>{const on=sndBtn.getAttribute("aria-pressed")!=="true";if(flight)flight.sound(on);else store.set("ufuq-rw-snd",on);sndShow(on);};
  labOff=()=>{if(flight)flight.stop();flight=null;};
  all();
}
