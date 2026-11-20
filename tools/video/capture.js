const {chromium}=require('playwright');const base='file://'+__dirname+'/site.html';
(async()=>{const b=await chromium.launch();const errs=[];
const mk=async(pre)=>{const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,colorScheme:'light'});await ctx.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const st=document.createElement('style');st.textContent='.fab{display:none!important}';document.head.append(st);});});const p=await ctx.newPage();
 await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());p.on('pageerror',e=>errs.push(String(e)));
 await p.goto(base+'#home');await p.evaluate(pre||(()=>{}));return p;};
const full=async(p,name,h)=>{await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(300);
 await p.screenshot({path:`cap/${name}.jpg`,type:'jpeg',quality:92,fullPage:true,clip:{x:0,y:0,width:390,height:h}});};
let p=await mk(()=>localStorage.setItem('ufuq-rw-snd','false'));
await p.goto(base+'#home');await p.reload();await p.waitForTimeout(800);await full(p,'home',2700);
// drawer
await p.evaluate(()=>openDrawer());await p.waitForTimeout(500);await p.screenshot({path:'cap/ask0.jpg',type:'jpeg',quality:92});
await p.fill('#ask-input','لماذا يبدو المريخ أحمر؟');await p.waitForTimeout(100);await p.screenshot({path:'cap/ask1.jpg',type:'jpeg',quality:92});
await p.click('#send-btn');await p.waitForTimeout(1500);await p.screenshot({path:'cap/ask2.jpg',type:'jpeg',quality:92});
const sec=await p.evaluate(()=>SECTIONS.map(s=>s.id+':'+s.title).join(' | '));console.log(sec);
await p.keyboard.press('Escape');await p.waitForTimeout(300);
const tid=await p.evaluate(()=>SECTIONS[0].id);
await p.goto(base+'#topic-'+tid);await p.waitForTimeout(700);await full(p,'topic',2500);
await p.goto(base+'#lab');await p.waitForTimeout(1200);await full(p,'lab',2600);
for(const h of ['sky','solar','saudi','quiz']){await p.goto(base+'#'+h);await p.waitForTimeout(1200);await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(200);await p.screenshot({path:`cap/${h}.jpg`,type:'jpeg',quality:92});}
// build page with the moon rocket loaded
await p.evaluate(()=>{localStorage.setItem('ufuq-rw',JSON.stringify({mission:'m5',stars:{m1:3,m2:3,m3:3,m4:3,m5:0},builds:{m5:["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"]},legs:{m5:false},goal:'orbit'}));});
await p.goto(base+'#build');await p.waitForTimeout(900);await full(p,'build',3300);
console.log('errors',errs);await b.close();})();
