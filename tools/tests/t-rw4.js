const {chromium}=require('playwright');const base='file://'+__dirname+'/test.html';
(async()=>{const b=await chromium.launch();const errs=[];const ok=(n,c,x='')=>console.log((c?'ok  ':'FAIL')+' '+n+(c?'':' -> '+x));
 const ctx=await b.newContext({viewport:{width:1280,height:900}});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&!m.text().includes('ERR_FAILED'))errs.push(m.text());});
 await p.goto(base+'#build');await p.waitForTimeout(300);
 ok('mission 2 locked',await p.locator('.rw-m').nth(1).isDisabled());
 for(const [tab,n] of [['المحركات','محرك واحد'],['الخزانات','خزان صغير'],['الحمولات','قمر صناعي صغير'],['الفواصل','غطاء']]){await p.click(`#rw-tabs button:has-text("${tab}")`);await p.click(`.rw-item:has-text("${n}")`);}
 await p.click('.rw-go');await p.waitForTimeout(4500);
 const clk=async()=>p.textContent('#rw-clock');
 await p.click('#rw-pause');const c1=await clk();await p.waitForTimeout(800);const c2=await clk();ok('pause freezes clock',c1===c2,c1+' '+c2);
 ok('pause label',(await p.textContent('#rw-pause'))==='تابع');await p.click('#rw-pause');
 await p.click('#rw-snd');ok('sound toggles off',(await p.getAttribute('#rw-snd','aria-pressed'))==='false');ok('sound pref saved',await p.evaluate(()=>localStorage.getItem('ufuq-rw-snd'))==='false');
 await p.click('#rw-speed button[data-v="4"]');const t1=await clk();await p.waitForTimeout(1000);const t2=await clk();console.log('   x4 clock',t1,'->',t2);
 await p.click('#rw-skip');await p.waitForTimeout(400);ok('skip shows result',await p.locator('#rw-result').isVisible());
 ok('stars saved',await p.evaluate(()=>JSON.parse(localStorage.getItem('ufuq-rw')).stars.m1)===3);
 await p.click('#rw-result button:has-text("أطلق مرة أخرى")');await p.waitForTimeout(500);ok('relaunch hides result',!(await p.locator('#rw-result').isVisible()));ok('speed reset',(await p.getAttribute('#rw-speed button[data-v="1"]','aria-pressed'))==='true');
 await p.click('#rw-skip');await p.waitForTimeout(300);
 await p.click('#rw-result button:has-text("المهمة التالية")');await p.waitForTimeout(300);
 ok('next mission selected',await p.evaluate(()=>JSON.parse(localStorage.getItem('ufuq-rw')).mission)==='m2');ok('shop visible again',await p.locator('#rw-shop').isVisible());ok('flight hidden',!(await p.locator('#rw-flight').isVisible()));
 ok('mission 2 unlocked',!(await p.locator('.rw-m').nth(1).isDisabled()));
 console.log('   brief:',(await p.textContent('#rw-brief')).replace(/\s+/g,' ').slice(0,140));
 // keyboard: select part via Enter, delete with Delete
 await p.click('#rw-tabs button:has-text("المحركات")');await p.click('.rw-item:has-text("محرك واحد")');
 await p.locator('#rw-bay .rw-hit').first().focus();await p.keyboard.press('Enter');ok('keyboard select',(await p.textContent('#rw-tools')).includes('احذفها'));
 await p.keyboard.press('Delete');ok('keyboard delete',await p.evaluate(()=>JSON.parse(localStorage.getItem('ufuq-rw')).builds.m2.length)===0);
 console.log('errors:',errs.length?errs.join('\n'):'none');await b.close();})();
