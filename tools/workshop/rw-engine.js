/* ---------- rocket workshop: parts, staging, rocket equation, flight profile ---------- */
const RW_G0=9.81,RW_MU=398600,RW_RE=6371,RW_VORB=7.8,RW_TLI=3.1;
const RW_PARTS={
  e1:{cat:"eng",n:"محرك واحد",d:"محرك يحرق الكيروسين مع الأكسجين السائل. مناسب للمرحلة الأولى.",m:.5,thr:850,isp:300,h:3.6,k:1},
  e3:{cat:"eng",n:"عنقود من 3 محركات",d:"ثلاثة محركات معًا: دفع أكبر ووزن أكبر.",m:1.5,thr:2550,isp:300,h:3.6,k:3},
  e9:{cat:"eng",n:"عنقود من 9 محركات",d:"تسعة محركات معًا، مثل المرحلة الأولى لصاروخ فالكون 9.",m:4.5,thr:7650,isp:300,h:3.6,k:9},
  ev:{cat:"eng",n:"محرك الفراغ",d:"فوهته الكبيرة تعطي كفاءة عالية في الفضاء، لكنه ضعيف قرب سطح الأرض. مكانه المرحلة الثانية.",m:.5,thr:980,isp:348,h:5.2,k:1,vac:1},
  t1:{cat:"tank",n:"خزان صغير",d:"يحمل 25 طنًا من الوقود، وكتلته فارغًا 2 طن.",m:2,prop:25,h:8},
  t2:{cat:"tank",n:"خزان متوسط",d:"يحمل 100 طن من الوقود، وكتلته فارغًا 6 أطنان.",m:6,prop:100,h:19},
  t3:{cat:"tank",n:"خزان كبير",d:"يحمل 200 طن من الوقود، وكتلته فارغًا 11 طنًا.",m:11,prop:200,h:31},
  dc:{cat:"str",n:"فاصل مراحل",d:"حين ينفد وقود المرحلة التي تحته يفصلها ويرميها، فيخف الصاروخ.",m:.5,h:2.4},
  fr:{cat:"str",n:"غطاء الحمولة",d:"يحمي القمر الصناعي من ضغط الهواء أثناء الصعود، ثم يُرمى في الفضاء. ضعه فوق الحمولة.",m:2,h:0,fair:1},
  p1:{cat:"pay",n:"قمر صناعي صغير",d:"كتلته نصف طن.",m:.5,h:2.6,pay:"sat"},
  p3:{cat:"pay",n:"مسبار القمر",d:"كتلته طنان.",m:2,h:3.6,pay:"sat"},
  p2:{cat:"pay",n:"قمر اتصالات",d:"كتلته 6 أطنان.",m:6,h:6.4,pay:"sat"},
  p4:{cat:"pay",n:"كبسولة برواد",d:"كتلتها 12 طنًا مع الرواد، ولها درع حراري فلا تحتاج غطاء.",m:12,h:8.2,pay:"crew"}
};
const RW_LEGS={n:"أرجل هبوط وزعانف شبكية",d:"تُركّب على المرحلة الأولى لتعود وتهبط بعد الإطلاق، كما يفعل فالكون 9. لكنها تزيد الكتلة طنين، ويُحجز 10% من وقود المرحلة الأولى للهبوط.",m:2,res:.1};
const RW_MISSIONS=[
  {id:"m1",n:"القفزة الأولى",goal:"space",pay:"p1",m2:45,m3:32,brief:"أوصل قمرًا صناعيًا صغيرًا إلى الفضاء، فوق خط كارمان على ارتفاع 100 كم.",tip:"صاروخ صغير بمرحلة واحدة يكفي. لا تنس غطاء الحمولة!"},
  {id:"m2",n:"أول قمر في المدار",goal:"orbit",pay:"p1",m2:320,m3:230,brief:"ضع القمر الصغير في مدار حول الأرض. المدار يحتاج سرعة أفقية نحو 7.8 كم/ث.",tip:"جرّب أولًا بمرحلة واحدة وشاهد ماذا يحدث، ثم أضف فاصل مراحل ومرحلة ثانية."},
  {id:"m3",n:"قمر اتصالات",goal:"orbit",pay:"p2",m2:600,m3:460,brief:"ضع قمر اتصالات كتلته 6 أطنان في المدار.",tip:"محرك الفراغ هو الأفضل للمرحلة الثانية."},
  {id:"m4",n:"رواد إلى المدار",goal:"orbit",pay:"p4",m2:650,m3:470,brief:"أوصل كبسولة فيها رواد فضاء إلى المدار، كما في رحلة أكسيوم 2.",tip:"الكبسولة ثقيلة، فانتبه أن يبقى الدفع أكبر من الوزن عند الإقلاع."},
  {id:"m5",n:"إلى القمر",goal:"moon",pay:"p3",m2:700,m3:500,brief:"أرسل مسبارًا إلى القمر: بعد المدار تحتاج 3.1 كم/ث إضافية للانطلاق نحوه.",tip:"قد تحتاج ثلاث مراحل!"},
  {id:"m6",n:"صاروخ يعود",goal:"orbit",pay:"p2",legs:1,m2:650,m3:470,brief:"ضع قمر الاتصالات في المدار، ثم أعد المرحلة الأولى لتهبط على الأرض كما يفعل فالكون 9.",tip:"أضف «أرجل الهبوط» من قسم الإضافات. تذكّر أنها تحجز جزءًا من الوقود."}
];
const RW_GOALS={space:"الوصول إلى الفضاء (100 كم)",orbit:"مدار حول الأرض",moon:"الذهاب إلى القمر"};
/* split the stack (bottom -> top) into stages and check that it can fly */
function rwParse(stack,legs){
  const errs=[],warns=[],stages=[];let cur=[],payload=null,payIdx=-1,fair=false;
  stack.forEach((id,i)=>{const P=RW_PARTS[id];
    if(P.cat==="pay"){if(payload)errs.push("ضع حمولة واحدة فقط.");payload=id;payIdx=i;return;}
    if(P.fair){if(fair)errs.push("غطاء واحد للحمولة يكفي.");else if(payIdx!==i-1)errs.push("ضع غطاء الحمولة فوق الحمولة مباشرة.");fair=true;return;}
    if(payload){errs.push(`لا يمكن وضع «${P.n}» فوق الحمولة. ضع الحمولة في أعلى الصاروخ.`);return;}
    cur.push(id);if(id==="dc"){stages.push(cur);cur=[];}
  });
  if(cur.length)stages.push(cur);
  if(!stack.length)errs.push("المنصة فارغة: ابدأ من الأسفل بمحرك.");
  stages.forEach((s,i)=>{
    const n=i+1,body=s.filter(id=>id!=="dc"),engs=body.filter(id=>RW_PARTS[id].cat==="eng"),tanks=body.filter(id=>RW_PARTS[id].cat==="tank");
    if(!body.length){errs.push(i===0?"لا يبدأ الصاروخ بفاصل مراحل: ضع محركًا في الأسفل.":"فاصلان متتاليان: ضع بينهما محركًا وخزانًا.");return;}
    if(!engs.length)errs.push(`المرحلة ${n} بلا محرك: ضع محركًا في أسفلها.`);
    else if(RW_PARTS[body[0]].cat!=="eng")errs.push(`في المرحلة ${n} ضع المحرك في الأسفل، تحت الخزانات.`);
    if(engs.length>1)errs.push(`في المرحلة ${n} أكثر من محرك واحد. استخدم عنقود محركات بدلًا من ذلك.`);
    if(!tanks.length&&engs.length)errs.push(`محرك المرحلة ${n} بلا وقود: ضع خزانًا فوقه.`);
  });
  if(stages.length>3)errs.push("ثلاث مراحل تكفي لأي مهمة هنا.");
  if(stack.length&&!payload)errs.push("أضف الحمولة في أعلى الصاروخ.");
  if(payload&&RW_PARTS[payload].pay==="sat"&&!fair)warns.push("الحمولة مكشوفة بلا غطاء: قد يحطمها ضغط الهواء أثناء الصعود.");
  if(payload&&RW_PARTS[payload].pay==="crew"&&fair)warns.push("الكبسولة لها درع حراري ولا تحتاج غطاء، فهو وزن زائد.");
  if(stages[0]&&stages[0][0]==="ev")warns.push("محرك الفراغ في المرحلة الأولى ضعيف قرب الأرض: دفعه عند الإقلاع أقل بنحو 30%.");
  return {stages,payload,fair,legs:!!legs&&stages.length>1,legsAlone:!!legs&&stages.length<2,errs,warns};
}
function rwPhysics(st){
  const S=st.stages.map(s=>{let m=0,prop=0,thr=0,isp=0,eng=null;s.forEach(id=>{const P=RW_PARTS[id];m+=P.m+(P.prop||0);prop+=P.prop||0;if(P.thr){thr=P.thr;isp=P.isp;eng=id;}});return {m,prop,thr,isp,eng,ids:s};});
  if(!S.length)return null;
  let reserve=0;
  if(st.legs){S[0].m+=RW_LEGS.m;reserve=S[0].prop*RW_LEGS.res;}
  if(S[0].eng==="ev"){S[0].thr*=.7;S[0].isp=290;}
  const payM=st.payload?RW_PARTS[st.payload].m:0,fairM=st.fair?RW_PARTS.fr.m:0;
  const out=[];
  S.forEach((s,i)=>{
    let above=payM+(i===0||S.length===1?fairM:0);for(let j=i+1;j<S.length;j++)above+=S[j].m;
    const m0=s.m+above,usable=s.prop-(i===0?reserve:0),mf=m0-usable;
    const thr=s.thr,isp=s.isp||1,mdot=thr*1000/(isp*RW_G0);
    out.push({m0,mf,usable,thr,isp,twr:thr/(m0*RW_G0),dv:thr?isp*RW_G0*Math.log(m0/mf)/1000:0,tb:thr?usable*1000/mdot:0,mdot,ids:s.ids});
  });
  const dv=out.reduce((a,s)=>a+s.dv,0),t1=out[0].twr;
  let loss=1.5*Math.min(2.2,Math.max(.8,Math.pow(1.45/Math.max(t1,.01),.8)));
  if(out.slice(1).some(s=>s.thr&&s.twr<.45))loss+=.3;
  return {stages:out,m0:out[0].m0,twr:t1,dv,loss,vf:Math.max(0,dv-loss)};
}
/* coast after burnout: point mass around a spherical Earth (km, s) */
function rwCoast(h0,v,gamma,tmax){
  let x=0,y=RW_RE+h0;const g=gamma*Math.PI/180;let vx=v*Math.cos(g),vy=v*Math.sin(g);
  const pts=[],dt=2;let t=0,ang0=0;
  const acc=(x,y)=>{const r=Math.hypot(x,y),k=-RW_MU/(r*r*r);return [k*x,k*y];};
  while(t<tmax){
    const r=Math.hypot(x,y),h=r-RW_RE,sp=Math.hypot(vx,vy),rv=(x*vx+y*vy)/r;
    pts.push({t,h,v:sp,vr:rv});
    if(t>4&&h<8){pts[pts.length-1].h=0;break;}
    const [ax,ay]=acc(x,y),xm=x+vx*dt/2,ym=y+vy*dt/2,vxm=vx+ax*dt/2,vym=vy+ay*dt/2,[bx,by]=acc(xm,ym);
    x+=vxm*dt;y+=vym*dt;vx+=bx*dt;vy+=by*dt;t+=dt;
  }
  return pts;
}
/* full flight: samples (t -> altitude, speed, pitch, stage) and timed events */
function rwFlight(st,ph,goal){
  const ev=[],S=ph.stages,add=(t,txt,k)=>ev.push({t,txt,k:k||""});
  const F={ev,kind:"",apogee:0,maxv:0,tEnd:0,stageAt:[],orbit:false,moon:false,fail:"",land:false};
  if(ph.twr<1){F.kind="pad";F.tEnd=5;add(0,"تشغيل المحركات");add(2.5,"الدفع أقل من وزن الصاروخ، فلم يتحرك عن المنصة","bad");add(4.5,"أُطفئت المحركات وأُلغي الإطلاق","bad");F.sample=t=>({h:0,v:0,pitch:0,stage:0,fuel:1,burn:t<4.5});return F;}
  /* burn timeline */
  let T=0;const seg=[];S.forEach((s,i)=>{seg.push({i,t0:T,t1:T+s.tb});T+=s.tb+(i<S.length-1?4:0);});
  const Tb=seg[seg.length-1].t1;
  const ideal=t=>{let v=0;for(const g of seg){const s=S[g.i];if(t<=g.t0)break;const tau=Math.min(t,g.t1)-g.t0;v+=s.isp*RW_G0*Math.log(s.m0/(s.m0-s.mdot/1000*tau))/1000;}return v;};
  const speed=t=>Math.max(0,ideal(t)-ph.loss*Math.min(1,t/Tb));
  const stageOf=t=>{let k=0;for(const g of seg)if(t>=g.t0)k=g.i;return k;};
  const fuelOf=t=>{const k=stageOf(t),g=seg[k];return Math.max(0,1-(Math.min(t,g.t1)-g.t0)/(g.t1-g.t0||1));};
  const burning=t=>seg.some(g=>t>=g.t0&&t<g.t1);
  const vf=ph.vf,orbit=vf>=RW_VORB;
  /* altitude and pitch tables: climb by integrating vertical speed, capped by a curve that
     reaches the target height exactly when the target speed is reached */
  function table(tEnd,vT,hT,pMax,steep){
    const dt=.5,N=Math.max(2,Math.ceil(tEnd/dt)),Hh=[],Pp=[];let fm=0,hi=0;
    for(let i=0;i<=N;i++){const t=i*dt*tEnd/(N*dt),v=speed(t);fm=Math.max(fm,Math.min(1,v/vT));
      const p=steep?pMax*t/tEnd:pMax*Math.pow(fm,.55)*Math.min(1,Math.max(0,(t-6)/10));
      if(i)hi+=v*Math.cos(p*Math.PI/180)*tEnd/N;
      Hh.push(steep?hi:Math.min(hi,hT*(1-Math.pow(1-fm,1.3))));Pp.push(p);}
    if(!steep){const e=hT-Hh[N];for(let i=0;i<=N;i++)Hh[i]+=e*Math.pow(i/N,4);}
    const at=(A,t)=>{const x=Math.max(0,Math.min(1,t/tEnd))*N,i=Math.min(N-1,Math.floor(x)),f=x-i;return A[i]+(A[i+1]-A[i])*f;};
    return {h:t=>at(Hh,t),p:t=>at(Pp,t),hEnd:Hh[N]};
  }
  if(orbit){
    let tIns=Tb;for(let t=0;t<=Tb;t+=.5)if(speed(t)>=RW_VORB){tIns=t;break;}
    const Tt=table(tIns,RW_VORB,200,88,false),hOf=Tt.h,pitchOf=Tt.p;
    F.kind="orbit";F.orbit=true;F.tEnd=tIns;F.apogee=200;F.maxv=RW_VORB;F.extra=vf-RW_VORB;F.moon=goal==="moon"&&F.extra>=RW_TLI;
    F.sample=t=>{t=Math.min(t,tIns);return {h:hOf(t),v:Math.min(speed(t),RW_VORB),pitch:pitchOf(t),stage:stageOf(t),fuel:fuelOf(t),burn:burning(t)&&t<tIns};};
    F.burnEnd=tIns;
  }else{
    const steep=goal==="space"||vf<3;
    let hbo,gam;
    gam=steep?84:Math.max(8,45-5*vf);
    const Tt=table(Tb,Math.max(.05,vf),steep?0:Math.min(180,30+22*vf),90-gam,steep);hbo=Math.max(.5,steep?Tt.hEnd:Math.min(180,30+22*vf));
    const hOf=Tt.h,pitchOf=Tt.p;
    const co=rwCoast(hbo,Math.max(.05,vf),gam,20000);
    F.kind="sub";F.coast=co;F.apogee=Math.max(hbo,...co.map(p=>p.h));F.maxv=Math.max(vf,...co.map(p=>p.v));F.tEnd=Tb+co[co.length-1].t;F.burnEnd=Tb;
    F.sample=t=>{
      if(t<=Tb)return {h:hOf(t),v:speed(t),pitch:pitchOf(t),stage:stageOf(t),fuel:fuelOf(t),burn:burning(t)};
      const u=(t-Tb)/2,i=Math.min(co.length-2,Math.floor(u)),f=Math.min(1,u-i),a=co[i],b=co[i+1]||a;
      const vr=a.vr+(b.vr-a.vr)*f,v=a.v+(b.v-a.v)*f,pitch=90-Math.asin(Math.max(-1,Math.min(1,vr/Math.max(v,.01))))*180/Math.PI;
      return {h:Math.max(0,a.h+(b.h-a.h)*f),v,pitch,stage:S.length-1,fuel:0,burn:false};
    };
  }
  /* events */
  add(0,"إقلاع! انطلق الصاروخ عن المنصة","ok");
  const find=(fn,t0,t1,dt)=>{for(let t=t0;t<=t1;t+=dt||.5)if(fn(F.sample(t)))return t;return null;};
  const tEndAsc=F.kind==="orbit"?F.tEnd:F.burnEnd;
  const tM=find(s=>s.v>=.343,0,tEndAsc);if(tM!=null)add(tM,"تجاوز سرعة الصوت");
  const tQ=find(s=>s.h>=12,0,tEndAsc);
  if(tQ!=null){
    add(tQ,"أقصى ضغط للهواء على الصاروخ (Max-Q)");
    if(st.payload&&RW_PARTS[st.payload].pay==="sat"&&!st.fair){F.fail="maxq";F.tFail=tQ+1;F.tEnd=tQ+1;add(tQ+1,"تحطّمت الحمولة المكشوفة من ضغط الهواء!","bad");
      const sq=F.sample(tQ+1);F.apogee0=F.orbit?200:F.apogee;F.apogee=sq.h;F.maxv=sq.v;F.kind="fail";F.orbit=F.moon=false;}
  }
  seg.forEach((g,i)=>{if(i<seg.length-1&&g.t1<F.tEnd){add(g.t1,`انفصال المرحلة ${i+1} بعد نفاد وقودها`,"sep");add(g.t1+4,`تشغيل محرك المرحلة ${i+2}`);F.stageAt.push(g.t1);}});
  if(st.fair){const tF=find(s=>s.h>=110,seg.length>1?seg[0].t1+6:0,tEndAsc);if(tF!=null&&tF<F.tEnd){add(tF,"رُمي غطاء الحمولة: لم يعد هناك هواء يضغط عليها","sep");F.tFair=tF;}}
  const tK=find(s=>s.h>=100,0,F.tEnd,1);if(tK!=null&&!F.fail)add(tK,"عبر خط كارمان: الصاروخ في الفضاء!","ok");
  if(!F.fail){
    if(F.kind==="orbit")add(F.tEnd,F.extra>.05?"وصل إلى سرعة المدار 7.8 كم/ث وأطفأ محركه":"وصل إلى سرعة المدار وأطفأ محركه","ok");
    else{add(F.burnEnd,"نفد الوقود وانطفأ آخر محرك");const ta=F.burnEnd+F.coast.reduce((b,p)=>p.h>b.h?p:b,F.coast[0]).t;add(ta,`أعلى ارتفاع: ${Math.round(F.apogee).toLocaleString("en-US")} كم`);if(F.apogee>=100){const tr=find(s=>s.h<100,ta,F.tEnd,2);if(tr!=null)add(tr,"عاد إلى الغلاف الجوي لأن سرعته لا تكفي للمدار");}add(F.tEnd,"سقط في المحيط");}
  }
  if(st.legs&&seg.length>1&&!F.fail){const t0=seg[0].t1;F.land=true;add(t0+25,"المرحلة الأولى تستدير عائدة نحو الأرض","sep");F.tLand=t0+380;if(F.tLand<=F.tEnd)add(F.tLand,"هبطت المرحلة الأولى بنجاح على منصة الهبوط!","ok");}
  ev.sort((a,b)=>a.t-b.t);
  return F;
}
function rwScore(mission,st,ph,F){
  const goal=mission.goal;let ok=false;
  if(F.fail||F.kind==="pad")ok=false;
  else if(goal==="space")ok=F.apogee>=100;
  else if(goal==="orbit")ok=F.orbit;
  else ok=F.moon;
  if(mission.legs&&!F.land)ok=false;
  let stars=0;if(ok&&mission.m2){stars=1;if(ph.m0<=mission.m2)stars=2;if(ph.m0<=mission.m3)stars=3;}
  return {ok,stars};
}
