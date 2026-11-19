const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const issues=[];const base='file://'+process.cwd()+'/site.html';
const routes=['','#tools','#lab','#rocket','#build','#sky','#solar','#saudi','#quiz','#glossary','#about','#topic-planets','#topic-ai'];
for(const scheme of ['light','dark']){
 const ctx=await b.newContext({viewport:{width:1280,height:900},colorScheme:scheme});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
 for(const h of routes){await p.goto(base+h);await p.waitForTimeout(450);
  const low=await p.evaluate(()=>{
   const P=c=>{const m=c.match(/[\d.]+/g);if(!m)return null;return {r:+m[0],g:+m[1],b:+m[2],a:m[3]==null?1:+m[3]};};
   function bg(el){const layers=[];while(el){const cs=getComputedStyle(el);if(cs.backgroundImage&&cs.backgroundImage!=='none')return null;const c=P(cs.backgroundColor);if(c&&c.a>0){layers.push(c);if(c.a>=.99)break;}el=el.parentElement;}
     let base=layers.length&&layers[layers.length-1].a>=.99?layers.pop():P(getComputedStyle(document.body).backgroundColor);
     for(let i=layers.length-1;i>=0;i--){const l=layers[i];base={r:l.r*l.a+base.r*(1-l.a),g:l.g*l.a+base.g*(1-l.a),b:l.b*l.a+base.b*(1-l.a),a:1};}return base;}
   const L=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b);};
   const out=[],seen=new Set();
   for(const el of document.querySelectorAll('#view *, .top *, footer *')){
     if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;const r=el.getBoundingClientRect();if(!r.width||el.closest('[hidden],svg,[disabled]'))continue;
     const cs=getComputedStyle(el);let op=1,a=el;while(a){op*=+getComputedStyle(a).opacity;a=a.parentElement;}if(op<.6)continue;
     const B=bg(el);if(!B)continue;let C=P(cs.color);if(C.a<1)C={r:C.r*C.a+B.r*(1-C.a),g:C.g*C.a+B.g*(1-C.a),b:C.b*C.a+B.b*(1-C.a)};
     const x=L(C),y=L(B),ratio=(Math.max(x,y)+.05)/(Math.min(x,y)+.05);const big=parseFloat(cs.fontSize)>=18.6||(parseFloat(cs.fontSize)>=14&&+cs.fontWeight>=700);
     if(ratio<(big?3:4.5)){const k=el.tagName+'.'+el.className;if(!seen.has(k)){seen.add(k);out.push(k+' "'+el.textContent.trim().slice(0,22)+'" '+ratio.toFixed(2)+' fs'+cs.fontSize);}}}
   return out;});
  if(low.length)issues.push(scheme+' '+(h||'#home')+': '+low.join(' | '));}
 await ctx.close();}
console.log(issues.join('\n')||'no issues');await b.close();})();
