// App icons for the installable site: icon-192.png, icon-512.png (logo.svg) and icon-maskable-512.png (icon-maskable.svg,
// full-bleed so Android can crop it to a circle or rounded square). Run from tools/brand, then copy the PNGs to the repo root.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [svg,n,out,bg] of [['logo.svg',192,'icon-192.png',false],['logo.svg',512,'icon-512.png',false],['icon-maskable.svg',512,'icon-maskable-512.png',true]]){
  const p=await b.newPage({viewport:{width:n,height:n},deviceScaleFactor:1});
  await p.goto('file://'+process.cwd()+'/'+svg);await p.waitForTimeout(150);
  await p.screenshot({path:out,omitBackground:!bg});await p.close();}
await b.close();})();
