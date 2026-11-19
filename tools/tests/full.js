const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const issues=[];const base='file://'+process.cwd()+'/site.html';
const p0=await b.newPage();await p0.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());await p0.goto(base);await p0.waitForTimeout(300);
const secs=await p0.evaluate(()=>SECTIONS.map(s=>s.id));await p0.close();
const routes=['','#tools','#lab','#rocket','#build','#sky','#solar','#saudi','#quiz','#glossary','#about','#panel','#nonsense',...secs.map(s=>'#topic-'+s)];
for(const [w,scheme] of [[390,'light'],[360,'dark'],[1280,'light'],[1280,'dark']]){
 const ctx=await b.newContext({viewport:{width:w,height:860},colorScheme:scheme});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
 const tag=w+'/'+scheme;let cur='';p.on('pageerror',e=>issues.push(tag+cur+' JS: '+e.message));p.on('console',m=>{if((m.type()==='error'||m.type()==='warning')&&!m.text().includes('ERR_FAILED'))issues.push(tag+cur+' CONSOLE: '+m.text().slice(0,150));});
 for(const h of routes){cur=h||'#home';
  await p.goto(base+h);await p.waitForTimeout(450);
  const r=await p.evaluate(()=>{
   const o={sw:document.documentElement.scrollWidth,vw:innerWidth};
   const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&!e.closest('[hidden]');};
   o.wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();if(!(r.width>0))return false;if(getComputedStyle(e).position==='fixed')return false;let a=e.parentElement;while(a){const ov=getComputedStyle(a).overflowX;if(ov!=='visible')return false;a=a.parentElement;}return r.right>innerWidth+1||r.left<-1;}).slice(0,4).map(e=>e.tagName+'.'+(e.className.baseVal??e.className)+' '+Math.round(e.getBoundingClientRect().left)+'..'+Math.round(e.getBoundingClientRect().right));
   function bg(el){while(el){const cs=getComputedStyle(el);if(cs.backgroundImage&&cs.backgroundImage!=='none')return null;const c=cs.backgroundColor;if(c&&!/rgba\(0, 0, 0, 0\)/.test(c)&&!/, 0\)$/.test(c))return c;el=el.parentElement;}return getComputedStyle(document.body).backgroundColor;}
   function L(c){const m=c.match(/[\d.]+/g);const [r,g,b]=m.slice(0,3).map(Number).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b;}
   o.low=[];const seen=new Set();
   for(const el of document.querySelectorAll('#view *, header *, footer *, .top *')){
     if(!el.childNodes.length||![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;if(!vis(el))continue;
     const cs=getComputedStyle(el);if(/, 0\)$/.test(cs.color)||+cs.opacity<.6)continue;if(el.closest('[disabled],[aria-disabled="true"],svg'))continue;
     const B=bg(el);if(!B)continue;const a=L(cs.color),c=L(B);const ratio=(Math.max(a,c)+.05)/(Math.min(a,c)+.05);
     const big=parseFloat(cs.fontSize)>=18.6||(parseFloat(cs.fontSize)>=14&&+cs.fontWeight>=700);
     if(ratio<(big?3:4.5)){const k=el.className+'|'+el.tagName;if(!seen.has(k)){seen.add(k);o.low.push(el.tagName+'.'+el.className+' "'+el.textContent.trim().slice(0,18)+'" '+ratio.toFixed(2));}}}
   o.noName=[...document.querySelectorAll('button,a[href],[role=button],input,select,textarea')].filter(e=>vis(e)&&!(e.getAttribute('aria-label')||e.textContent.trim()||e.title||e.getAttribute('aria-labelledby')||(e.labels&&e.labels.length)||e.placeholder||e.querySelector('img[alt]'))).slice(0,4).map(e=>e.tagName+'#'+e.id+'.'+e.className);
   const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);o.dupIds=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))].slice(0,6);
   o.badLinks=[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href')).filter(h=>h.length>1&&!/^#(home|tools|lab|rocket|build|sky|solar|saudi|quiz|glossary|about|panel|topic-[a-z]+|rights|built|main|view)$/.test(h)).slice(0,5);
   o.blank=[...document.querySelectorAll('a[target=_blank]')].filter(a=>!/noopener/.test(a.rel)).length;
   o.imgNoAlt=[...document.querySelectorAll('img')].filter(i=>!i.hasAttribute('alt')).length;
   o.h1=document.querySelectorAll('#view h1').length;
   o.tiny=[...document.querySelectorAll('#view *')].filter(e=>vis(e)&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&parseFloat(getComputedStyle(e).fontSize)<11).slice(0,3).map(e=>e.tagName+'.'+e.className+' '+getComputedStyle(e).fontSize);
   o.smallTap=innerWidth<500?[...document.querySelectorAll('#view button,#view a[href]')].filter(e=>{if(!vis(e))return false;const r=e.getBoundingClientRect();return r.height<28&&r.width<28;}).slice(0,4).map(e=>e.tagName+'.'+e.className+' '+e.textContent.trim().slice(0,12)):[];
   return o;});
  const T=tag+' '+cur;
  if(r.sw>r.vw)issues.push(T+' OVERFLOW sw='+r.sw);
  if(r.wide.length)issues.push(T+' WIDE '+r.wide.join(' ; '));
  if(r.low.length)issues.push(T+' LOWCONTRAST '+r.low.slice(0,6).join(' ; '));
  if(r.noName.length)issues.push(T+' NONAME '+r.noName.join(' ; '));
  if(r.dupIds.length)issues.push(T+' DUPID '+r.dupIds.join(','));
  if(r.badLinks.length)issues.push(T+' BADLINK '+r.badLinks.join(','));
  if(r.blank)issues.push(T+' BLANK-noopener '+r.blank);
  if(r.imgNoAlt)issues.push(T+' IMG-noalt '+r.imgNoAlt);
  if(r.h1!==1&&cur!=='#nonsense')issues.push(T+' H1count '+r.h1);
  if(r.tiny.length)issues.push(T+' TINYTEXT '+r.tiny.join(' ; '));
  if(r.smallTap.length)issues.push(T+' SMALLTAP '+r.smallTap.join(' ; '));
 }
 await ctx.close();}
console.log(issues.join('\n')||'no issues');await b.close();})();
