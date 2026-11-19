const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
let p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});await p.goto('file://'+process.cwd()+'/og.html');await p.waitForTimeout(200);await p.screenshot({path:'og.png'});
for(const n of [32,180]){p=await b.newPage({viewport:{width:n,height:n},deviceScaleFactor:1});await p.goto('file://'+process.cwd()+'/favicon.svg');await p.waitForTimeout(100);await p.screenshot({path:n===32?'favicon-32.png':'apple-touch-icon.png',omitBackground:true});}
await b.close();})();
