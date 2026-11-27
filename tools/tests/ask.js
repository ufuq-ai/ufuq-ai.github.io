/* اختبار «اسأل أفق» بأسئلة الناس الحقيقية (50 سؤالًا)
   يشغّل محرك البحث نفسه الموجود في الصفحة (searchKB) وقرار الجواب نفسه (kbPick) الذي يستخدمه answerLocal.
   وفي النسخ الأقدم من 1.1 (بلا kbPick) يطبق قاعدتها: أعلى نتيجة إذا كانت درجتها 2 أو أكثر، وإلا «ما فيه جواب».
   التشغيل من داخل tools/tests بعد نسخ index.html إلى site.html:  node ask.js   (و node ask.js -v للتفاصيل)

   كل سؤال: [النوع، السؤال، الجواب المتوقع]
   الجواب المتوقع: رقم معلومة (K…) أو مصطلح (G…)، أو قائمة أرقام كلها مقبولة، أو "none" يعني «ما فيه جواب في الموسوعة».
   «نجاح هش» = نجح لكن النتيجة الثانية (معلومة أخرى) درجتها قريبة جدًا (فرق أقل من 0.5)، فأي تغيير صغير قد يقلبه.
   الأنواع: عامية، إملاء، صيغة، تشكيل، خارج (أسئلة ليست في الموسوعة: يجب ألا يجيب عنها).
   المتوقع مكتوب من معنى السؤال ونصوص المعلومات، لا من مخرجات المحرك. لا تغيّره لتنجح النتيجة. */
