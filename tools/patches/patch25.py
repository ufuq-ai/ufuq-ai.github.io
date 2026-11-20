# v1.2: «حدث الأسبوع» strip in the home hero: one curated event (WEEK_EVENT) with a day-level countdown,
# a link to its encyclopedia entry, an "after" line until it expires. The weekly update refreshes WEEK_EVENT.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)

# ---------- markup: right under the lede ----------
rep('''موسوعة عربية للفلك والفضاء تستخدم الذكاء الاصطناعي: اسأل «أفق» فيجيبك من معلومات موثقة بمصادرها، وجرّب في المختبر كيف يكتشف الذكاء الاصطناعي الكواكب.</p>
''','''موسوعة عربية للفلك والفضاء تستخدم الذكاء الاصطناعي: اسأل «أفق» فيجيبك من معلومات موثقة بمصادرها، وجرّب في المختبر كيف يكتشف الذكاء الاصطناعي الكواكب.</p>
      <div id="wk-ev"></div>
''')

# ---------- data + renderer ----------
rep('const TOUR_K="ufuq-tour",TOUR_OFF="ufuq-tour-off";','''/* حدث الأسبوع: يحدّثه التحديث الأسبوعي. date يوم الحدث بتوقيت السعودية (YYYY-MM-DD) بلا ساعة ما لم تعلنها الجهة الرسمية،
   until آخر يوم يظهر فيه، entry رقم المعلومة في الموسوعة أو ""، after جملة تظهر بعد موعده ولا تدّعي نتيجة لم تتأكد. null يخفي الشريط. */
const WEEK_EVENT={title:"بيبي كولومبو تدخل مدار عطارد",note:"بعد رحلة دامت 8 سنوات، تدخل المركبة الأوروبية اليابانية مدار عطارد، ثم تنفصل مركبتاها في ديسمبر.",date:"2026-11-21",until:"2026-11-24",entry:"K266",after:"ننتظر تأكيد وكالة الفضاء الأوروبية لنجاح دخول المدار."};
function weekEvent(){
  const box=$("#wk-ev");if(!box)return;
  const E=WEEK_EVENT,day=v=>{const [y,m,d]=String(v).split("-").map(Number);return new Date(y,m-1,d);};
  if(!E||!E.date){box.remove();return;}
  const t0=new Date();t0.setHours(0,0,0,0);const d=day(E.date);
  if(t0>day(E.until||E.date)){box.remove();return;}
  const past=t0>d,today=t0.getTime()===d.getTime(),e=E.entry?KB_BY_ID[E.entry]:null;
  const b=el(e?"button":"div","wk-ev"+(today?" now":""));if(e)b.type="button";
  b.innerHTML=`<span class="wk-ic" aria-hidden="true"><svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="8" fill="#cbb999"/><circle cx="17" cy="17.5" r="2.2" fill="#a8957a" opacity=".75"/><circle cx="23" cy="23" r="1.4" fill="#a8957a" opacity=".6"/><ellipse cx="20" cy="20" rx="17" ry="7" transform="rotate(-24 20 20)" fill="none" stroke="#c3a6ff" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="33.6" cy="11.3" r="3" fill="#ffd796"/></svg></span>`
   +`<span class="wk-tx"><span class="wk-k">${past?"حدث هذا الأسبوع":"حدث الأسبوع"}</span><b>${E.title}</b><small>${past&&E.after?E.after:E.note}</small>${e?`<span class="wk-go">اقرأ التفاصيل في الموسوعة ←</span>`:""}</span>`
   +`<span class="wk-when"><b>${past?"حدث":daysText(d)}</b><small>${dateText(d)}</small></span>`;
  if(e)b.onclick=()=>goTo(e);
  box.replaceWith(b);
}
const TOUR_K="ufuq-tour",TOUR_OFF="ufuq-tour-off";''')
rep('''  startCard();
''','''  startCard();
  weekEvent();
''')

# ---------- styles ----------
rep('/* home first impression */','''/* home: event of the week */
.wk-ev{display:flex;align-items:center;gap:14px;width:100%;max-width:640px;margin:22px auto 0;padding:12px 16px;border-radius:16px;text-align:start;color:var(--sky-fg);background:linear-gradient(90deg,rgba(255,215,150,.14),rgba(255,255,255,.06) 62%);border:1px solid rgba(255,215,150,.45);box-shadow:0 8px 26px rgba(0,0,0,.25);font:inherit;line-height:1.6}
button.wk-ev{cursor:pointer;transition:border-color .2s,transform .2s}
button.wk-ev:hover{border-color:#ffd796;transform:translateY(-1px)}
.wk-ic{position:relative;flex:none;width:44px;height:44px;display:grid;place-items:center}
.wk-ic::after{content:"";position:absolute;inset:-2px;border-radius:50%;border:2px solid #ffd796;opacity:0;animation:wkp 2.4s ease-out infinite}
.wk-ev.now .wk-ic::after{animation-duration:1.2s}
@keyframes wkp{0%{transform:scale(.65);opacity:.8}100%{transform:scale(1.2);opacity:0}}
.wk-tx{flex:1;min-width:0;display:flex;flex-direction:column}
.wk-k{font-size:.78rem;font-weight:700;color:#ffd796}
.wk-tx b{font-family:var(--f-display);font-size:1.08rem;font-weight:700;color:#fff;line-height:1.5}
.wk-tx small{font-size:.86rem;color:var(--sky-muted);line-height:1.7}
.wk-go{font-size:.84rem;font-weight:600;color:var(--sky-accent);margin-top:2px}
.wk-when{flex:none;align-self:stretch;display:flex;flex-direction:column;justify-content:center;text-align:center;padding-inline-start:14px;border-inline-start:1px solid var(--sky-line);min-width:88px}
.wk-when b{display:block;font-family:var(--f-display);font-size:1.35rem;color:#ffd796;line-height:1.3}
.wk-when small{display:block;font-size:.76rem;color:var(--sky-muted)}
@media (max-width:560px){.wk-ev{display:grid;grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:"ic k w" "t t t" "n n n" "g g g";column-gap:10px;row-gap:0;align-items:center;padding:12px 14px}.wk-ic{grid-area:ic;width:34px;height:34px}.wk-ic svg{width:32px;height:32px}.wk-tx{display:contents}.wk-k{grid-area:k}.wk-tx b{grid-area:t;margin-top:8px}.wk-tx small{grid-area:n}.wk-go{grid-area:g}.wk-when{grid-area:w;flex-direction:row;align-items:baseline;gap:6px;align-self:center;min-width:0;border:0;padding:3px 12px;border-radius:999px;background:rgba(255,215,150,.15)}.wk-when b{font-size:1rem}.wk-when small{font-size:.74rem}}

/* home first impression */''')

# ---------- version 1.2 (new feature) ----------
rep('<small class="ver">الإصدار 1.1.3 · آخر تحديث 20 نوفمبر 2026</small>','<small class="ver">الإصدار 1.2 · آخر تحديث 20 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch25 ok')
