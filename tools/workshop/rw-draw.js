/* ---------- rocket workshop: drawing the parts (SVG, also rasterised for the flight canvas) ---------- */
const RW_D=3.7;/* body diameter, m */
const RW_DEFS=`<defs>
<linearGradient id="rwg-cyl" x1="0" x2="1"><stop offset="0" stop-color="#9f99bd"/><stop offset=".18" stop-color="#e6e2f3"/><stop offset=".45" stop-color="#ffffff"/><stop offset=".78" stop-color="#d6d2e8"/><stop offset="1" stop-color="#8b85a8"/></linearGradient>
<linearGradient id="rwg-metal" x1="0" x2="1"><stop offset="0" stop-color="#48455a"/><stop offset=".35" stop-color="#a19db4"/><stop offset=".52" stop-color="#e2dfee"/><stop offset=".72" stop-color="#8a869f"/><stop offset="1" stop-color="#3a374b"/></linearGradient>
<linearGradient id="rwg-dark" x1="0" x2="1"><stop offset="0" stop-color="#15111f"/><stop offset=".5" stop-color="#3a3450"/><stop offset="1" stop-color="#110d1b"/></linearGradient>
<linearGradient id="rwg-gold" x1="0" x2="1"><stop offset="0" stop-color="#9a6a18"/><stop offset=".45" stop-color="#f7d57e"/><stop offset=".7" stop-color="#c9973a"/><stop offset="1" stop-color="#7d5410"/></linearGradient>
<linearGradient id="rwg-vac" x1="0" x2="1"><stop offset="0" stop-color="#231d36"/><stop offset=".42" stop-color="#6c6390"/><stop offset=".55" stop-color="#8e86b0"/><stop offset="1" stop-color="#1e1930"/></linearGradient>
<linearGradient id="rwg-panel" x1="0" x2="1"><stop offset="0" stop-color="#16306e"/><stop offset=".5" stop-color="#3567c9"/><stop offset="1" stop-color="#132a60"/></linearGradient>
</defs>`;
const rwF=n=>n.toFixed(1);
function rwBell(cx,top,bot,wt,wb,fill){const h=bot-top;return `<path d="M${rwF(cx-wt/2)} ${rwF(top)} C${rwF(cx-wt/2)} ${rwF(top+h*.45)} ${rwF(cx-wb/2)} ${rwF(bot-h*.25)} ${rwF(cx-wb/2)} ${rwF(bot)} L${rwF(cx+wb/2)} ${rwF(bot)} C${rwF(cx+wb/2)} ${rwF(bot-h*.25)} ${rwF(cx+wt/2)} ${rwF(top+h*.45)} ${rwF(cx+wt/2)} ${rwF(top)}Z" fill="${fill}"/><ellipse cx="${rwF(cx)}" cy="${rwF(bot)}" rx="${rwF(wb/2)}" ry="${rwF(Math.max(.6,wb*.08))}" fill="#1a1626" opacity=".85"/>`;}
/* one part, bottom at y=yb, centred at x=cx, s px per metre */
function rwPart(id,cx,yb,s,o={}){
  const P=RW_PARTS[id],W=RW_D*s,h=o.hp!=null?o.hp:(P.h||0)*s,yt=yb-h,x=cx-W/2;let g="";
  if(P.cat==="eng"&&!P.vac){
    g+=`<rect x="${rwF(x)}" y="${rwF(yt)}" width="${rwF(W)}" height="${rwF(1.1*s)}" fill="url(#rwg-dark)"/>`;
    const top=yt+1.1*s;
    if(P.k===1)g+=rwBell(cx,top,yb,1.1*s,2.5*s,"url(#rwg-metal)");
    else if(P.k===3)[-1.22,0,1.22].forEach(d=>g+=rwBell(cx+d*s,top,yb,.62*s,1.18*s,"url(#rwg-metal)"));
    else{[-.62,.62].forEach(d=>g+=rwBell(cx+d*s,top,yb-.25*s,.5*s,.95*s,"#5c586f"));[-1.3,0,1.3].forEach(d=>g+=rwBell(cx+d*s,top,yb,.52*s,1.02*s,"url(#rwg-metal)"));}
  }else if(P.vac){
    g+=`<rect x="${rwF(cx-W*.32)}" y="${rwF(yt)}" width="${rwF(W*.64)}" height="${rwF(.9*s)}" fill="url(#rwg-dark)"/>`;
    g+=rwBell(cx,yt+.9*s,yb,.9*s,3.3*s,"url(#rwg-vac)");
    g+=`<path d="M${rwF(cx-1.65*s)} ${rwF(yb)} h${rwF(3.3*s)}" stroke="#b8b0d8" stroke-width="${rwF(Math.max(.6,.12*s))}"/>`;
  }else if(P.cat==="tank"){
    g+=`<rect x="${rwF(x)}" y="${rwF(yt)}" width="${rwF(W)}" height="${rwF(h)}" fill="url(#rwg-cyl)"/>`;
    g+=`<path d="M${rwF(x)} ${rwF(yt+.35*s)} h${rwF(W)} M${rwF(x)} ${rwF(yb-.35*s)} h${rwF(W)}" stroke="#8b85a8" stroke-width="${rwF(Math.max(.5,.08*s))}"/>`;
    if(P.h>15)g+=`<rect x="${rwF(x)}" y="${rwF(yt+h*.42)}" width="${rwF(W)}" height="${rwF(.55*s)}" fill="#7b45ff" opacity=".85"/><path d="M${rwF(x)} ${rwF(yt+h*.62)} h${rwF(W)}" stroke="#b9b3d3" stroke-width="${rwF(Math.max(.5,.06*s))}"/>`;
  }else if(id==="dc"){
    g+=`<rect x="${rwF(x)}" y="${rwF(yt)}" width="${rwF(W)}" height="${rwF(h)}" fill="url(#rwg-dark)"/>`;
    g+=`<path d="M${rwF(x)} ${rwF(yt+h/2)} h${rwF(W)}" stroke="#ffd796" stroke-width="${rwF(Math.max(.6,.1*s))}" stroke-dasharray="${rwF(.5*s)} ${rwF(.35*s)}"/>`;
  }else if(P.cat==="pay")g+=rwPayload(id,cx,yb,s);
  return g;
}
function rwPayload(id,cx,yb,s){
  const P=RW_PARTS[id],h=P.h*s,yt=yb-h;let g="";
  if(id==="p4"){
    const W=RW_D*s,trunk=3.4*s;
    g+=`<rect x="${rwF(cx-W/2)}" y="${rwF(yb-trunk)}" width="${rwF(W)}" height="${rwF(trunk)}" fill="url(#rwg-cyl)"/><rect x="${rwF(cx-W/2)}" y="${rwF(yb-trunk*.75)}" width="${rwF(W)}" height="${rwF(trunk*.45)}" fill="url(#rwg-panel)"/>`;
    const b=yb-trunk;g+=`<path d="M${rwF(cx-W/2)} ${rwF(b)} L${rwF(cx-W*.24)} ${rwF(yt+.7*s)} Q${rwF(cx)} ${rwF(yt-.1*s)} ${rwF(cx+W*.24)} ${rwF(yt+.7*s)} L${rwF(cx+W/2)} ${rwF(b)}Z" fill="url(#rwg-cyl)"/>`;
    g+=`<rect x="${rwF(cx-W/2)}" y="${rwF(b-.35*s)}" width="${rwF(W)}" height="${rwF(.35*s)}" fill="#24203a"/>`;
    [-.55,0,.55].forEach(d=>g+=`<rect x="${rwF(cx+d*s-.22*s)}" y="${rwF(b-2.6*s)}" width="${rwF(.44*s)}" height="${rwF(.5*s)}" rx="${rwF(.1*s)}" fill="#1b1242"/>`);
    return g;
  }
  const bw=(id==="p2"?2.8:id==="p3"?2.0:1.6)*s;
  g+=`<rect x="${rwF(cx-bw/2)}" y="${rwF(yt+(id==="p3"?1.1:.5)*s)}" width="${rwF(bw)}" height="${rwF(h-(id==="p3"?1.1:.5)*s)}" fill="url(#rwg-gold)"/>`;
  g+=`<path d="M${rwF(cx-bw/2)} ${rwF(yt+h*.45)} h${rwF(bw)}" stroke="#8a5c12" stroke-width="${rwF(Math.max(.4,.06*s))}"/>`;
  const pw=.45*s;[-1,1].forEach(k=>g+=`<rect x="${rwF(k<0?cx-bw/2-pw:cx+bw/2)}" y="${rwF(yt+.8*s)}" width="${rwF(pw)}" height="${rwF(h-1.3*s)}" fill="url(#rwg-panel)"/>`);
  if(id==="p3")g+=`<path d="M${rwF(cx-.95*s)} ${rwF(yt+1.1*s)} Q${rwF(cx)} ${rwF(yt-.2*s)} ${rwF(cx+.95*s)} ${rwF(yt+1.1*s)}Z" fill="#ece8f8"/><path d="M${rwF(cx)} ${rwF(yt+.9*s)} v${rwF(-.9*s)}" stroke="#ece8f8" stroke-width="${rwF(Math.max(.5,.08*s))}"/>`;
  else g+=`<path d="M${rwF(cx)} ${rwF(yt+.5*s)} v${rwF(-.5*s)}" stroke="#ece8f8" stroke-width="${rwF(Math.max(.5,.08*s))}"/>${id==="p2"?`<ellipse cx="${rwF(cx)}" cy="${rwF(yt+.2*s)}" rx="${rwF(.8*s)}" ry="${rwF(.25*s)}" fill="#ece8f8"/>`:""}`;
  return g;
}
const rwFairH=pay=>Math.max(10.5,RW_PARTS[pay].h+4.5);
function rwFairing(cx,yb,s,pay,op,half){
  const Wb=RW_D*s,Wf=RW_D*1.4*s,H=rwFairH(pay)*s,cyl=H*.48,ad=1.1*s;let d;
  const L=`M${rwF(cx-Wb/2)} ${rwF(yb)} L${rwF(cx-Wf/2)} ${rwF(yb-ad)} L${rwF(cx-Wf/2)} ${rwF(yb-cyl)} C${rwF(cx-Wf/2)} ${rwF(yb-H*.82)} ${rwF(cx-Wf*.18)} ${rwF(yb-H)} ${rwF(cx)} ${rwF(yb-H)}`;
  const R=`C${rwF(cx+Wf*.18)} ${rwF(yb-H)} ${rwF(cx+Wf/2)} ${rwF(yb-H*.82)} ${rwF(cx+Wf/2)} ${rwF(yb-cyl)} L${rwF(cx+Wf/2)} ${rwF(yb-ad)} L${rwF(cx+Wb/2)} ${rwF(yb)}Z`;
  if(half==="L")d=`${L} L${rwF(cx)} ${rwF(yb)}Z`;
  else if(half==="R")d=`M${rwF(cx)} ${rwF(yb)} L${rwF(cx)} ${rwF(yb-H)} ${R}`;
  else d=`${L} ${R}`;
  return `<path d="${d}" fill="url(#rwg-cyl)" opacity="${op}"/>${half?"":`<path d="M${rwF(cx)} ${rwF(yb-H+.4*s)} V${rwF(yb)}" stroke="#8b85a8" stroke-width="${rwF(Math.max(.5,.07*s))}" opacity="${op}"/><rect x="${rwF(cx-Wf/2)}" y="${rwF(yb-cyl*.55)}" width="${rwF(Wf)}" height="${rwF(.45*s)}" fill="#7b45ff" opacity="${(op*.8).toFixed(2)}"/>`}`;
}
function rwLegs(cx,yb,s,hStage){
  const W=RW_D*s,L=Math.min(hStage*.38,9*s);let g="";
  [-1,1].forEach(k=>{const x=cx+k*W/2;g+=`<path d="M${rwF(x)} ${rwF(yb-.3*s)} L${rwF(x+k*.55*s)} ${rwF(yb-.6*s)} L${rwF(x+k*.55*s)} ${rwF(yb-L)} L${rwF(x)} ${rwF(yb-L+.6*s)}Z" fill="#1c1830" stroke="#5c5674" stroke-width="${rwF(Math.max(.4,.05*s))}"/>`;});
  return g;
}
function rwFins(cx,ytop,s){const W=RW_D*s;let g="";[-1,1].forEach(k=>{const x=cx+k*W/2;g+=`<rect x="${rwF(k<0?x-1.1*s:x)}" y="${rwF(ytop+.6*s)}" width="${rwF(1.1*s)}" height="${rwF(.9*s)}" fill="#2b2640" stroke="#77708f" stroke-width="${rwF(Math.max(.3,.04*s))}"/>`;});return g;}
/* stack geometry: list of {id,i,y0,y1} bottom->top, total height in metres */
function rwLayout(stack){
  let y=0;const out=[];let payIdx=stack.findIndex(id=>RW_PARTS[id].cat==="pay");
  stack.forEach((id,i)=>{const P=RW_PARTS[id];
    if(P.fair){const pay=stack[i-1]&&RW_PARTS[stack[i-1]].cat==="pay"?stack[i-1]:null;
      if(pay){const base=out[out.length-1].y0,top=base+rwFairH(pay);out.push({id,i,y0:base,y1:top,pay});y=Math.max(y,top);}
      else{out.push({id,i,y0:y,y1:y+4,pay:null});y+=4;}
      return;}
    out.push({id,i,y0:y,y1:y+P.h});y+=P.h;});
  return {parts:out,H:y,payIdx};
}
/* the rocket as one SVG string (for the flight canvas); s px per metre */
function rwStackSVG(stack,o){
  const s=o.s||6,L=rwLayout(stack),pad=2*s,Wmax=RW_D*1.6*s+pad*2,Hpx=L.H*s+pad*2,cx=Wmax/2,yb0=Hpx-pad;
  let g="",legsDone=false;
  L.parts.forEach(p=>{const yb=yb0-p.y0*s;
    if(RW_PARTS[p.id].fair){if(p.pay&&o.fair!==false)g+=rwFairing(cx,yb,s,p.pay,1);return;}
    if(RW_PARTS[p.id].cat==="pay"&&o.fair!==false&&stack.includes("fr")&&stack[p.i+1]==="fr")return;
    g+=rwPart(p.id,cx,yb,s);});
  if(o.legs){const st=L.parts.filter(p=>p.i<=o.legsTop);const top=st.length?st[st.length-1].y1:0;g+=rwLegs(cx,yb0,s,top*s)+rwFins(cx,yb0-top*s,s);legsDone=true;}
  return {svg:`<svg xmlns="http://www.w3.org/2000/svg" width="${Math.ceil(Wmax)}" height="${Math.ceil(Hpx)}" viewBox="0 0 ${rwF(Wmax)} ${rwF(Hpx)}">${RW_DEFS}${g}</svg>`,w:Wmax,h:Hpx,s,cx,yb:yb0,H:L.H};
}
function rwThumb(id){
  const P=RW_PARTS[id],h=P.fair?rwFairH("p2"):P.h||1,cx=30,yb=53;let g="";
  const wf={p1:2.5,p3:2.9,p2:3.7,p4:3.7}[id]||(P.vac?3.3:RW_D),s=Math.min(46/Math.max(h,wf*1.25),11);
  if(P.fair)g=rwPayload("p2",cx,yb,s)+rwFairing(cx,yb,s,"p2",.78);
  else if(P.cat==="tank")g=rwPart(id,cx,yb,3.6,{hp:12+P.h*1.12});
  else g=rwPart(id,cx,yb,s);
  return `<svg viewBox="0 0 60 56" aria-hidden="true">${g}</svg>`;
}
function rwLegsThumb(){const s=4.2,cx=30,yb=54,W=RW_D*s;return `<svg viewBox="0 0 60 56" aria-hidden="true"><rect x="${rwF(cx-W/2)}" y="6" width="${rwF(W)}" height="${yb-6}" fill="url(#rwg-cyl)"/>${rwLegs(cx,yb,s,46)}${rwFins(cx,6,s)}</svg>`;}
