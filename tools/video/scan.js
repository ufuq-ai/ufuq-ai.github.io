const {chromium}=require('playwright');const base='file://'+__dirname+'/site.html';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});const p=await ctx.newPage();
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());await p.clock.install({time:new Date('2026-11-20T12:00:00')});
await p.goto(base+'#home');await p.evaluate(()=>{localStorage.setItem('ufuq-rw-snd','false');localStorage.setItem('ufuq-tour-off','true');localStorage.setItem('ufuq-rw',JSON.stringify({mission:'m5',stars:{m1:3,m2:3,m3:3,m4:3,m5:0},builds:{m5:["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"]},legs:{m5:false},goal:'orbit'}));});
await p.goto(base+'#build');await p.clock.pauseAt(new Date('2026-11-20T12:00:05'));await p.clock.runFor(800);await p.click('.rw-go');await p.waitForTimeout(1500);
let sim=0,lc='',ll='';
while(sim<230){await p.clock.runFor(100);sim+=0.1;
 const st=await p.evaluate(()=>({clk:document.querySelector('#rw-clock').textContent,top:(document.querySelector('#rw-log > *')||{}).textContent||'',res:!document.querySelector('#rw-result').hidden,alt:document.querySelector('#rw-alt').textContent}));
 if(st.top!==ll){console.log(sim.toFixed(1),'LOG',st.clk,'|',st.top.slice(0,64));ll=st.top;}
 if(st.clk.startsWith('T−')&&st.clk!==lc){console.log(sim.toFixed(1),'CLK',st.clk);}lc=st.clk;
 if(st.res){console.log(sim.toFixed(1),'RESULT',st.alt);break;}}
await b.close();})();
