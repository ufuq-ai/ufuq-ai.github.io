const fs=require('fs');eval(fs.readFileSync(__dirname+'/rw-engine.js','utf8')+`
const D={
 m1min:[["e1","t1","p1","fr"],0,"m1"], m1bare:[["e1","t1","p1"],0,"m1"],
 m2one:[["e9","t3","t3","p1","fr"],0,"m2"], m2ref:[["e3","t2","dc","ev","t2","p1","fr"],0,"m2"],
 m3ref:[["e9","t3","dc","ev","t3","p2","fr"],0,"m3"], m4ref:[["e9","t3","dc","ev","t3","p4"],0,"m4"],
 f9:[["e9","t3","t3","dc","ev","t2","p4"],0,"m4"],
 m5two:[["e9","t3","dc","ev","t3","p3","fr"],0,"m5"], m5three:[["e9","t3","dc","ev","t3","dc","ev","t1","p3","fr"],0,"m5"],
 m6ref:[["e9","t3","dc","ev","t3","p2","fr"],1,"m6"], m6noleg:[["e9","t3","dc","ev","t3","p2","fr"],0,"m6"],
 heavy1:[["e1","t3","p4"],0,"m4"], vac1:[["ev","t2","p1","fr"],0,"m1"], bad:[["t2","e1","p1","fr"],0,"m1"],
};
for(const k in D){const [stk,legs,mid]=D[k];const M=RW_MISSIONS.find(m=>m.id===mid);const st=rwParse(stk,legs);
 if(st.errs.length){console.log(k.padEnd(9),'ERR',st.errs.join(' | '));continue;}
 const ph=rwPhysics(st),F=rwFlight(st,ph,M.goal),sc=rwScore(M,st,ph,F);
 console.log(k.padEnd(9),'m0',ph.m0.toFixed(1),'twr',ph.twr.toFixed(2),'dv',ph.dv.toFixed(2),'loss',ph.loss.toFixed(2),'vf',ph.vf.toFixed(2),'|',F.kind,F.fail||'','apo',Math.round(F.apogee),'tEnd',Math.round(F.tEnd),'moon',F.moon,'land',F.land,'|',sc.ok?'OK':'--','★'+sc.stars, ph.stages.map(s=>'['+s.twr.toFixed(2)+' '+s.dv.toFixed(2)+' '+Math.round(s.tb)+'s]').join(''));
 if(k==='f9'||k==='m2one'||k==='m1min')console.log('   ',F.ev.map(e=>Math.round(e.t)+'s '+e.txt).join(' / '));
}`);
