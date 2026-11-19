const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
async function grab(f,h){const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();await p.route(/fonts/,r=>r.abort());await p.addInitScript(()=>{let s=1;Math.random=()=>((s=s*16807%2147483647)/2147483647);Date.now=()=>1794920000000;});
 await p.goto('file://'+__dirname+'/'+f+'#'+h);await p.waitForTimeout(500);const v=await p.evaluate(()=>document.querySelector('#view').innerHTML.replace(/\s+/g,' '));await ctx.close();return v;}
for(const h of ['home','topic-planets','topic-ai','topic-galaxies','lab','rocket','sky','solar','saudi','about','tools']){const a=await grab('old.html',h),c=await grab('test.html',h);
 if(a===c){console.log('same   ',h);continue;}let i=0;while(a[i]===c[i])i++;console.log('DIFF   ',h,a.length,c.length,'\n   old:',a.slice(Math.max(0,i-60),i+120),'\n   new:',c.slice(Math.max(0,i-60),i+160));}
await b.close();})();
