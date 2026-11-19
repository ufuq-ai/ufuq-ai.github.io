/* ---------- rocket workshop: the launch, drawn on a canvas that follows the rocket ---------- */
async function rwFly(A,cb){
  const {pr,ph,F,st}=A,goal=A.M.goal;
  const cv=$("#rw-cv"),stage=$("#rw-stage"),ctx=cv.getContext("2d"),mini=$("#rw-mini"),mx=mini.getContext("2d");
  const still=matchMedia("(prefers-reduced-motion: reduce)").matches,dpr=Math.min(2,window.devicePixelRatio||1);
  const log=$("#rw-log"),big=$("#rw-big");log.replaceChildren();big.textContent="";big.className="rw-big";
  /* images of every piece the rocket will shed */
  const ranges=[];let i0=0;pr.stages.forEach(sg=>{ranges.push([i0,i0+sg.length]);i0+=sg.length;});
  const n=ranges.length,S6=6,isPay=x=>RW_PARTS[x].cat==="pay"||RW_PARTS[x].fair;
  const mk=async(ids,o)=>{const r=rwStackSVG(ids,Object.assign({s:S6},o));r.img=await rwImg(r.svg);return r;};
  const up=[],upNF=[],drop=[];
  for(let k=0;k<n;k++){
    const ids=st.slice(ranges[k][0]),lg=k===0&&pr.legs,lt=ranges[0][1]-1;
    up[k]=await mk(ids,{legs:lg,legsTop:lt});
    upNF[k]=pr.fair?await mk(ids.filter(x=>x!=="fr"),{fair:false,legs:lg,legsTop:lt}):up[k];
    drop[k]=await mk(st.slice(ranges[k][0],ranges[k][1]),{legs:lg,legsTop:ranges[0][1]-1});
  }
  let noPay=null,payImg=null,topNoPay=null;const insStage=F.kind==="orbit"?Math.min(n-1,F.sample(F.tEnd).stage):0;
  if(F.fail)noPay=await mk(st.filter(x=>!isPay(x)),{legs:pr.legs,legsTop:ranges[0][1]-1});
  if(F.kind==="orbit"&&pr.payload){payImg=await mk([pr.payload],{fair:false});const top=st.slice(ranges[insStage][0]).filter(x=>!isPay(x));topNoPay=top.length?await mk(top,{legs:insStage===0&&pr.legs,legsTop:ranges[0][1]-1}):null;}
  let fairL=null,fairR=null;
  if(pr.fair&&pr.payload){const Wf=RW_D*1.4*S6+4*S6,Hf=rwFairH(pr.payload)*S6+4*S6,cx=Wf/2,yb=Hf-2*S6;
    const svg=h=>`<svg xmlns="http://www.w3.org/2000/svg" width="${Math.ceil(Wf)}" height="${Math.ceil(Hf)}" viewBox="0 0 ${Wf} ${Hf}">${RW_DEFS}${rwFairing(cx,yb,S6,pr.payload,1,h)}</svg>`;
    fairL={img:await rwImg(svg("L")),w:Wf,h:Hf};fairR={img:await rwImg(svg("R")),w:Wf,h:Hf};}
  /* sound: engine rumble from filtered noise, beeps, separation thumps and the explosion */
  const SND={ctx:null,eng:null,on:store.get("ufuq-rw-snd",true)!==false};
  function sndInit(){
    if(SND.ctx||!SND.on)return;const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;
    try{const a=new AC(),master=a.createGain();master.gain.value=.5;master.connect(a.destination);
      const len=a.sampleRate*2,buf=a.createBuffer(1,len,a.sampleRate),d=buf.getChannelData(0);let l=0;for(let i=0;i<len;i++){const w=Math.random()*2-1;l=(l+.02*w)/1.02;d[i]=l*3.2;}
      const src=a.createBufferSource();src.buffer=buf;src.loop=true;const lp=a.createBiquadFilter();lp.type="lowpass";lp.frequency.value=420;const g=a.createGain();g.gain.value=0;
      src.connect(lp);lp.connect(g);g.connect(master);src.start();SND.ctx=a;SND.master=master;SND.eng=g;SND.lp=lp;SND.noise=buf;}catch(_){SND.ctx=null;}
  }
  function beep(fq,dur,vol){const a=SND.ctx;if(!a||!SND.on)return;const o=a.createOscillator(),g=a.createGain();o.frequency.value=fq;o.type="sine";g.gain.setValueAtTime(0,a.currentTime);g.gain.linearRampToValueAtTime(vol||.25,a.currentTime+.01);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+dur);o.connect(g);g.connect(SND.master);o.start();o.stop(a.currentTime+dur+.05);}
  function thump(vol,dur,fq){const a=SND.ctx;if(!a||!SND.on)return;const s=a.createBufferSource();s.buffer=SND.noise;const lp=a.createBiquadFilter();lp.type="lowpass";lp.frequency.value=fq||300;const g=a.createGain();g.gain.setValueAtTime(vol,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+dur);s.connect(lp);lp.connect(g);g.connect(SND.master);s.start(0,Math.random());s.stop(a.currentTime+dur+.05);}
  function engineVol(v){if(SND.eng&&SND.ctx)SND.eng.gain.setTargetAtTime(SND.on?v:0,SND.ctx.currentTime,.12);}
  let lastBeep=99;
  /* sizing: the camera zooms so the current stage fills about half the view */
  let W=0,H=0,k=4,kT=4,stageIdx=0;
  const kFor=i=>Math.max(1.4,Math.min(9,H*.5/up[Math.min(i,n-1)].H));
  function size(){const w=Math.round(stage.getBoundingClientRect().width)||600,h=Math.round(Math.min(600,Math.max(420,w*.62)));
    stage.style.height=h+"px";cv.width=w*dpr;cv.height=h*dpr;cv.style.width=w+"px";cv.style.height=h+"px";ctx.setTransform(dpr,0,0,dpr,0,0);W=w;H=h;
    k=kT=kFor(stageIdx);
    const mw=Math.min(180,w*.34),mh=mw*.58;mini.width=mw*dpr;mini.height=mh*dpr;mini.style.width=mw+"px";mini.style.height=mh+"px";mx.setTransform(dpr,0,0,dpr,0,0);
    if(still&&staticReady)staticDraw();}
  let staticReady=false;function staticDraw(){last=performance.now();frame(last);cancelAnimationFrame(raf);}
  size();addEventListener("resize",size);
  /* scenery */
  let seed=9;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const stars=Array.from({length:150},()=>({x:rnd(),y:rnd(),r:rnd()*1.2+.3,a:rnd()*.6+.3}));
  const clouds=Array.from({length:9},(_,i)=>({alt:1.2+i*.9+rnd()*.6,x:rnd(),w:90+rnd()*140,h:18+rnd()*16}));
  const streaks=Array.from({length:34},()=>({x:rnd()-.5,y:rnd(),v:.6+rnd()*.8,l:.5+rnd()}));
  const parts=[],puffs=[],debris=[];
  /* state */
  const tIgn=F.kind==="pad"?-1:-3;
  let t=-5,tau=0,phase="count",speed=1,paused=false,raf=0,last=0,shift=0,shiftFrom=0,shiftT=1,fairOn=!!pr.fair,failed=false,flash=0,shake=0,fade=0,mapRot=0,postT=0,phT=0,boomT=0,endT=0,doneSent=false,evI=0,landLogged=0,splashed=false,ignLogged=false;
  const C=()=>({x:W*.5,y:H*.5});
  const sea=()=>F.kind==="sub"&&t>F.burnEnd+2;
  function hudSet(clk,alt,vel,stg,fuel){
    $("#rw-clock").textContent=clk<0?"T−"+rwT(Math.ceil(-clk-1e-9)):"T+"+rwT(clk);
    $("#rw-alt").textContent=rwNum(alt,alt<10?1:0)+" كم";
    $("#rw-vel").textContent=rwNum(vel,2)+" كم/ث";
    $("#rw-stg").textContent=stg;
    $("#rw-fuel").style.width=Math.max(0,Math.min(1,fuel))*100+"%";
  }
  function pushLog(e){
    const li=el("li",e.k||"");li.append(el("b",null,e.t<0?"T−"+rwT(-e.t):"T+"+rwT(e.t)),el("span",null,e.txt));log.prepend(li);
    while(log.children.length>4)log.lastChild.remove();
  }
  function bigMsg(txt,cls){big.textContent=txt;big.className="rw-big"+(cls?" "+cls:"");}
  /* pacing: real seconds shown per second of flight. Real time at liftoff so the rocket feels heavy, slow
     motion around events, and one rate for the rest, chosen so that reaching space takes about a minute and
     reaching orbit about 70 seconds; the clock on screen always shows the true flight time */
  const PACE=(()=>{
    if(F.kind==="pad")return null;
    const at=txt=>{const e=F.ev.find(x=>x.txt.includes(txt));return e?e.t:null;};
    let tK=null;if(F.kind!=="fail")for(let x=0;x<=F.tEnd;x+=.5)if(F.sample(x).h>=100){tK=x;break;}
    const win=[],add=(a,b,v)=>win.push([a,b,v]),tM=at("سرعة الصوت"),tQ=at("Max-Q");
    if(tM!=null)add(tM-2,tM+2,.45);if(tQ!=null)add(tQ-3,tQ+3,.4);
    F.stageAt.forEach(x=>add(x-3,x+8,.5));if(F.tFair!=null)add(F.tFair-3,F.tFair+3,.45);
    if(F.tFail!=null)add(F.tFail-6,F.tFail+.5,.55);if(F.land&&F.tLand<=F.tEnd)add(F.tLand-35,F.tLand+7,.15);
    if(tK!=null)add(tK-2,tK+2,.45);if(F.kind==="orbit")add(F.tEnd-10,F.tEnd,.4);if(F.kind==="sub")add(F.tEnd-22,F.tEnd,.2);
    const wv=x=>{let r=0;for(const [a,b,v] of win)if(x>=a&&x<=b&&v>r)r=v;return r;};
    const lift=x=>1/(1+Math.max(0,x-5)/12);
    const tGoal=F.kind==="orbit"?F.tEnd:F.kind==="fail"?F.tFail:tK!=null?tK:F.burnEnd,Rg=F.kind==="orbit"?72:F.kind==="fail"?0:tK!=null?60:40;
    const dS=.25,N=Math.max(1,Math.ceil(F.tEnd/dS));
    const integ=b=>{let R=0;for(let i=0;i<N;i++){const x=(i+.5)*dS;if(x>tGoal)break;R+=Math.max(lift(x),wv(x),b)*dS;}return R;};
    let base=.2;
    if(Rg>0){if(integ(0)>=Rg)base=0;else if(integ(1)<=Rg)base=1;else{let lo=0,hi=1;for(let i=0;i<40;i++){const m=(lo+hi)/2;if(integ(m)<Rg)lo=m;else hi=m;}base=(lo+hi)/2;}}
    const rC=F.kind==="sub"&&F.tEnd>tGoal?24/(F.tEnd-tGoal):base;
    const R=new Float64Array(N+1);for(let i=0;i<N;i++){const x=(i+.5)*dS;R[i+1]=R[i]+(x<=tGoal?Math.max(lift(x),wv(x),base):Math.max(rC,wv(x)))*dS;}
    return {R,dS,N,total:R[N]};
  })();
  function tAt(x){if(!PACE)return Math.min(F.tEnd,x);const {R,dS,N}=PACE;if(x>=R[N])return F.tEnd;let lo=0,hi=N;while(hi-lo>1){const m=(lo+hi)>>1;if(R[m]<=x)lo=m;else hi=m;}return Math.min(F.tEnd,(lo+(x-R[lo])/((R[hi]-R[lo])||1))*dS);}
  /* after orbit: how long each scene lasts (real seconds) and the Earth-to-Moon transfer used for the numbers */
  const DEP=3.4,ORB=5,PARK=12,TLI=10,TRANS=30,ARR=3.5,TT0=90;
  const sIns=F.kind==="orbit"?F.sample(F.tEnd):null,f0=sIns?sIns.fuel:0,fracTLI=F.moon?Math.min(1,RW_TLI/Math.max(F.extra,.01)):0;
  const TR=(()=>{if(!F.moon)return null;const mu=RW_MU,r1=RW_RE+200,rm=384400,T=3*86400;
    const tTo=r2=>{const a=(r1+r2)/2,e=(r2-r1)/(r2+r1),nn=Math.sqrt(mu/(a*a*a)),E=Math.acos(Math.max(-1,Math.min(1,(1-rm/a)/e)));return (E-e*Math.sin(E))/nn;};
    let lo=rm*1.0001,hi=rm*6;for(let i=0;i<60;i++){const m=(lo+hi)/2;if(tTo(m)>T)lo=m;else hi=m;}
    const r2=(lo+hi)/2,a=(r1+r2)/2,e=(r2-r1)/(r2+r1),nn=Math.sqrt(mu/(a*a*a)),Em=Math.acos((1-rm/a)/e),tab=[];
    for(let i=0;i<=600;i++){const E=Em*i/600;tab.push([(E-e*Math.sin(E))/nn,a*(1-e*Math.cos(E))]);}
    const rAt=x=>{if(x<=0)return r1;for(let i=1;i<tab.length;i++)if(tab[i][0]>=x){const [a0,b0]=tab[i-1],[a1,b1]=tab[i];return b0+(b1-b0)*(x-a0)/((a1-a0)||1);}return rm;};
    return {rAt,vAt:r=>Math.sqrt(mu*(2/r-1/a)),T,r1,rm};})();
  const ttTrans=u=>TT0+(TR?TR.T-TT0:0)*Math.pow(Math.max(0,Math.min(1,u)),1.6);
  const TMARK=[[RW_RE+35786,"تجاوز ارتفاع الأقمار الصناعية الثابتة: نحو 36,000 كم"],[192200,"منتصف الطريق إلى القمر"],[318000,"دخل منطقة جاذبية القمر"]];let tmI=0;
  /* sky colour by altitude */
  const lerp=(a,b,u)=>a+(b-a)*u,mix=(c1,c2,u)=>{const p=c=>[1,3,5].map(i=>parseInt(c.slice(i,i+2),16));const A=p(c1),B=p(c2);return `rgb(${A.map((v,i)=>Math.round(lerp(v,B[i],u))).join(",")})`;};
  function skyCols(h){const P=[[0,"#3f86d8","#a9d4f5"],[12,"#1c3f8f","#5b97dc"],[35,"#0a1440","#22468c"],[70,"#03061a","#0c1a48"],[120,"#010208","#050b22"]];
    for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1];if(h<=b[0]){const u=Math.max(0,(h-a[0])/(b[0]-a[0]));return [mix(a[1],b[1],u),mix(a[2],b[2],u)];}}return [P[4][1],P[4][2]];}
  function drawSky(h){
    const [top,bot]=skyCols(h),g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,top);g.addColorStop(1,bot);ctx.fillStyle=g;ctx.fillRect(-20,-20,W+40,H+40);
    const sa=Math.max(0,Math.min(1,(h-20)/45));
    if(sa>0){ctx.fillStyle="#fff";stars.forEach(s=>{ctx.globalAlpha=s.a*sa;ctx.beginPath();ctx.arc(((s.x*W-shift*.02)%W+W)%W,s.y*H,s.r,0,7);ctx.fill();});ctx.globalAlpha=1;}
    if(h>22){const lh=H*Math.min(.3,.04+(h-22)/700),R=W*2.2/(1+h/500),cy=H-lh+R;
      const eg=ctx.createRadialGradient(W/2,cy,R*.9,W/2,cy,R);eg.addColorStop(0,"#0d2c5c");eg.addColorStop(1,"#2f74c4");
      ctx.fillStyle=eg;ctx.beginPath();ctx.arc(W/2,cy,R,0,7);ctx.fill();
      ctx.fillStyle="rgba(255,255,255,.18)";for(let i=0;i<7;i++){const x=((i*W*.37-shift*.15)%(W*1.6)+W*1.6)%(W*1.6)-W*.3,y=H-lh*(.35+.1*(i%3));ctx.beginPath();ctx.ellipse(x,y+lh*.25,60+(i%4)*30,4+(i%3)*2,0,0,7);ctx.fill();}
      for(let i=0;i<6;i++){ctx.strokeStyle=`rgba(126,196,255,${.22-i*.035})`;ctx.lineWidth=3+i*3;ctx.beginPath();ctx.arc(W/2,cy,R+i*3,Math.PI*1.1,Math.PI*1.9);ctx.stroke();}}
  }
  function drawClouds(h){
    const c=C();clouds.forEach(cl=>{const y=c.y-(cl.alt-h)*70,x=((cl.x*W-shift*.6)%(W+300)+W+300)%(W+300)-150;if(y<-60||y>H+60)return;
      ctx.fillStyle="rgba(255,255,255,.62)";for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(x+i*cl.w/5,y+Math.sin(i*1.7)*4,cl.w/4,cl.h*(.6+.4*Math.sin(i)),0,0,7);ctx.fill();}});
  }
  /* air rushing past: streaks along the rocket's axis, only in the thick lower air */
  function drawStreaks(h,v,pitch,dt){
    const air=h<2?h/2:Math.max(0,1-(h-2)/55),amt=air*Math.min(1,v/.8);if(amt<.03||failed||splashed||phase==="end")return;
    const c=C(),Lh=H*1.5;ctx.save();ctx.translate(c.x,c.y);ctx.rotate(pitch*Math.PI/180);ctx.strokeStyle="#fff";ctx.lineCap="round";
    streaks.forEach(s=>{s.y=(s.y+dt*s.v*(1.2+v*1.6))%1;const y=s.y*Lh-Lh/2,len=(20+60*Math.min(1.5,v))*s.l;ctx.globalAlpha=.32*amt;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(s.x*W*1.3,y);ctx.lineTo(s.x*W*1.3,y-len);ctx.stroke();});
    ctx.restore();ctx.globalAlpha=1;
  }
  /* condensation cloud around the rocket as it passes the speed of sound */
  function vaporCone(cx,cy,a,cur,v,h){
    if(v<.29||v>.5||h>16||failed)return;const u=1-Math.abs(v-.36)/.14;if(u<=0)return;
    const L=cur.H*k,mx_=cx+a.x*L*.12,my=cy+a.y*L*.12;ctx.save();ctx.translate(mx_,my);ctx.rotate(Math.atan2(a.y,a.x)+Math.PI/2);
    const g=ctx.createLinearGradient(0,-L*.1,0,L*.35);g.addColorStop(0,"rgba(255,255,255,0)");g.addColorStop(.35,`rgba(255,255,255,${.55*u})`);g.addColorStop(1,"rgba(255,255,255,0)");
    ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(-RW_D*k*.55,-L*.08);ctx.quadraticCurveTo(-RW_D*k*2.6,L*.22,-RW_D*k*1.9,L*.36);ctx.lineTo(RW_D*k*1.9,L*.36);ctx.quadraticCurveTo(RW_D*k*2.6,L*.22,RW_D*k*.55,-L*.08);ctx.fill();ctx.restore();
  }
  function groundY(h,pitch){return C().y+up[stageIdx].H/2*k*Math.cos(pitch*Math.PI/180)+h*1000*k;}
  function drawGround(h,pitch){
    const gy=groundY(h,pitch);if(gy>H+40)return gy;const c=C();
    if(sea()){
      const g=ctx.createLinearGradient(0,gy,0,H);g.addColorStop(0,"#2a6fb5");g.addColorStop(1,"#123a6e");ctx.fillStyle=g;ctx.fillRect(-20,gy,W+40,H-gy+40);
      ctx.strokeStyle="rgba(220,240,255,.35)";ctx.lineWidth=1.4;for(let i=0;i<14;i++){const y=gy+6+i*i*3;if(y>H)break;const x0=((i*97-shift*(.4+i*.05))%(W+120)+W+120)%(W+120)-60;ctx.beginPath();ctx.moveTo(x0,y);ctx.quadraticCurveTo(x0+14,y-3,x0+28,y);ctx.stroke();}
      return gy;}
    ctx.fillStyle="#2f6b45";ctx.fillRect(-20,gy,W+40,H-gy+40);ctx.fillStyle="#3f8a59";ctx.fillRect(-20,gy,W+40,4);
    ctx.fillStyle="#4a4363";ctx.beginPath();ctx.moveTo(c.x-RW_D*k*2.2,gy);ctx.lineTo(c.x-RW_D*k*1.4,gy-1.6*k);ctx.lineTo(c.x+RW_D*k*1.4,gy-1.6*k);ctx.lineTo(c.x+RW_D*k*2.2,gy);ctx.fill();
    const tx=c.x+RW_D*k*1.5+6,th=(up[0].H+6)*k;ctx.strokeStyle="#6f6890";ctx.lineWidth=1.2;ctx.strokeRect(tx,gy-th,12,th);
    ctx.beginPath();for(let y=gy-th;y<gy-4;y+=12){ctx.moveTo(tx,y);ctx.lineTo(tx+12,y+12);ctx.moveTo(tx+12,y);ctx.lineTo(tx,y+12);}ctx.stroke();
    return gy;
  }
  function axis(p){const a=p*Math.PI/180;return {x:Math.sin(a),y:-Math.cos(a)};}
  function drawImgAt(r,cx,cy,rot,alpha){if(!r||!r.img)return;const f=k/S6;ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.translate(cx,cy);ctx.rotate(rot*Math.PI/180);ctx.drawImage(r.img,-r.w*f/2,-r.h*f/2,r.w*f,r.h*f);ctx.restore();}
  function flame(bx,by,ax,h,power,vac){
    const len=(vac?7:10)*k*(.85+Math.random()*.25)*Math.min(2.6,1+h/45)*power,wid=RW_D*k*(vac?.9:1.05)*Math.min(3,1+h/35);
    ctx.save();ctx.translate(bx,by);ctx.rotate(Math.atan2(-ax.x,ax.y));ctx.globalCompositeOperation="lighter";
    const g=ctx.createLinearGradient(0,0,0,len);g.addColorStop(0,"rgba(255,255,240,.95)");g.addColorStop(.25,"rgba(255,214,120,.85)");g.addColorStop(.6,"rgba(255,140,60,.45)");g.addColorStop(1,"rgba(255,90,40,0)");
    ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(-wid*.22,0);ctx.quadraticCurveTo(-wid*.6,len*.45,0,len);ctx.quadraticCurveTo(wid*.6,len*.45,wid*.22,0);ctx.fill();
    if(h<1.5){const gl=ctx.createRadialGradient(0,len*.6,0,0,len*.6,len*1.2);gl.addColorStop(0,"rgba(255,190,90,.35)");gl.addColorStop(1,"rgba(255,190,90,0)");ctx.fillStyle=gl;ctx.beginPath();ctx.arc(0,len*.6,len*1.2,0,7);ctx.fill();}
    ctx.restore();
  }
  function emit(bx,by,ax,h,dt,power){
    const nF=Math.round(26*dt*60*power),smoke=h<38;
    for(let i=0;i<nF;i++){const sp=(260+Math.random()*180),sd=(Math.random()-.5)*.5;
      parts.push({x:bx+(Math.random()-.5)*RW_D*k*.6,y:by,vx:-ax.x*sp+sd*120*ax.y,vy:-ax.y*sp+sd*120*ax.x,life:0,max:.25+Math.random()*.3,r:3+Math.random()*4,f:1});}
    if(smoke)for(let i=0;i<Math.round(8*dt*60);i++)parts.push({x:bx+(Math.random()-.5)*RW_D*k,y:by+10,vx:-ax.x*120+(Math.random()-.5)*50,vy:-ax.y*120+160+Math.random()*120,life:0,max:1.4+Math.random()*1.4,r:6+Math.random()*8,f:0});
    if(parts.length>1100)parts.splice(0,parts.length-1100);
  }
  function drawParts(dt){
    for(let i=parts.length-1;i>=0;i--){const p=parts[i];p.life+=dt;if(p.life>p.max){parts.splice(i,1);continue;}p.x+=p.vx*dt;p.y+=p.vy*dt;if(p.g)p.vy+=p.g*dt;if(p.drag){p.vx*=1-p.drag*dt;p.vy*=1-p.drag*dt;}p.r+=dt*(p.grow!=null?p.grow:p.f?14:26);
      const u=p.life/p.max;ctx.globalAlpha=(1-u)*(p.a||(p.fx?.9:p.f?.8:.35));ctx.fillStyle=p.col||(p.fx?(u<.12?"#fff3c4":u<.3?"#ffc04d":u<.55?"#ff7a2e":"#7d3b2c"):p.f?(u<.3?"#fff3c4":u<.6?"#ffb15c":"#ff7a3d"):"#c9c6d4");
      if(p.f&&!p.fx)ctx.globalCompositeOperation="lighter";ctx.beginPath();ctx.arc(p.x,p.y,Math.max(.5,p.r),0,7);ctx.fill();ctx.globalCompositeOperation="source-over";}
    ctx.globalAlpha=1;
  }
  function drawPuffs(gy,dt){
    for(let i=puffs.length-1;i>=0;i--){const p=puffs[i];p.life+=dt;if(p.life>p.max){puffs.splice(i,1);continue;}p.x+=p.vx*dt;p.vx*=.985;p.r+=dt*22;p.alt+=dt*4;
      ctx.globalAlpha=.55*(1-p.life/p.max);ctx.fillStyle="#d8d5e2";ctx.beginPath();ctx.arc(p.x,gy-p.alt*k*.2-p.r*.4,p.r,0,7);ctx.fill();}ctx.globalAlpha=1;
  }
  function drawDebris(dt,h){
    for(let i=debris.length-1;i>=0;i--){const d=debris[i];d.life+=dt;if(d.life>d.max){debris.splice(i,1);continue;}
      d.vx+=d.ax*dt;d.vy+=d.ay*dt;d.x+=d.vx*dt;d.y+=d.vy*dt;d.rot+=d.vr*dt;
      if(d.flip&&d.life>1.4&&d.life<3.6){d.rot+=(d.flipTo-d.rot)*Math.min(1,dt*1.6);}
      const al=Math.max(0,Math.min(1,(d.max-d.life)/1.2));
      if(d.flip&&d.life>2.6&&d.life<4.4){const a=axis(d.rot);flame(d.x-a.x*d.r.H/2*k,d.y-a.y*d.r.H/2*k,a,h,.45,false);}
      if(d.chunk){ctx.save();ctx.globalAlpha=al;ctx.translate(d.x,d.y);ctx.rotate(d.rot*Math.PI/180);ctx.fillStyle=d.chunk;ctx.fillRect(-d.w/2,-d.h/2,d.w,d.h);ctx.restore();
        if(d.burn&&d.life<d.burn&&Math.random()<.7)parts.push({x:d.x,y:d.y,vx:(Math.random()-.5)*20,vy:(Math.random()-.5)*20,life:0,max:.5+Math.random()*.6,r:1.5+Math.random()*2,f:Math.random()<.5?1:0,a:.6,grow:8});}
      else drawImgAt(d.r,d.x,d.y,d.rot,al);}
    ctx.globalAlpha=1;
  }
  function separate(kNew,pitch){
    const old=fairOn?up[kNew-1]:upNF[kNew-1],hd=drop[kNew-1].H,Hs=old.H,a=axis(pitch),c=C();
    const off=(hd-Hs)/2*k;
    debris.push({r:drop[kNew-1],x:c.x+a.x*off,y:c.y+a.y*off,vx:-a.x*30,vy:-a.y*30,ax:-a.x*90,ay:-a.y*90+40,rot:pitch,vr:(Math.random()-.5)*8,life:0,max:6,flip:kNew===1&&pr.legs,flipTo:pitch+170});
    for(let i=0;i<26;i++){const an=Math.random()*7,sp=20+Math.random()*80;parts.push({x:c.x+a.x*(off+hd/2*k),y:c.y+a.y*(off+hd/2*k),vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,life:0,max:.6+Math.random()*.6,r:2+Math.random()*3,f:0,a:.7,col:"#eef"});}
    shiftFrom=hd/2;shiftT=0;kT=kFor(kNew);shake=Math.max(shake,.25);thump(.6,.5,500);
  }
  function jettisonFairing(pitch){
    if(!fairL)return;const cur=up[stageIdx],a=axis(pitch),c=C(),fh=rwFairH(pr.payload)/2,off=(cur.H/2-fh)*k,nx=a.y,ny=-a.x;
    [[fairL,-1],[fairR,1]].forEach(([r,sgn])=>debris.push({r:Object.assign({H:rwFairH(pr.payload)},r),x:c.x+a.x*off,y:c.y+a.y*off,vx:sgn*nx*-60-a.x*20,vy:sgn*ny*-60-a.y*20,ax:-a.x*60,ay:-a.y*60+30,rot:pitch,vr:sgn*-38,life:0,max:4.5}));
  }
  /* the exposed satellite breaks up at Max-Q: fireball, smoke and tumbling pieces */
  function explode(pitch){
    const cur=curImg(),a=axis(pitch),c=C(),L=cur.H*k,ox=c.x+a.x*L*.35,oy=c.y+a.y*L*.35;
    for(let i=0;i<170;i++){const an=Math.random()*7,sp=30+Math.random()*300;parts.push({x:ox+(Math.random()-.5)*RW_D*k,y:oy+(Math.random()-.5)*RW_D*k,vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,life:0,max:.7+Math.random()*1.3,r:4+Math.random()*10,f:1,fx:1,drag:2.2,grow:22});}
    for(let i=0;i<70;i++){const an=Math.random()*7,sp=10+Math.random()*120;parts.push({x:ox,y:oy,vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,life:0,max:3+Math.random()*3,r:10+Math.random()*14,f:0,a:.55,drag:1.4,grow:18,col:Math.random()<.5?"#8d8a99":"#c9c6d4"});}
    if(noPay)debris.push({r:noPay,x:c.x-a.x*(L*.12),y:c.y-a.y*(L*.12),vx:-a.x*10+(Math.random()-.5)*30,vy:-a.y*10,ax:0,ay:70,rot:pitch,vr:(Math.random()<.5?-1:1)*(40+Math.random()*40),life:0,max:9});
    const cols=["#e9e4f6","#d9a63a","#c7a24a","#5d6fb8","#9a95b3","#3b3550"];
    for(let i=0;i<26;i++){const an=Math.random()*7,sp=60+Math.random()*260;debris.push({chunk:cols[i%cols.length],w:2+Math.random()*k*1.4,h:2+Math.random()*k*.9,x:ox,y:oy,vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,ax:0,ay:90,rot:Math.random()*360,vr:(Math.random()-.5)*720,life:0,max:4+Math.random()*4,burn:1+Math.random()*2});}
    flash=1.3;shake=1.2;thump(1.4,2.6,260);thump(.8,1.2,1400);
  }
  function splash(pitch){
    const c=C(),a=axis(pitch),cur=curImg(),gy=groundY(0,pitch),x=c.x+a.x*cur.H*k*.5;
    for(let i=0;i<120;i++){const an=-Math.PI/2+(Math.random()-.5)*1.3,sp=80+Math.random()*320;parts.push({x:x+(Math.random()-.5)*20,y:gy,vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,g:420,life:0,max:1.2+Math.random()*1.2,r:2+Math.random()*4,f:0,a:.9,grow:3,col:Math.random()<.6?"#eaf6ff":"#9fd0ff"});}
    for(let i=0;i<30;i++)parts.push({x:x+(Math.random()-.5)*60,y:gy-4,vx:(Math.random()-.5)*60,vy:-10-Math.random()*20,life:0,max:2.5+Math.random()*2,r:8+Math.random()*10,f:0,a:.5,grow:14,col:"#f4f8ff"});
    shake=.5;splashed=true;thump(.7,1.6,900);
  }
  /* picture-in-picture: the first stage coming back down onto its landing pad */
  const lpuffs=[];let lastTau=99;
  function landCam(tau,dt){
    if(!F.land||tau>34||tau<-7)return;
    const iw=Math.min(230,W*.36),ih=Math.round(iw*.74),x0=12,y0=H-12-ih,yg=y0+ih*.84,r=drop[0],ki=ih*.48/r.H,f=ki/S6,cx0=x0+iw/2;
    ctx.save();ctx.beginPath();ctx.roundRect?ctx.roundRect(x0,y0,iw,ih,12):ctx.rect(x0,y0,iw,ih);ctx.clip();
    const g=ctx.createLinearGradient(0,y0,0,yg);g.addColorStop(0,"#1c3f8f");g.addColorStop(1,"#86bce9");ctx.fillStyle=g;ctx.fillRect(x0,y0,iw,ih);
    ctx.fillStyle="#2f6b45";ctx.fillRect(x0,yg,iw,ih);ctx.fillStyle="#7d7894";ctx.fillRect(cx0-iw*.22,yg-2,iw*.44,5);
    ctx.strokeStyle="#ffd796";ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(cx0,yg,iw*.09,2.2,0,0,7);ctx.stroke();
    const alt=tau>0?ih*1.15*Math.pow(tau/34,1.5):0,cx=cx0+(tau>0?Math.sin(tau*.25)*iw*.08*tau/34:0),yb=yg-1-alt;
    const burn=(tau>0&&tau<9)||(tau>27&&tau<31);
    if(burn){ctx.save();ctx.globalCompositeOperation="lighter";const L=ih*(.16+.06*Math.random())*(tau<9?1:.8),fg=ctx.createLinearGradient(0,yb,0,yb+L);fg.addColorStop(0,"rgba(255,255,235,.95)");fg.addColorStop(.4,"rgba(255,190,90,.75)");fg.addColorStop(1,"rgba(255,110,50,0)");ctx.fillStyle=fg;ctx.beginPath();ctx.moveTo(cx-RW_D*ki*.25,yb);ctx.quadraticCurveTo(cx-RW_D*ki*.5,yb+L*.5,cx,yb+L);ctx.quadraticCurveTo(cx+RW_D*ki*.5,yb+L*.5,cx+RW_D*ki*.25,yb);ctx.fill();ctx.restore();
      if(alt<ih*.3)for(let i=0;i<2;i++)lpuffs.push({x:cx+(Math.random()-.5)*10,y:yg-2,vx:(Math.random()<.5?-1:1)*(15+Math.random()*40),r:3+Math.random()*4,life:0,max:1.5+Math.random()});}
    if(lastTau>0&&tau<=0)for(let i=0;i<24;i++)lpuffs.push({x:cx+(Math.random()-.5)*20,y:yg-2,vx:(Math.random()<.5?-1:1)*(20+Math.random()*60),r:4+Math.random()*5,life:0,max:2+Math.random()*1.5});
    lastTau=tau;
    for(let i=lpuffs.length-1;i>=0;i--){const p=lpuffs[i];p.life+=dt;if(p.life>p.max){lpuffs.splice(i,1);continue;}p.x+=p.vx*dt;p.vx*=.97;p.r+=dt*9;ctx.globalAlpha=.6*(1-p.life/p.max);ctx.fillStyle="#e4e1ec";ctx.beginPath();ctx.arc(p.x,p.y-p.r*.4,p.r,0,7);ctx.fill();}
    ctx.globalAlpha=1;if(r.img)ctx.drawImage(r.img,cx-r.w*f/2,yb+2*S6*f-r.h*f,r.w*f,r.h*f);
    ctx.fillStyle="rgba(5,3,22,.6)";ctx.fillRect(x0,y0,iw,22);ctx.fillStyle="#fff";ctx.font=`600 12px ${getComputedStyle(document.body).fontFamily}`;ctx.textAlign="right";ctx.fillText("كاميرا الهبوط: المرحلة الأولى",x0+iw-8,y0+15);
    if(tau<=0){ctx.fillStyle="#4fe3a1";ctx.font=`700 ${Math.round(ih*.13)}px ${getComputedStyle(document.body).fontFamily}`;ctx.textAlign="center";ctx.fillText("هبطت بأمان!",cx0,y0+22+ih*.15);}
    ctx.restore();ctx.strokeStyle="rgba(255,255,255,.4)";ctx.lineWidth=1.2;ctx.beginPath();ctx.roundRect?ctx.roundRect(x0+.5,y0+.5,iw-1,ih-1,12):ctx.rect(x0,y0,iw,ih);ctx.stroke();
  }
  function curImg(){if(failed&&noPay&&stageIdx===0)return noPay;return fairOn?up[stageIdx]:upNF[stageIdx];}
  function ascent(dt){
    const s=F.sample(Math.max(0,t)),h=t<0?0:s.h,pitch=t<0?0:s.pitch,a=axis(pitch),c=C();
    if(t>=0&&s.stage>stageIdx){for(let q=stageIdx+1;q<=s.stage;q++)separate(q,pitch);stageIdx=s.stage;}
    if(fairOn&&F.tFair!=null&&t>=F.tFair){jettisonFairing(pitch);fairOn=false;}
    if(F.fail&&!failed&&t>=F.tFail){explode(pitch);failed=true;}
    shift+=s.v*Math.sin(pitch*Math.PI/180)*dt*40;
    k+=(kT-k)*Math.min(1,dt*1.1);
    drawSky(h);drawClouds(h);
    const gy=drawGround(h,pitch);drawPuffs(gy,dt);
    drawStreaks(h,s.v,pitch,dt);
    drawDebris(dt,h);
    shiftT=Math.min(1,shiftT+dt/1.1);const sh=shiftFrom*(1-(1-Math.pow(1-shiftT,3)));
    let cx=c.x+a.x*sh*k,cy=c.y+a.y*sh*k;
    if(F.kind==="pad"&&t>0&&t<4.5){cx+=(Math.random()-.5)*2.4;cy+=(Math.random()-.5)*1.6;}
    const cur=curImg(),bx=cx-a.x*cur.H/2*k,by=cy-a.y*cur.H/2*k;
    const burning=!failed&&t>=tIgn&&(t<0||(F.kind==="pad"?t<4.5:s.burn));
    const eng=RW_PARTS[pr.stages[Math.min(stageIdx,n-1)][0]],full=F.kind==="pad"?.7:Math.min(1.3,.55+(eng.k||1)*.08),power=t<0?full*(.3+.7*Math.max(0,(t-tIgn)/-tIgn)):full;
    engineVol(burning?Math.min(1,power)*(h<70?1-h/100:.3):0);
    if(burning){emit(bx,by,a,h,dt,power);if(t<14&&h<.4)for(let i=0;i<3;i++)puffs.push({x:c.x+(Math.random()-.5)*20,alt:0,vx:(Math.random()<.5?-1:1)*(60+Math.random()*140),r:10+Math.random()*10,life:0,max:3+Math.random()*2});}
    drawParts(dt);
    if(!failed&&!splashed){
      if(burning)flame(bx,by,a,h,power,!!eng.vac);
      vaporCone(cx,cy,a,cur,s.v,h);
      drawImgAt(cur,cx,cy,pitch);
      /* re-entry glow on the falling rocket */
      if(F.kind==="sub"&&t>F.burnEnd&&pitch>95&&h<95&&s.v>1.2){const u=Math.min(1,(s.v-1.2)/3)*Math.max(0,1-Math.abs(h-55)/45),fx=cx+a.x*cur.H/2*k,fy=cy+a.y*cur.H/2*k,R=RW_D*k*2.4;
        if(u>0){ctx.save();ctx.globalCompositeOperation="lighter";const g=ctx.createRadialGradient(fx,fy,0,fx,fy,R);g.addColorStop(0,`rgba(255,240,200,${.9*u})`);g.addColorStop(.4,`rgba(255,140,60,${.55*u})`);g.addColorStop(1,"rgba(255,80,40,0)");ctx.fillStyle=g;ctx.beginPath();ctx.arc(fx,fy,R,0,7);ctx.fill();ctx.restore();
          if(Math.random()<u)parts.push({x:fx,y:fy,vx:-a.x*200+(Math.random()-.5)*40,vy:-a.y*200+(Math.random()-.5)*40,life:0,max:.4+Math.random()*.4,r:2+Math.random()*3,f:1});}}
    }
    hudSet(t,h,s.v,failed?"—":`${Math.min(n,s.stage+1)} من ${n}`,failed?0:s.fuel);return s;
  }
  /* the burn from Earth orbit toward the Moon, seen close up */
  function tliScene(dt){
    const u=Math.min(1,phT/TLI),pitch=sIns.pitch,a=axis(pitch),c=C(),cur=curImg(),on=phT<TLI;
    k+=(kT-k)*Math.min(1,dt*1.1);shift+=(7.8+3.1*u)*Math.sin(pitch*Math.PI/180)*dt*14;
    drawSky(200);drawDebris(dt,200);
    const bx=c.x-a.x*cur.H/2*k,by=c.y-a.y*cur.H/2*k,eng=RW_PARTS[pr.stages[stageIdx][0]];
    if(on)emit(bx,by,a,200,dt,1);
    drawParts(dt);if(on)flame(bx,by,a,200,1,!!eng.vac);
    drawImgAt(cur,c.x,c.y,pitch);engineVol(on?.35:0);
  }
  /* payload separation once the rocket reaches orbital speed */
  function deployScene(dt){
    const deployT=phT,s=sIns,pitch=s.pitch,a=axis(pitch),c=C(),hs=topNoPay?topNoPay.H:0,hp=payImg?payImg.H:0;
    k+=(kT-k)*Math.min(1,dt*1.1);shift+=7.8*Math.sin(pitch*Math.PI/180)*dt*12;
    drawSky(200);drawDebris(dt,200);drawParts(dt);
    const u=Math.max(0,deployT-.6),gap=u*u*5+u*10;
    if(topNoPay)drawImgAt(topNoPay,c.x-a.x*(hp/2*k+gap*.25),c.y-a.y*(hp/2*k+gap*.25),pitch+u*3);
    if(payImg)drawImgAt(payImg,c.x+a.x*(hs/2*k+gap),c.y+a.y*(hs/2*k+gap),pitch-u*2);
    if(deployT>.6&&!dPuff){dPuff=1;for(let i=0;i<14;i++){const an=Math.random()*7,sp=15+Math.random()*40;parts.push({x:c.x+a.x*(hs-hp)/2*k,y:c.y+a.y*(hs-hp)/2*k,vx:Math.cos(an)*sp,vy:Math.sin(an)*sp,life:0,max:.8,r:1.5+Math.random()*2,f:0,a:.8,grow:3,col:"#fff"});}}
  }
  let dPuff=0;
  /* the map: Earth, the 200 km orbit and, for Moon missions, the path to the Moon (not to scale) */
  function mapScene(dt,mode){
    mapRot+=dt*.05;const ex=W*.6,ey=H*.56,R=Math.min(W,H)*.25,ro=R*1.32,mxp=W*.13,myp=H*.66,mr=Math.min(W,H)*.06,thm=Math.atan2(ey-myp,mxp-ex),php=thm+Math.PI;
    const fnt=getComputedStyle(document.body).fontFamily;
    ctx.fillStyle="#02030b";ctx.fillRect(-20,-20,W+40,H+40);ctx.fillStyle="#fff";stars.forEach(s=>{ctx.globalAlpha=s.a;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,7);ctx.fill();});ctx.globalAlpha=1;
    const eg=ctx.createRadialGradient(ex-R*.35,ey-R*.35,R*.1,ex,ey,R);eg.addColorStop(0,"#5aa2ec");eg.addColorStop(.7,"#1f5aa8");eg.addColorStop(1,"#0b2a5a");
    ctx.fillStyle=eg;ctx.beginPath();ctx.arc(ex,ey,R,0,7);ctx.fill();
    ctx.save();ctx.beginPath();ctx.arc(ex,ey,R,0,7);ctx.clip();ctx.fillStyle="rgba(84,160,96,.75)";[[-.3,-.2,.28,.16],[.25,.1,.22,.3],[-.05,.38,.3,.12],[.6,-.4,.2,.12]].forEach(([x,y,w,h])=>{ctx.beginPath();ctx.ellipse(ex+((x+mapRot+1)%2-1)*R,ey+y*R,w*R,h*R,.4,0,7);ctx.fill();});ctx.restore();
    const sh=ctx.createLinearGradient(ex-R,0,ex+R,0);sh.addColorStop(.55,"rgba(0,0,10,0)");sh.addColorStop(1,"rgba(0,0,10,.65)");ctx.fillStyle=sh;ctx.beginPath();ctx.arc(ex,ey,R,0,7);ctx.fill();
    ctx.strokeStyle="rgba(126,196,255,.5)";ctx.lineWidth=4;ctx.beginPath();ctx.arc(ex,ey,R+2,0,7);ctx.stroke();
    ctx.setLineDash([4,6]);ctx.strokeStyle="rgba(200,190,255,.4)";ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(ex,ey,ro,0,7);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle="#cfe6ff";ctx.font=`600 13px ${fnt}`;ctx.textAlign="center";ctx.fillText("الأرض",ex,ey+R+22);
    if(F.moon){ctx.fillStyle="#e9e4cf";ctx.beginPath();ctx.arc(mxp,myp,mr,0,7);ctx.fill();ctx.fillStyle="#cfc8ad";[[-.3,-.2,.22],[.25,.2,.16],[.1,-.35,.1]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(mxp+x*mr,myp+y*mr,r*mr,0,7);ctx.fill();});ctx.fillStyle="#f1ead2";ctx.fillText("القمر",mxp,myp+mr+18);}
    let px,py,glow=0;
    const arc=(a0,a1)=>{ctx.strokeStyle="rgba(255,215,150,.85)";ctx.lineWidth=2.4;ctx.beginPath();ctx.arc(ex,ey,ro,-a1,-a0,false);ctx.stroke();};
    if(mode==="orbit"){const ang=Math.PI*.75+phT*1.05;px=ex+ro*Math.cos(ang);py=ey-ro*Math.sin(ang);arc(ang-Math.min(phT*1.05,2.2),ang);}
    else if(mode==="park"){const ang=php-Math.PI+Math.PI*Math.min(1,phT/PARK);px=ex+ro*Math.cos(ang);py=ey-ro*Math.sin(ang);arc(ang-Math.min(phT*.26,1.6),ang);}
    else{const r2=Math.hypot(mxp-ex,myp-ey)-mr*1.35,aa=(ro+r2)/2,e=(r2-ro)/(r2+ro),rd=th=>aa*(1-e*e)/(1+e*Math.cos(th)),P=th=>[ex+rd(th)*Math.cos(php+th),ey-rd(th)*Math.sin(php+th)];
      ctx.setLineDash([3,5]);ctx.strokeStyle="rgba(255,215,150,.5)";ctx.lineWidth=1.4;ctx.beginPath();for(let q=0;q<=80;q++){const [x,y]=P(Math.PI*q/80);q?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();ctx.setLineDash([]);
      const tt=mode==="arrive"?TR.T:ttTrans(phT/TRANS),fr=Math.max(0,Math.min(1,(TR.rAt(tt)-TR.r1)/(TR.rm-TR.r1))),want=ro+fr*(r2-ro),th=Math.acos(Math.max(-1,Math.min(1,(aa*(1-e*e)/want-1)/e)));
      ctx.strokeStyle="rgba(255,215,150,.9)";ctx.lineWidth=2.4;ctx.beginPath();for(let q=0;q<=60;q++){const [x,y]=P(th*q/60);q?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();
      [px,py]=P(th);glow=mode==="transfer"?Math.max(0,1-phT/1.5):0;
      if(mode==="arrive"){const u=(phT%1.4)/1.4;ctx.strokeStyle=`rgba(79,227,161,${.8*(1-u)})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(mxp,myp,mr*1.2+u*mr*1.4,0,7);ctx.stroke();}}
    const gr=12+glow*14,gl=ctx.createRadialGradient(px,py,0,px,py,gr);gl.addColorStop(0,"rgba(255,255,230,1)");gl.addColorStop(1,glow?"rgba(255,150,70,0)":"rgba(255,215,150,0)");ctx.fillStyle=gl;ctx.beginPath();ctx.arc(px,py,gr,0,7);ctx.fill();
    ctx.fillStyle="#ffb347";ctx.strokeStyle="#2a1600";ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(px,py,3.4,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle="#bdb3e6";ctx.font=`400 11px ${fnt}`;ctx.textAlign="left";ctx.fillText("الرسم ليس بمقياس حقيقي",12,H-12);
  }
  function drawMini(){
    const w=mini.width/dpr,h=mini.height/dpr;mx.clearRect(0,0,w,h);mx.fillStyle="rgba(10,7,30,.72)";mx.fillRect(0,0,w,h);
    if(F.kind==="pad")return;
    const T=F.tEnd,Y=Math.max(220,F.apogee*1.1),X=v=>6+v/T*(w-12),Yp=v=>h-8-v/Y*(h-16);
    mx.setLineDash([3,3]);mx.strokeStyle="rgba(255,215,150,.6)";mx.beginPath();mx.moveTo(4,Yp(100));mx.lineTo(w-4,Yp(100));mx.stroke();mx.setLineDash([]);
    mx.fillStyle="#ffd796";mx.font="9px sans-serif";mx.textAlign="right";mx.fillText("100 km",w-6,Yp(100)-3);
    mx.strokeStyle="#c4abff";mx.lineWidth=1.8;mx.beginPath();const tt=Math.min(Math.max(0,t),T);for(let q=0;q<=80;q++){const x=tt*q/80,s=F.sample(x);q?mx.lineTo(X(x),Yp(s.h)):mx.moveTo(X(x),Yp(s.h));}mx.stroke();
    const sN=F.sample(tt);mx.fillStyle="#ffd796";mx.beginPath();mx.arc(X(tt),Yp(sN.h),2.6,0,7);mx.fill();
  }
  function endMsg(){
    if(F.kind==="pad")return ["أُلغي الإطلاق","bad"];
    if(F.fail)return ["فشلت المهمة","bad"];
    if(F.apogee>=100)return goal==="space"?["نجحت المهمة!","go"]:["عاد إلى الأرض","bad"];
    return ["لم يصل إلى الفضاء","bad"];
  }
  function toPhase(p,fd){phase=p;phT=0;if(fd)fade=1;}
  function frame(now){
    const dtR=Math.min(.05,(now-last)/1000||0);last=now;const dt=paused?0:dtR,dS=phase==="count"?dt:dt*speed;
    ctx.save();if(shake>0&&!still){ctx.translate((Math.random()-.5)*shake*9,(Math.random()-.5)*shake*9);shake=Math.max(0,shake-dt*1.4);}
    if(phase==="count"){t+=dt;const c=Math.ceil(-t);
      if(c!==lastBeep&&c>0){lastBeep=c;beep(880,.18);}
      if(!ignLogged&&t>=tIgn&&F.kind!=="pad"){ignLogged=true;pushLog({t:tIgn,txt:"إشعال المحركات: يزداد الدفع والصاروخ مثبت على المنصة"});}
      if(t>=tIgn&&t<0&&F.kind!=="pad")shake=Math.max(shake,.12);
      bigMsg(t<0?String(Math.max(1,c)):"","count");
      if(t>=0){t=0;tau=0;phase="ascent";if(F.kind==="pad"){bigMsg("");}else{shake=.6;beep(1320,.4,.22);bigMsg("إقلاع!","go");}setTimeout(()=>{if(big.textContent==="إقلاع!")bigMsg("");},1300);}
      ascent(dt);}
    else if(phase==="ascent"){
      tau+=dS;t=tAt(tau);
      while(evI<F.ev.length&&F.ev[evI].t<=t){const e=F.ev[evI++];if(F.kind==="orbit"&&e.t>F.tEnd+.01){evI--;break;}pushLog(e);}
      const end=F.tEnd;
      ascent(dt);
      if(F.land&&F.tLand<=F.tEnd)landCam(F.tLand-t,dt);
      if(t>=end){
        if(F.kind==="orbit"){engineVol(0);beep(660,.25,.2);setTimeout(()=>beep(990,.4,.2),180);bigMsg("في المدار!","go");setTimeout(()=>{if(big.textContent==="في المدار!")bigMsg("");},1800);
          while(evI<F.ev.length&&F.ev[evI].t<=F.tEnd+.01)pushLog(F.ev[evI++]);
          stageIdx=insStage;postT=0;
          if(F.moon){toPhase("park",true);pushLog({t:F.tEnd+60,txt:"يدور حول الأرض وينتظر الموضع المناسب للانطلاق نحو القمر"});}
          else toPhase("deploy");}
        else if(F.fail){phase="boom";boomT=0;}
        else{if(F.kind==="sub")splash(F.sample(t).pitch);phase="end";endT=0;const [m,c]=endMsg();setTimeout(()=>bigMsg(m,c),F.kind==="sub"?700:0);sendDone();}
      }
    }else if(phase==="boom"){boomT+=dt;ascent(dt);if(boomT>2.4){phase="end";const [m,c]=endMsg();bigMsg(m,c);sendDone();}}
    else if(phase==="end"){endT+=dt;ascent(dt);}
    else{
      phT+=dS;postT+=dS;const T0=F.tEnd,stg=`${insStage+1} من ${n}`;
      if(phase==="deploy"&&!F.moon){deployScene(dS);hudSet(T0+phT*20,200,7.8,"الحمولة",0);
        if(phT>=3&&!dLog){dLog=1;pushLog({t:T0+60,txt:`انفصلت الحمولة: ${RW_PARTS[pr.payload].n}`,k:"ok"});}
        if(phT>=DEP)toPhase("orbit",true);}
      else if(phase==="orbit"){mapScene(dS,"orbit");hudSet(T0+DEP*20+phT*900,200,7.8,"الحمولة",0);if(phT>ORB&&!doneSent)sendDone();}
      else if(phase==="park"){mapScene(dS,"park");hudSet(T0+phT*225,200,7.8,stg,f0);
        if(phT>=PARK){toPhase("tli",true);bigMsg("الانطلاق نحو القمر","go");setTimeout(()=>{if(big.textContent==="الانطلاق نحو القمر")bigMsg("");},2200);beep(990,.3,.2);pushLog({t:T0+2700,txt:"تشغيل المحرك من جديد للانطلاق نحو القمر",k:"ok"});}}
      else if(phase==="tli"){tliScene(dS);const u=Math.min(1,phT/TLI);hudSet(T0+2700+Math.min(phT,TLI)*33,200,7.8+3.1*u,stg,f0*(1-fracTLI*u));
        if(phT>=TLI&&!tLog){tLog=1;engineVol(0);pushLog({t:T0+3030,txt:"انطفأ المحرك: السرعة 10.9 كم/ث، وهي تكفي للوصول إلى القمر",k:"ok"});}
        if(phT>=TLI+1.2)toPhase("deploy");}
      else if(phase==="deploy"){deployScene(dS);const tt=TT0*Math.min(1,phT/DEP),r=TR.rAt(tt);hudSet(T0+3030+tt,r-RW_RE,TR.vAt(r),"المسبار",0);
        if(phT>=1&&!dLog){dLog=1;pushLog({t:T0+3060,txt:"انفصل المسبار عن المرحلة الأخيرة",k:"ok"});}
        if(phT>=DEP)toPhase("transfer",true);}
      else if(phase==="transfer"){mapScene(dS,"transfer");const tt=ttTrans(phT/TRANS),r=TR.rAt(tt);hudSet(T0+3030+tt,r-RW_RE,TR.vAt(r),"المسبار",0);
        while(tmI<TMARK.length&&r>=TMARK[tmI][0])pushLog({t:T0+3030+tt,txt:TMARK[tmI++][1]});
        if(phT>=TRANS){toPhase("arrive");pushLog({t:T0+3030+TR.T,txt:"وصل المسبار إلى القمر بعد نحو 3 أيام",k:"ok"});bigMsg("وصل إلى القمر!","go");beep(660,.25,.2);setTimeout(()=>beep(990,.5,.2),180);}}
      else if(phase==="arrive"){mapScene(dS,"arrive");hudSet(T0+3030+TR.T,TR.rm-RW_RE,TR.vAt(TR.rm),"المسبار",0);if(phT>ARR&&!doneSent)sendDone();}
      if(F.land&&F.tLand>F.tEnd){const tau_=34-postT*7;landCam(tau_,dS);if(tau_<=0&&!landLogged){landLogged=1;pushLog({t:F.tLand,txt:"هبطت المرحلة الأولى بنجاح على منصة الهبوط!",k:"ok"});}}
    }
    if(flash>0){ctx.fillStyle=`rgba(255,240,200,${Math.min(1,flash)*.6})`;ctx.fillRect(-20,-20,W+40,H+40);flash=Math.max(0,flash-dt*1.8);}
    if(fade>0){ctx.fillStyle=`rgba(2,3,11,${fade})`;ctx.fillRect(-20,-20,W+40,H+40);fade=Math.max(0,fade-dt*1.6);}
    ctx.restore();
    drawMini();
    raf=requestAnimationFrame(frame);
  }
  let dLog=0,tLog=0;
  function sendDone(){if(doneSent)return;doneSent=true;engineVol(0);cb.done();}
  const api={
    stop(){cancelAnimationFrame(raf);removeEventListener("resize",size);if(SND.ctx){try{SND.ctx.close();}catch(_){}SND.ctx=null;}},
    toggle(){paused=!paused;if(SND.ctx){try{paused?SND.ctx.suspend():SND.ctx.resume();}catch(_){}}return paused;},
    sound(on){SND.on=on;store.set("ufuq-rw-snd",on);if(on){sndInit();if(SND.ctx&&SND.ctx.state==="suspended"&&!paused)SND.ctx.resume();}else engineVol(0);return on;},
    speed(v){speed=v;},
    skip(){if(doneSent)return;while(evI<F.ev.length)pushLog(F.ev[evI++]);t=F.tEnd;tau=PACE?PACE.total:t;fade=0;
      if(F.kind==="orbit"){stageIdx=insStage;postT=99;
        if(F.moon){phase="arrive";phT=ARR;pushLog({t:F.tEnd+2700,txt:"تشغيل المحرك من جديد للانطلاق نحو القمر",k:"ok"});pushLog({t:F.tEnd+3030+TR.T,txt:"وصل المسبار إلى القمر بعد نحو 3 أيام",k:"ok"});bigMsg("وصل إلى القمر!","go");}
        else{phase="orbit";phT=ORB;pushLog({t:F.tEnd+60,txt:`انفصلت الحمولة: ${RW_PARTS[pr.payload].n}`,k:"ok"});bigMsg("في المدار!","go");}
        if(F.land&&F.tLand>F.tEnd&&!landLogged){landLogged=1;pushLog({t:F.tLand,txt:"هبطت المرحلة الأولى بنجاح على منصة الهبوط!",k:"ok"});}}
      else{phase="end";stageIdx=Math.min(n-1,F.sample(t).stage);k=kT=kFor(stageIdx);fairOn=fairOn&&F.tFair==null;if(F.fail)failed=true;if(F.kind==="sub")splashed=true;const [m,c]=endMsg();bigMsg(m,c);}
      engineVol(0);sendDone();}
  };
  if(still){api.skip();staticReady=true;staticDraw();
    /* one static frame only */
    return Object.assign(api,{stop(){removeEventListener("resize",size);}});}
  sndInit();
  last=performance.now();raf=requestAnimationFrame(frame);
  return api;
}
