const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+__dirname+'/stage.html');await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
const ts=(process.argv[2]||'3.5,10.6,15.6,25.5,33,38.5,44,52.2,58.5').split(',').map(Number);
for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:`kf-${t}.jpg`,type:'jpeg',quality:85});}
console.log(errs);await b.close();})();