const CASES=[
 // ── العامية السعودية
 ["عامية","ليش المريخ احمر","K20"],
 ["عامية","كم بعد القمر عنا","K86"],
 ["عامية","ليش النجوم ترمش","K1"],
 ["عامية","وش يصير لو دخلت ثقب اسود","K33"],
 ["عامية","ليش القمر يصير احمر وقت الخسوف","K60"],
 ["عامية","متى الكسوف الجاي عندنا بالسعودية","K69"],
 ["عامية","ليش رواد الفضاء يطيرون داخل المحطة","K56"],
 ["عامية","وش سالفة بلوتو ليش شالوه من الكواكب","K30"],
 ["عامية","كم قمر عند المشتري","K99"],
 ["عامية","ابي اعرف وش الفرق بين الشهاب والنيزك","K62"],
 ["عامية","ليش ما نشوف الا وجه واحد من القمر","K7"],
 ["عامية","وين احسن مكان اشوف فيه النجوم بالسعودية","K167"],
 ["عامية","الشمس كم تبعد عنا","K73"],
 ["عامية","ليش الصيف حار والشتا بارد","K9"],
 ["عامية","مين اول رائد فضاء عربي","K255"],
 ["عامية","وشلون انقرضت الديناصورات","K65"],
 ["عامية","البرج حقي يأثر على شخصيتي؟","K6"],
 // ── أخطاء إملائية
 ["إملاء","لماذا لون المريح احمر","K20"],
 ["إملاء","تلسكوب جيمس ويبب وش يميزه","K55"],
 ["إملاء","كيف بدا الكون بالانفجار العضيم","K40"],
 ["إملاء","هل اندرومدا بتصطدم بمجرتنا","K13"],
 ["إملاء","مااهو كوكب عطارد","K19"],
 ["إملاء","ليش السما مظلمه بالليل","K2"],
 ["إملاء","المجره درب التبانه كم فيها نجم","K18"],
 ["إملاء","كم عدد اقمار اورانص","K231"],
 ["إملاء","ماهو الثقب الاسوود","G74"],
 ["إملاء","ماهي اشعاعات هوكنج","K35"],
 // ── صيغ مختلفة للمعنى نفسه
 ["صيغة","كم تبلغ المسافة بين الأرض والقمر","K86"],
 ["صيغة","درجة حرارة الشمس","K71"],
 ["صيغة","هل نزل الإنسان على القمر فعلا","K50"],
 ["صيغة","أكبر كوكب في المجموعة الشمسية","K97"],
 ["صيغة","ما هو أسخن كوكب","K77"],
 ["صيغة","هل فيه حياة على المريخ","K21"],
 ["صيغة","ما هو أقرب نجم لنا بعد الشمس","K74"],
 ["صيغة","كم ياخذ ضوء الشمس عشان يوصلنا","K47"],
 ["صيغة","ليش البحر يمد ويجزر","K90"],
 ["صيغة","كم عمر كوكب الأرض","K81"],
 ["صيغة","هل نقدر نشوف الكواكب بدون تلسكوب","K110"],
 ["صيغة","من وين تجي المذنبات","K118"],
 // ── التشكيل والهمزات والتاء المربوطة
 ["تشكيل","لِمَاذَا تَتَلَأْلَأُ النُّجُومُ؟","K1"],
 ["تشكيل","مسبار الامل الاماراتي","K53"],
 ["تشكيل","اين تقع مجموعتنا الشمسيه في المجره","K121"],
 ["تشكيل","مَا الْبُقْعَةُ الْحَمْرَاءُ فِي الْمُشْتَرِي","K22"],
 // ── خارج الموسوعة: يجب أن يقول «ما فيه جواب»
 ["خارج","وش أحسن جوال أشتريه","none"],
 ["خارج","كم سعر تذكرة رحلة سياحية للفضاء","none"],
 ["خارج","من فاز بكأس العالم 2022","none"],
 ["خارج","هل الثقوب الدودية حقيقية","none"],
 ["خارج","هل كوكب نيبيرو بيصطدم بالأرض","none"],
 ["خارج","كم عدد أقمار ستارلينك اللي في السما","none"],
 ["خارج","وش الطقس بكرة في الرياض","none"],
];
const {chromium}=require('playwright');
const verbose=process.argv.includes('-v');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.goto('file://'+process.cwd()+'/site.html');await p.waitForTimeout(500);
const res=await p.evaluate(cases=>cases.map(([type,q,exp])=>{
  const hits=searchKB(q),good=hits.filter(h=>h.score>=2);
  const pick=typeof kbPick==='function'?kbPick(hits):good[0],got=pick?pick.e.id:'none';
  const ok=[].concat(exp);
  const fragile=!!pick&&good.length>1&&good[0].score-good[1].score<0.5;
  return {type,q,exp:ok,got,pass:ok.includes(got),fragile,
    top:hits.slice(0,3).map(h=>h.e.id+' '+h.score.toFixed(1)+(h.cov!=null?' cov'+Math.round(h.cov*100)+'%':'')+' '+h.e.t.replace(/[​⁠-⁤]/g,'').slice(0,40)),
    toks:ktoks(q)};
}),CASES);
await b.close();
const byType={};let pass=0;
for(const r of res){(byType[r.type]=byType[r.type]||{n:0,ok:0}).n++;if(r.pass){pass++;byType[r.type].ok++;}}
const pct=x=>Math.round(x*100);
for(const r of res){
  if(r.pass&&!verbose)continue;
  const kind=r.pass?'ok  ':r.got==='none'?'MISS':r.exp.includes('none')?'MADE':'WRNG';
  console.log(kind,'['+r.type+']',r.q,'| expected',r.exp.join('/'),'| got',r.got);
  if(!r.pass||verbose)console.log('     tokens:',r.toks.join(' '),'\n     top:',r.top.join(' ; ')||'-');
}
const made=res.filter(r=>!r.pass&&r.exp.includes('none')).length,wrong=res.filter(r=>!r.pass&&!r.exp.includes('none')&&r.got!=='none').length,miss=res.filter(r=>!r.pass&&r.got==='none').length;
console.log('\nby type:');for(const [t,v] of Object.entries(byType))console.log('  '+t+': '+v.ok+'/'+v.n+' ('+pct(v.ok/v.n)+'%)');
console.log('fragile passes (top two within 0.5):',res.filter(r=>r.pass&&r.fragile).map(r=>r.q).join(' ، ')||0);
console.log('missed (said no answer but there is one):',miss,'| wrong fact:',wrong,'| answered an out-of-scope question:',made);
console.log('ASK SCORE '+pass+'/'+res.length+' ('+pct(pass/res.length)+'%)');
if(errs.length)console.log('ERR',errs);
})();
