const {chromium}=require('playwright');const base='file://'+__dirname+'/test.html';
(async()=>{const b=await chromium.launch();const errs=[];const ok=(n,c,x='')=>console.log((c?'ok  ':'FAIL')+' '+n+(c?'':' -> '+x));
 async function page(w,h,o={}){const ctx=await b.newContext({viewport:{width:w,height:h},...o});const p=await ctx.newPage();await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());p.on('pageerror',e=>errs.push(String(e)));return p;}
 // desktop: build from empty via clicks, check validation, move/delete/undo
 const p=await page(1280,900);await p.goto(base+'#build');await p.waitForTimeout(300);
 await p.screenshot({path:'shots/d-empty.png'});
 ok('launch disabled when empty',await p.locator('.rw-go').isDisabled());
 await p.click('#rw-tabs button:has-text("الخزانات")');await p.click('.rw-item:has-text("خزان صغير")');
 console.log('   errs w/o engine:',(await p.textContent('.rw-errs').catch(()=>'')).slice(0,120));
 await p.click('#rw-tabs button:has-text("المحركات")');await p.click('.rw-item:has-text("محرك واحد")');
 const stackTxt=async()=>p.evaluate(()=>JSON.parse(localStorage.getItem('ufuq-rw')).builds.m1.join(','));
 console.log('   stack:',await stackTxt());
 // select the engine (top) and move it down
 await p.locator('#rw-bay .rw-hit').last().click();console.log('   tools:',(await p.textContent('#rw-tools')).replace(/\s+/g,' '));
 await p.click('#rw-tools button:has-text("أنزلها")');console.log('   after move:',await stackTxt());
 await p.click('#rw-tabs button:has-text("الحمولات")');await p.click('.rw-item:has-text("قمر صناعي صغير")');
 await p.click('#rw-tabs button:has-text("الفواصل")');await p.click('.rw-item:has-text("غطاء")');console.log('   with fairing:',await stackTxt());
 ok('launch enabled',!(await p.locator('.rw-go').isDisabled()));
 await p.locator('#rw-shop').screenshot({path:'shots/d-built.png'});
 await p.click('#rw-tools button:has-text("تراجع")');console.log('   undo:',await stackTxt());
 // free mode + F9 preset
 await p.click('.rw-free');await p.click('button:has-text("ابدأ من تصميم يشبه فالكون 9")');await p.waitForTimeout(200);
 await p.locator('#rw-shop').screenshot({path:'shots/d-f9.png'});
 // drag & drop a tank onto the bay
 await p.click('#rw-tabs button:has-text("الخزانات")');
 await p.locator('.rw-item:has-text("خزان صغير")').dragTo(p.locator('#rw-bay svg'),{targetPosition:{x:200,y:400}});
 console.log('   after drag (free):',await p.evaluate(()=>JSON.parse(localStorage.getItem('ufuq-rw')).builds.free.join(',')));
 // tools page + rocket page entry cards
 await p.goto(base+'#tools');await p.waitForTimeout(300);ok('tools CTA',await p.locator('a.rw-cta[href="#build"]').count()===1);
 await p.locator('a.rw-cta').scrollIntoViewIfNeeded();await p.screenshot({path:'shots/d-tools.png'});
 await p.goto(base+'#rocket');await p.waitForTimeout(300);ok('rocket CTA',await p.locator('a.rw-cta[href="#build"]').count()===1);ok('old builder gone',await p.locator('#rb').count()===0);
 await p.locator('a.rw-cta').scrollIntoViewIfNeeded();await p.locator('a.rw-cta').screenshot({path:'shots/d-rkcta.png'});
 // leaving mid-flight stops animation without errors
 await p.goto(base+'#build');await p.waitForTimeout(200);await p.click('.rw-go').catch(()=>{});await p.waitForTimeout(1500);await p.goto(base+'#home');await p.waitForTimeout(500);
 // mobile
 for(const w of [390,360]){const m=await page(w,800);await m.goto(base+'#build');await m.waitForTimeout(400);
  ok(`mobile ${w} no h-scroll`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),await m.evaluate(()=>document.documentElement.scrollWidth));
  if(w===390){await m.screenshot({path:'shots/m-build.png',fullPage:true});
   await m.evaluate(()=>{const s=JSON.parse(localStorage.getItem('ufuq-rw')||'{}');s.mission='free';s.builds=s.builds||{};s.builds.free=["e9","t3","dc","ev","t2","p2","fr"];localStorage.setItem('ufuq-rw',JSON.stringify(s));});
   await m.goto(base+'#tools');await m.goto(base+'#build');await m.waitForTimeout(300);await m.click('.rw-go');await m.waitForTimeout(9000);
   await m.locator('#rw-flight').screenshot({path:'shots/m-flight.png'});
   ok(`mobile flight no h-scroll`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}}
 // reduced motion
 const r=await page(1280,900,{reducedMotion:'reduce'});await r.goto(base+'#build');await r.waitForTimeout(300);
 await r.evaluate(()=>{const s=JSON.parse(localStorage.getItem('ufuq-rw')||'{}');s.mission='free';s.goal='orbit';s.builds=s.builds||{};s.builds.free=["e9","t3","dc","ev","t2","p2","fr"];localStorage.setItem('ufuq-rw',JSON.stringify(s));});
 await r.goto(base+'#tools');await r.goto(base+'#build');await r.waitForTimeout(300);await r.click('.rw-go');await r.waitForTimeout(800);
 ok('reduced motion result immediately',await r.locator('#rw-result').isVisible());await r.locator('#rw-flight').screenshot({path:'shots/r-flight.png'});
 // dark mode
 const dk=await page(1280,900,{colorScheme:'dark'});await dk.goto(base+'#build');await dk.waitForTimeout(300);await dk.screenshot({path:'shots/dk-build.png'});
 console.log('errors:',errs.length?errs.join('\n'):'none');await b.close();})();
