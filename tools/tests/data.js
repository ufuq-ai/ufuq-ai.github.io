const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')errs.push(m.type()+': '+m.text().slice(0,160))});await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.goto('file://'+process.cwd()+'/site.html');await p.waitForTimeout(500);
const r=await p.evaluate(()=>{
 const out={};
 const ids=KB.map(e=>e.id);out.dupIds=ids.filter((x,i)=>ids.indexOf(x)!==i);
 out.counts={KB:KB.length,KQ:KQ.length,KN,TERMS:TERMS.length,QUIZ:QUIZ.length,SECRETS:(typeof SECRETS!=='undefined'?SECRETS.length:'undef')};
 out.noUrl=KQ.filter(e=>!e.url).map(e=>e.id);
 out.badCat=KB.filter(e=>!['glossary','secret',...SECTIONS.map(s=>s.id)].includes(e.c)).map(e=>e.id);
 out.badTag=KB.filter(e=>e.tag&&!['تقدير','استنتاج','سؤال مفتوح'].includes(e.tag)).map(e=>e.id+':'+e.tag);
 out.quizBadRef=QUIZ.filter(q=>!KB_BY_ID[q[4]]).map(q=>q[0]);
 out.quizBadAns=QUIZ.filter(q=>q[2]<0||q[2]>=q[1].length).map(q=>q[0]);
 out.quizDupOpts=QUIZ.filter(q=>new Set(q[1]).size!==q[1].length).map(q=>q[0]);
 out.quizLevels=[1,2,3].map(n=>QUIZ.filter(q=>q[5]===n).length);
 out.srcOrphans=Object.keys(SRC).filter(k=>!KB_BY_ID[k]);
 out.levelsMissing=SECTIONS.filter(s=>!LEVELS[s.id]||!LEVELS[s.id].easy||!LEVELS[s.id].deep).map(s=>s.id);
 const titles=KQ.map(e=>e.t);out.dupTitles=titles.filter((x,i)=>titles.indexOf(x)!==i);
 out.longA=KQ.filter(e=>e.a.length>700).map(e=>e.id+':'+e.a.length);
 out.httpLinks=KQ.filter(e=>e.url&&!e.url.startsWith('https://')).map(e=>e.id);
 out.domains=[...new Set(KQ.map(e=>{try{return new URL(e.url).hostname}catch(_){return 'BAD'}}))];
 out.secretsLeft=['foundSecret','renderSecretsBox','FAN_NOTE','HINTS','ORIGINAL_TEXT','renderObservatory'].filter(n=>{try{return typeof eval(n)!=='undefined'}catch(_){return false}});
 out.heroFacts=document.querySelector('.hero')?null:'(hero on home only)';
 out.titleTag=document.title;
 // KB IDs referenced by LEVELS / goTo not needed
 out.emptyKeywords=KQ.filter(e=>!e.k||e.k.trim().length<4).map(e=>e.id);
 // per-entry self-findability: searching its own title should return itself top-3
 out.selfMiss=KQ.filter(e=>!searchKB(e.t).slice(0,3).some(h=>h.e.id===e.id)).map(e=>e.id+' '+e.t);
 return out;});
console.log(JSON.stringify(r,null,1));console.log('ERR',errs);await b.close();})();
