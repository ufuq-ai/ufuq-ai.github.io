const {chromium}=require('playwright');const base='file://'+__dirname+'/test.html';
const which=process.argv[2]||'all';
const SC={
 m1:{mission:'m1',b:["e1","t1","p1","fr"],legs:0,shots:[1.5,4,6,9,12,15]},
 m1bare:{mission:'m1',b:["e1","t1","p1"],legs:0,shots:[3,5.5,7,9,11]},
 pad:{mission:'free',goal:'orbit',b:["e1","t3","p4"],legs:0,shots:[3.5,6,9]},
 m3:{mission:"m3",b:["e9","t3","dc","ev","t3","p2","fr"],legs:0,shots:[4,8,12,15,18,21,24,27,29,31,34]},
 m5:{mission:"m5",b:["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"],legs:0,shots:[36,40,44]},
 m6:{mission:"m6",b:["e9","t3","dc","ev","t3","p2","fr"],legs:1,shots:[3.6,5.5,9.2,10,24.5,27,31,34]},
 f9:{mission:"free",goal:"orbit",b:["e9","t3","t3","dc","ev","t2","p4"],legs:1,shots:[24,27,29,31,33,35]},
 m2sub:{mission:'m2',b:["e9","t3","t3","p1","fr"],legs:0,shots:[6,12,18,24,30]},
};
(async()=>{const b=await chromium.launch();const errs=[];
 for(const [name,S] of Object.entries(SC)){if(which!=='all'&&!which.split(',').includes(name))continue;
  const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
  p.on('pageerror',e=>errs.push(name+': '+String(e)));
  await p.goto(base+'#home');await p.evaluate(S=>{const st={mission:S.mission,stars:{m1:3,m2:3,m3:3,m4:3,m5:3},builds:{[S.mission]:S.b},legs:{[S.mission]:!!S.legs},goal:S.goal||'orbit'};localStorage.setItem('ufuq-rw',JSON.stringify(st));},S);
  await p.goto(base+'#build');await p.waitForTimeout(400);
  console.log(name,'|',(await p.textContent('#rw-panel')).replace(/\s+/g,' ').slice(0,160));
  await p.click('.rw-go');const t0=Date.now();
  for(const s of S.shots){const w=s*1000-(Date.now()-t0);if(w>0)await p.waitForTimeout(w);await p.locator('#rw-stage').screenshot({path:`shots/${name}-${String(s).replace('.','_')}.png`});}
  await p.waitForSelector('#rw-result:not([hidden])',{timeout:90000}).catch(()=>{});
  console.log('   result:',(await p.textContent('#rw-result')).replace(/\s+/g,' ').slice(0,260),' | took',((Date.now()-t0)/1000).toFixed(1),'s');
  console.log('   log:',(await p.textContent('#rw-log')).replace(/\s+/g,' ').slice(0,200));
  await ctx.close();}
 console.log('errors:',errs.length?errs.join('\n'):'none');await b.close();})();
