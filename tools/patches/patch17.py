import re,sys
SP='/home/claude/ai-horizon-v2/rw/'
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,cnt=1):
    global s
    assert s.count(o)==cnt,(s.count(o),o[:80]);s=s.replace(o,n)
def cut(a,b,n):
    global s
    i=s.index(a);j=s.index(b,i);s=s[:i]+n+s[j:]
# 1) CSS: old builder styles -> workshop styles
cut('/* rocket builder game */','</style>',open(SP+'rw.css',encoding='utf-8').read())
# 2) JS: old builder -> workshop engine/draw/fly/ui + CTA
js=''.join(open(SP+f,encoding='utf-8').read().rstrip()+'\n' for f in ['rw-engine.js','rw-draw.js','rw-fly.js','rw-ui.js'])
cta='''function rwCta(kick,title,text){const a=el("a","lab-cta rw-cta");a.href="#build";
  a.innerHTML=`<div><span class="kick">${kick}</span><h3>${title}</h3><p>${text}</p><span class="link-btn">افتح الورشة ←</span></div><svg class="mini-lc" viewBox="0 0 240 90" aria-hidden="true"><path d="M-10 92 Q120 52 250 92Z" fill="#2a63c9" opacity=".55"/><path d="M-10 92 Q120 52 250 92" fill="none" stroke="#8fd3ff" stroke-width="2" opacity=".7"/><circle cx="200" cy="14" r="1.3" fill="#fff"/><circle cx="150" cy="8" r="1" fill="#fff"/><circle cx="96" cy="16" r="1.1" fill="#fff" opacity=".7"/><circle cx="230" cy="40" r="1" fill="#fff" opacity=".7"/><path d="M52 66 C80 18 150 8 214 26" fill="none" stroke="#ffd796" stroke-width="1.6" stroke-dasharray="4 4"/><g transform="translate(214 26) rotate(70)"><rect x="-3" y="-7" width="6" height="12" rx="1.5" fill="#f4f1ff"/><path d="M-3 -7 L0 -12 L3 -7Z" fill="#f4f1ff"/><path d="M-9 -3h5v4h-5zM4 -3h5v4H4z" fill="#5fb0ff"/></g><path d="M32 74h40v4H32z" fill="#4a4363"/><rect x="47" y="34" width="10" height="38" rx="2" fill="#f4f1ff"/><path d="M47 34 L52 22 L57 34Z" fill="#f4f1ff"/><rect x="47" y="50" width="10" height="3" fill="#2b2840"/><rect x="47" y="60" width="10" height="2" fill="#c3a6ff"/><path d="M47 66 L42 74 H47Z M57 66 L62 74 H57Z" fill="#c3a6ff"/><path d="M65 30 h6 M68 27 v6" stroke="#ffd796" stroke-width="1.6"/></svg>`;return a;}
'''
cut('/* ---------- rocket builder game: assemble a rocket','/* ---------- capabilities: voice, comments, team data ---------- */',js+cta+'\n')
# 3) route
rep('  else if(h==="rocket") renderRocket();\n','  else if(h==="rocket") renderRocket();\n  else if(h==="build") renderWorkshop();\n')
# 4) Try page: CTA after the rocket one
rep('    <div id="t-rocket" class="rk-cta"></div>\n','    <div id="t-rocket" class="rk-cta"></div>\n    <div id="t-build"></div>\n')
rep('''  $("#t-rocket").replaceWith(rocketCta(''','''  $("#t-build").replaceWith(rwCta("جديد","ورشة الصواريخ","ركّب صاروخك قطعة قطعة: محركات وخزانات ومراحل وحمولة، ثم أطلقه وتابع رحلته لحظة بلحظة. ست مهمات من أول قفزة إلى الفضاء حتى الانطلاق نحو القمر."));
  $("#t-rocket").replaceWith(rocketCta(''')
rep('أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، والمجموعة الشمسية الآن، وتشريح الصاروخ، وقمر الليلة','أدوات صغيرة تقرّب لك السماء والفضاء: سماء الليلة، والمجموعة الشمسية الآن، وتشريح الصاروخ، وورشة الصواريخ، وقمر الليلة')
# 5) rocket page: step-3 builder -> link card to the workshop
cut('    <div class="lab-card" id="rb">','    <div class="rk-two">','    <div id="rk-build"></div>\n')
rep('''  const rbOff=rbSetup();
  labOff=()=>{clearInterval(timer);rbOff();};''','''  $("#rk-build").replaceWith(rwCta("جرّب بنفسك","ركّب صاروخك في ورشة الصواريخ","بعد أن عرفت أجزاء الصاروخ ومراحله: ركّب صاروخك من القطع، وأطلقه، وشاهد هل يصل إلى الفضاء أو المدار أو القمر."));
  labOff=()=>{clearInterval(timer);};''')
assert 'rbSetup' not in s and 'rb-grid' not in s and 'ufuq-rb"' not in s
open(P,'w',encoding='utf-8').write(s)
print('ok',len(s))
