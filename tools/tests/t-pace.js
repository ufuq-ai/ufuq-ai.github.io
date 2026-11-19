const {chromium}=require('playwright');const base='file://'+__dirname+'/test.html';
const which=(process.argv[2]||'').split(',');
const SC={
 m1:{mission:'m1',b:["e1","t1","p1","fr"]},
 m3:{mission:'m3',b:["e9","t3","dc","ev","t3","p2","fr"]},
 f9:{mission:'free',goal:'orbit',b:["e9","t3","t3","dc","ev","t2","p4"],legs:1},
 m6:{mission:"m6",b:["e9","t3","dc","ev","t3","p2","fr"],legs:1,shots:[38,40,42,44]},
 m5:{mission:'m5',b:["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"],shots:[80,86,92,96,100,108,118,128,134]},
 bare:{mission:'m1',b:["e1","t1","p1"]},
 pad:{mission:'free',goal:'orbit',b:["e1","t3","p4"]},
 m2sub:{mission:'m2',b:["e9","t3","t3","p1","fr"]},
};
(async()=>{const b=await chromium.launch();const errs=[];
 for(const [name,S] of Object.entries(SC)){if(which[0]&&!which.includes(name))continue;
  const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
  p.on('pageerror',e=>errs.push(name+': '+String(e)));
  await p.goto(base+'#home');await p.evaluate(S=>{localStorage.setItem('ufuq-rw-snd','false');localStorage.setItem('ufuq-rw',JSON.stringify({mission:S.mission,stars:{m1:3,m2:3,m3:3,m4:3,m5:3},builds:{[S.mission]:S.b},legs:{[S.mission]:!!S.legs},goal:S.goal||'orbit'}));},S);
  await p.goto(base+'#build');await p.waitForTimeout(400);await p.addStyleTag({content:'.top{display:none!important}'});
  await p.click('.rw-go');const t0=Date.now();const seen={};const marks=[['liftoff','إقلاع'],['karman','كارمان'],['orbit','سرعة المدار'],['tli','من جديد'],['geo','الثابتة'],['half','منتصف'],['arrive','وصل المسبار'],['land','هبطت المرحلة'],['boom','تحطّمت'],['splash','سقط في المحيط'],['abort','أُطفئت']];
  let a80=null,shotI=0;const shots=S.shots||[];
  while(Date.now()-t0<200000){
   const st=await p.evaluate(()=>({log:document.querySelector('#rw-log').textContent,alt:document.querySelector('#rw-alt').textContent,clk:document.querySelector('#rw-clock').textContent,res:!document.querySelector('#rw-result').hidden}));
   const el=(Date.now()-t0)/1000;
   for(const [k,txt] of marks)if(!seen[k]&&st.log.includes(txt))seen[k]=el.toFixed(1)+'s ('+st.clk+')';
   const altN=parseFloat(st.alt.replace(/,/g,''));if(a80==null&&altN>=80&&altN<1e6)a80=el.toFixed(1)+'s ('+st.clk+')';
   if(shotI<shots.length&&el>=shots[shotI]){await p.locator('#rw-stage').screenshot({path:`shots/pace-${name}-${shots[shotI]}.png`});shotI++;}
   if(st.res&&!seen.result){seen.result=el.toFixed(1)+'s';if(shotI>=shots.length)break;}
   await p.waitForTimeout(150);}
  console.log(name.padEnd(6),'80km:',a80,JSON.stringify(seen));
  await ctx.close();}
 console.log('errors:',errs.length?errs.join('\n'):'none');await b.close();})();
