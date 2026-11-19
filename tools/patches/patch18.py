# site-wide fixes from the full audit (applied after patch17)
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,cnt=1):
    global s
    assert s.count(o)==cnt,(s.count(o),o[:90]);s=s.replace(o,n)
# 1) dark theme: dark text on the light-violet accent (white was 2.7:1)
rep('--accent:#a888ff; --accent-soft:#2d2070; --accent-ink:#ffffff;','--accent:#a888ff; --accent-soft:#2d2070; --accent-ink:#160f2e;',2)
# 2) topic tags: darker text in light mode (some hues were 2.3:1)
rep('--ic-bs:95%; --ic-bl:91%; --ic-cs:82%; --ic-cl:40%; --wash:.10;','--ic-bs:95%; --ic-bl:91%; --ic-cs:82%; --ic-cl:40%; --wash:.10; --tag-cl:25%;')
rep('--ic-bs:78%; --ic-bl:23%; --ic-cs:96%; --ic-cl:75%; --wash:.20;','--ic-bs:78%; --ic-bl:23%; --ic-cs:96%; --ic-cl:75%; --wash:.20; --tag-cl:75%;',2)
rep('padding:1px 10px;background:hsl(var(--h) var(--ic-bs) var(--ic-bl));color:hsl(var(--h) var(--ic-cs) var(--ic-cl))}','padding:1px 10px;background:hsl(var(--h) var(--ic-bs) var(--ic-bl));color:hsl(var(--h) var(--ic-cs) var(--tag-cl,var(--ic-cl)))}')
# 3) small contrast and size fixes; screen-reader-only helper; narrow-screen formula
rep('.sa-chip{grid-column:3;grid-row:1;font-size:.75rem;border:1px solid currentColor;color:var(--gold,#b86b00);','.sa-chip{grid-column:3;grid-row:1;font-size:.75rem;border:1px solid currentColor;color:var(--warn,#8a4a00);')
rep('.sa-meta .src-link{font-size:.82rem}','.sa-meta .src-link{font-size:.82rem}\n.sa-meta small{font-size:inherit}\n.g-spot .kick{color:var(--accent)}\n.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}\n@media (max-width:440px){.eq-f{white-space:normal;line-height:1.7}}')
# 4) Saudi page: the sky gradient shared an id with the sky grid
rep('<linearGradient id="sa-sky" ','<linearGradient id="sa-sky-g" ')
rep('fill="url(#sa-sky)"','fill="url(#sa-sky-g)"')
# 5) Saudi page: count eclipse days by calendar day, like the Try page and the events list
rep('const daysLeft=big?Math.max(0,Math.ceil((big.d.getTime()-Date.now())/864e5)):0;','const daysLeft=big?(()=>{const a=new Date();a.setHours(0,0,0,0);const b=new Date(big.d);b.setHours(0,0,0,0);return Math.max(0,Math.round((b-a)/864e5));})():0;')
# 6) quiz page had no main heading
rep('  const w=el("section","wrap narrow quiz");const box=el("div","qbox");w.append(box);view.append(w);','  const w=el("section","wrap narrow quiz");const box=el("div","qbox");w.append(el("h1","sr-only","اختبر نفسك"),box);view.append(w);')
# 7) mobile nav: bring the current page's link into view
rep('function setNav(r){document.querySelectorAll(".links a").forEach(a=>{if(a.dataset.r===r)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});}',
    'function setNav(r){document.querySelectorAll(".links a").forEach(a=>{if(a.dataset.r===r){a.setAttribute("aria-current","page");const L=a.parentElement;if(L&&L.scrollWidth>L.clientWidth+2){const lr=L.getBoundingClientRect(),ar=a.getBoundingClientRect();L.scrollLeft+=(ar.left+ar.width/2)-(lr.left+lr.width/2);}}else a.removeAttribute("aria-current");});}')
# 8) glossary: only link encyclopedia questions that really mention the term
rep('const r=searchKB(t.ar+" "+t.en).filter(x=>x.e.c!=="glossary"&&x.score>=3).slice(0,2).map(x=>x.e);relCache.set(t.ar,r);return r;}',
    'const need=ktoks(t.ar),has=e=>{const f=new Set([...ktoks(e.t),...ktoks(e.a),...ktoks(e.k||"")]);return need.every(w=>f.has(w));};\n    const r=searchKB(t.ar+" "+t.en).filter(x=>x.e.c!=="glossary"&&x.score>=3&&has(x.e)).slice(0,2).map(x=>x.e);relCache.set(t.ar,r);return r;}')
# 9) a page title per page
rep('  if(!kept) window.scrollTo(0,0);\n}','  const h1=view.querySelector("h1"),nm=h1?h1.textContent.trim():"";document.title=nm&&nm!=="أفق الذكاء"&&h&&h!=="home"?nm+" · أفق الذكاء":"أفق الذكاء";\n  if(!kept) window.scrollTo(0,0);\n}')
open(P,'w',encoding='utf-8').write(s);print('patch18 ok',len(s))
