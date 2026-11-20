const {chromium}=require('playwright');const fs=require('fs');const base='file://'+__dirname+'/site.html';
fs.mkdirSync(__dirname+'/fl',{recursive:true});
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2});
await ctx.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const st=document.createElement('style');st.textContent='.fab{display:none!important}';document.head.append(st);});});
const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.clock.install();
await p.goto(base+'#home');await p.evaluate(()=>{localStorage.setItem('ufuq-rw-snd','false');localStorage.setItem('ufuq-tour-off','true');localStorage.setItem('ufuq-rw',JSON.stringify({mission:'m5',stars:{m1:3,m2:3,m3:3,m4:3,m5:0},builds:{m5:["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"]},legs:{m5:false},goal:'orbit'}));});
await p.goto(base+'#build');await p.clock.runFor(800);await p.click('.rw-go');
// sim seconds after click for video time v (0..DUR)
const DUR=9.5,FPS=30,N=Math.round(DUR*FPS);
const speed=v=>v<2.4?1.6:v<5?1.6+(23-1.6)*((v-2.4)/2.6)**1.5:23;
let sim=5.4,cur=0;const times=[];
for(let i=0;i<N;i++){const v=i/FPS;if(i>0)sim+=speed(v)/FPS;times.push(sim);}
console.log('sim end',times[N-1].toFixed(1));
for(let i=0;i<N;i++){const ms=Math.round(times[i]*1000)-cur;if(ms>0){await p.clock.runFor(ms);cur+=ms;}
 await p.screenshot({path:`fl/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:90});}
const st=await p.evaluate(()=>({log:document.querySelector('#rw-log').textContent.slice(-80),alt:document.querySelector('#rw-alt').textContent,res:!document.querySelector('#rw-result').hidden}));
console.log(JSON.stringify(st),errs);await b.close();})();
