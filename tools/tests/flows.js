const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const log=[];const base='file://'+process.cwd()+'/site.html';
const p=await b.newPage({viewport:{width:400,height:860},colorScheme:'light'});await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
p.on('pageerror',e=>log.push('JS ERROR: '+e.message));
const t=async(name,fn)=>{try{const r=await fn();log.push((r===true?'ok   ':'FAIL ')+name+(r===true?'':' -> '+JSON.stringify(r)));}catch(e){log.push('EXC  '+name+' -> '+e.message.split('\n')[0]);}};
await p.goto(base);await p.waitForTimeout(400);
await t('quick chip fills search',async()=>{await p.click('.quick button');await p.waitForTimeout(100);return (await p.inputValue('#q')).length>0&&await p.locator('.res').count()>0||{q:await p.inputValue('#q'),res:await p.locator('.res').count()}});
await t('quick chip top result relevant',async()=>{const txt=await p.textContent('.res summary b');return /ثقب|ثقوب/.test(txt)||txt});
await t('clear search hides results',async()=>{await p.fill('#q','');await p.waitForTimeout(50);return await p.locator('.res').count()===0});
await t('1-char search',async()=>{await p.fill('#q','ا');await p.waitForTimeout(50);return await p.locator('.results').count()===0});
await t('nonsense search shows ask-ufuq',async()=>{await p.fill('#q','وصفة كبسة');await p.waitForTimeout(50);return (await p.textContent('#results')).includes('اسأل أفق')});
await t('search with HTML chars safe',async()=>{await p.fill('#q','<img src=x onerror=alert(1)>');await p.waitForTimeout(50);return await p.locator('#results img').count()===0});
await t('open result + jump to section',async()=>{await p.fill('#q','حلقات زحل');await p.waitForTimeout(80);await p.click('.res summary');await p.click('.res .link-btn');await p.waitForTimeout(400);const h=await p.evaluate(()=>location.hash);const open=await p.locator('details.q[open]').count();const vis=await p.locator('details.q[open]').isVisible();return h==='#topic-planets'&&open===1&&vis||{h,open,vis}});
await t('opened question marked read',async()=>await p.locator('details.q.read[open]').count()===1);
await t('progress text updated',async()=>/قرأت [1-9]/.test(await p.textContent('.qs .muted')));
await t('level toggle deep',async()=>{await p.click('.seg button:nth-child(2)');return (await p.locator('.art-body p').count())>=3});
await t('level persists',async()=>{await p.goto(base+'#topic-galaxies');await p.waitForTimeout(200);return await p.getAttribute('.seg button:nth-child(2)','aria-pressed')==='true'});
await t('easy -> link to deep',async()=>{await p.click('.seg button:nth-child(1)');await p.click('.art-body .link-btn');return await p.getAttribute('.seg button:nth-child(2)','aria-pressed')==='true'});
await t('listen hidden w/o runtime',async()=>await p.locator('.tts-only').isHidden());
await t('report error fallback',async()=>{await p.click('details.q summary');await p.click('details.q[open] .quiet');await p.waitForTimeout(150);return await p.locator('.report textarea').count()===1});
await t('report toggles off',async()=>{await p.click('details.q[open] .quiet');await p.waitForTimeout(150);return await p.locator('.report').count()===0});
await t('ai-only hidden offline',async()=>await p.evaluate(()=>[...document.querySelectorAll('.ai-only')].every(e=>e.hidden)));
await t('pager next',async()=>{await p.click('.pager a.next');await p.waitForTimeout(250);return (await p.evaluate(()=>location.hash))==='#topic-planets'});
await t('scroll top on nav',async()=>(await p.evaluate(()=>scrollY))<5);
await t('planets filter',async()=>{await p.fill('#q-filter','المريخ');await p.waitForTimeout(80);const n=await p.evaluate(()=>[...document.querySelectorAll('.qlist details')].filter(d=>!d.hidden).length);return n>=4||n});
await t('planets filter none',async()=>{await p.fill('#q-filter','زززز');await p.waitForTimeout(80);return await p.evaluate(()=>[...document.querySelectorAll('.qs p.muted')].some(x=>!x.hidden&&x.textContent.includes('لا يوجد')))});
await t('show all',async()=>{await p.fill('#q-filter','');await p.click('text=أظهر كل الأسئلة');return await p.evaluate(()=>[...document.querySelectorAll('.qlist details')].every(d=>!d.hidden))});
await t('back button',async()=>{await p.goBack();await p.waitForTimeout(250);return (await p.evaluate(()=>location.hash))==='#topic-galaxies'});
// tools
await p.goto(base+'#tools');await p.waitForTimeout(250);
await t('moon card',async()=>/مضاء منه نحو/.test(await p.textContent('#t-moon')));
await t('eclipse countdown',async()=>/يومًا/.test(await p.textContent('#t-eclipse')));
await t('events list',async()=>await p.locator('.ev').count()>=4);
for(const v of ['','0','-5','abc','99999','70.5']){await t('weight input "'+v+'"',async()=>{await p.fill('#w-in',v);await p.waitForTimeout(30);const s=await p.textContent('#w-out');return !/NaN|Infinity|-/.test(s)||s.slice(0,60)});}
for(const v of ['','0','-3','abc','1000','15']){await t('age input "'+v+'"',async()=>{await p.fill('#a-in',v);await p.waitForTimeout(30);const s=await p.textContent('#a-out');return !/NaN|Infinity/.test(s)||s.slice(0,60)});}
await t('age 0 text',async()=>{await p.fill('#a-in','0');await p.waitForTimeout(30);return await p.textContent('#a-out')});
// quiz full runs
for(const lv of [1,2,3,4]){await t('quiz level '+lv+' full run',async()=>{await p.goto(base+'#home');await p.goto(base+'#quiz');await p.waitForTimeout(150);await p.click('.lv:nth-child('+lv+')');for(let i=0;i<5;i++){await p.click('.opt >> nth=0');await p.click('.qrow .btn-accent');}return /\d \/ 5/.test(await p.textContent('.score'))});}
await t('quiz again/level buttons',async()=>{await p.click('text=غيّر الموضوع أو المستوى');return await p.locator('.lv').count()===4});
await t('quiz best saved',async()=>/أفضل نتيجة/.test(await p.textContent('.lv-grid')));
await t('quiz options shuffled keep answer',async()=>{await p.click('.lv:nth-child(1)');const q=await p.textContent('.qbox h2');const ok=await p.evaluate(q=>{const it=QUIZ.find(x=>x[0]===q);return it&&it[1][it[2]]},q);const right=await p.locator('.opt[data-ok]').textContent();return right===ok||{q,ok,right}});
await t('quiz read-more link',async()=>{await p.click('.opt >> nth=0');const n=await p.locator('.qrow .link-btn').count();if(!n)return 'no link';await p.click('.qrow .link-btn');await p.waitForTimeout(300);return (await p.evaluate(()=>location.hash)).startsWith('#topic-')&&await p.locator('details.q[open]').count()===1});
// glossary
await p.goto(base+'#glossary');await p.waitForTimeout(200);
await t('glossary count',async()=>await p.locator('.term').count()===16);
await t('glossary filter arabic',async()=>{await p.fill('#gloss-q','سديم');await p.waitForTimeout(50);return await p.locator('.term').count()===1});
await t('glossary filter english',async()=>{await p.fill('#gloss-q','redshift');await p.waitForTimeout(50);return await p.locator('.term').count()===1});
await t('glossary none',async()=>{await p.fill('#gloss-q','qqq');await p.waitForTimeout(50);return await p.locator('.terms p.muted').count()===1});
await t('glossary ask opens drawer',async()=>{await p.fill('#gloss-q','');await p.click('.term .g-act .link-btn');await p.waitForTimeout(200);return await p.locator('#drawer').isVisible()&&await p.locator('.msg.user').count()===1});
await t('local answer for term',async()=>/السنة الضوئية|الوحدة الفلكية|.{10}/.test(await p.textContent('.msg.bot:last-child')));
await t('esc closes drawer',async()=>{await p.keyboard.press('Escape');return await p.locator('#drawer').isHidden()&&await p.locator('#fab').isVisible()});
// chat
await t('chat empty send ignored',async()=>{await p.click('#fab');const n=await p.locator('.msg').count();await p.press('#ask-input','Enter');return await p.locator('.msg').count()===n});
await t('chat follow-up chip',async()=>{await p.fill('#ask-input','ليش المريخ احمر');await p.press('#ask-input','Enter');await p.waitForTimeout(200);const c=await p.locator('.msg.bot:last-child .schip').count();if(!c)return 'no chips';await p.click('.msg.bot:last-child .schip >> nth=0');await p.waitForTimeout(200);return await p.locator('.msg.user').count()>=3});
await t('chat open section link',async()=>{await p.click('.msg.bot:last-child a:not(.src-link)');await p.waitForTimeout(300);return (await p.evaluate(()=>location.hash)).startsWith('#topic-')});
await t('drawer closed on mobile after link',async()=>await p.locator('#drawer').isHidden());
await t('note shown once',async()=>{await p.click('#fab');return await p.locator('.msg .note').count()===1});
await t('starter chips hidden after first q',async()=>await p.locator('#starter').isHidden());
// about/panel/unknown
await p.keyboard.press('Escape');
await p.goto(base+'#about');await p.waitForTimeout(150);
await t('about has team',async()=>/خالد يزيد العنزي/.test(await p.textContent('footer')));
await t('about goals 7',async()=>await p.locator('.goals li').count()===7);
await p.goto(base+'#panel');await p.waitForTimeout(150);
await t('panel locked offline',async()=>/لفريق أفق الذكاء|يتحقق/.test(await p.textContent('#view')));
await t('panel nav hidden',async()=>await p.locator('#nav-panel').isHidden());
await p.goto(base+'#observatory');await p.waitForTimeout(150);
await t('observatory -> home',async()=>await p.locator('.hero').count()===1);
await t('home fact another',async()=>{const a=await p.textContent('#fact h3');await p.click('#fact .btn-soft');return (await p.textContent('#fact h3'))!==a});
await t('home sky card links tools',async()=>{await p.click('#sky');await p.waitForTimeout(200);return (await p.evaluate(()=>location.hash))==='#tools'});
await t('home progress text',async()=>{await p.goto(base);await p.waitForTimeout(200);return await p.textContent('#prog-txt')});
await t('topic card counts',async()=>(await p.locator('.topic').allTextContents()).map(x=>x.replace(/\s+/g,' ').slice(-22)).join(' | '));
await t('nav current',async()=>{await p.goto(base+'#tools');await p.waitForTimeout(150);return await p.getAttribute('.links a[data-r=tools]','aria-current')==='page'});
await t('topic page nav current cleared',async()=>{await p.goto(base+'#topic-planets');await p.waitForTimeout(150);return await p.locator('.links a[aria-current]').count()===0});
// «حقيقة أم خرافة؟»
await t('myths page items',async()=>{await p.goto(base+'#myths');await p.waitForTimeout(200);const n=await p.locator('.my-item').count();return n>0&&n===await p.evaluate(()=>MYTHS.length)||n});
await t('myths answer reveals fix and score',async()=>{await p.locator('.my-item').first().locator('.my-act button').nth(1).click();await p.waitForTimeout(80);return await p.locator('.my-item').first().locator('.my-ans').isVisible()&&/أجبت عن 1 /.test(await p.textContent('.my-score'))||await p.textContent('.my-score')});
await t('myths answered buttons disabled',async()=>await p.locator('.my-item').first().locator('.my-act button[disabled]').count()===2);
await t('myths reveal all',async()=>{await p.click('.my-bar .link-btn');await p.waitForTimeout(80);return await p.locator('.my-ans:visible').count()===await p.evaluate(()=>MYTHS.length)});
await t('myths read more opens topic',async()=>{await p.locator('.my-item').first().locator('.my-more .link-btn').click();await p.waitForTimeout(300);return /^#topic-/.test(await p.evaluate(()=>location.hash))});
await t('quiz has myths mode',async()=>{await p.goto(base+'#quiz');await p.waitForTimeout(200);await p.click('.q-mode:has-text("حقيقة أم خرافة")');await p.waitForTimeout(200);return (await p.evaluate(()=>location.hash))==='#myths'&&await p.getAttribute('.links a[data-r=quiz]','aria-current')==='page'});
// «طريقك إلى الفضاء»
await t('path page sections',async()=>{await p.goto(base+'#path');await p.waitForTimeout(200);const n=[await p.locator('.pt-tl li').count(),await p.locator('.pt-card').count()];return n[0]===await p.evaluate(()=>PATH_ARABS.length)&&n[1]===await p.evaluate(()=>PATH_AGENCIES.length+PATH_NOW.length)||n});
await t('path read opens topic',async()=>{await p.locator('.pt-tl li').first().locator('.link-btn').click();await p.waitForTimeout(300);return /^#topic-/.test(await p.evaluate(()=>location.hash))});
await t('home teaser opens path',async()=>{await p.goto(base+'#home');await p.waitForTimeout(200);await p.click('a.pt-tease');await p.waitForTimeout(200);return (await p.evaluate(()=>location.hash))==='#path'&&await p.locator('.path h1').count()===1});
// «نجم يوم ميلادك»
await t('birthstar ruler lists all stars',async()=>{await p.goto(base+'#birthstar');await p.waitForTimeout(200);const n=await p.locator('.bs-rl li').count();return n===await p.evaluate(()=>BS_STARS.length)&&await p.locator('.bs-me').count()===0||n});
await t('birthstar picks the nearest star',async()=>{const d=await p.evaluate(()=>new Date(Date.now()-16.7*BS_YR).toISOString().slice(0,10));await p.fill('#bs-date',d);await p.dispatchEvent('#bs-date','change');await p.waitForTimeout(200);
  const h=await p.locator('.bs-res h2').textContent();return h==='النسر الطائر'&&await p.locator('.bs-rl li.on').count()===1&&await p.locator('.bs-me').count()===1&&/قبل ولادتك|بعد ولادتك|وُلدت فيه/.test(await p.locator('.bs-say').textContent())||h});
await t('birthstar rejects a future date',async()=>{const d=await p.evaluate(()=>new Date(Date.now()+3*864e5).toISOString().slice(0,10));await p.fill('#bs-date',d);await p.dispatchEvent('#bs-date','change');await p.waitForTimeout(200);return await p.locator('.bs-err').count()===1&&await p.locator('.bs-res').count()===0});
await t('tools card opens birthstar',async()=>{await p.goto(base+'#tools');await p.waitForTimeout(200);await p.click('a.bs-cta');await p.waitForTimeout(200);return (await p.evaluate(()=>location.hash))==='#birthstar'&&(await p.locator('h1').first().textContent())==='نجم يوم ميلادك'});
// عدّاد «اسأل أفق»: ثلاثة أحداث فقط، بلا نص السؤال
await t('ask counter events without question text',async()=>{await p.goto(base+'#home');await p.waitForTimeout(200);
  await p.evaluate(()=>{window.__gc=[];window.goatcounter={count:o=>window.__gc.push(o)};});
  await p.click('#fab');await p.fill('#ask-input','ليش المريخ احمر');await p.press('#ask-input','Enter');await p.waitForTimeout(200);
  await p.fill('#ask-input','من فاز بكأس العالم 2022');await p.press('#ask-input','Enter');await p.waitForTimeout(200);
  const ev=await p.evaluate(()=>window.__gc);const paths=ev.map(e=>e.path).join(','),txt=JSON.stringify(ev);
  return paths==='ask-open,ask-answer,ask-decline'&&ev.every(e=>e.event===true)&&!/المريخ|كأس/.test(txt)||txt});
console.log(log.join('\n'));await b.close();})();
