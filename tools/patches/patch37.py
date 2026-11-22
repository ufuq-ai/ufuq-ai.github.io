# v0.8.1 (renumbering, no new version): every release before the public launch becomes 0.x, and the launch will be 1.0.
#  - CHANGELOG: 1.N -> 0.(N+1) and 1.N.M -> 0.(N+1).M (1.0 -> 0.1 ... 1.7.1 -> 0.8.1); the old 1.0 is no longer «the launch»
#  - #changelog: a «قبل الإطلاق» tag next to every 0.x version; the summary shows the launch date once a 1.x release exists,
#    else the first release date; the build log heading says «قبل الإصدار 0.1»; «how we number» explains the leading zero
#  - footer 1.7.1 -> 0.8.1 (same date: nothing new was released)
#  - git commit messages before this keep the old numbers (1.0 … 1.7.1)
import re
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

a=s.index('const CHANGELOG=['); b=s.index('const BUILD_LOG=[')
blk=s[a:b]
def renum(m):
    minor=int(m.group(1))+1
    return 'v:"0.%d%s"'%(minor,m.group(2) or '')
new,n=re.subn(r'v:"1\.(\d+)(\.\d+)?"',renum,blk)
assert n==15,n
assert '"1.' not in new
new=new.replace('title:"الإطلاق الرسمي الأول"','title:"أول إصدار كامل"',1)
s=s[:a]+new+s[b:]

rep('<small class="ver">الإصدار 1.7.1 · آخر تحديث 22 نوفمبر 2026</small>','<small class="ver">الإصدار 0.8.1 · آخر تحديث 22 نوفمبر 2026</small>')
rep(' ["2026-11-19","الإصدار 1.0."]',' ["2026-11-19","الإصدار 0.1."]')
rep('<summary>قبل الإصدار 1.0: بناء الموقع','<summary>قبل الإصدار 0.1: بناء الموقع')
rep('''  const nFix=CHANGELOG.reduce((n,r)=>n+(r.fixes||[]).length,0);''',
    '''  const nFix=CHANGELOG.reduce((n,r)=>n+(r.fixes||[]).length,0);
  const isPre=r=>r.v.startsWith("0."),launch=[...CHANGELOG].reverse().find(r=>!isPre(r)),first=CHANGELOG[CHANGELOG.length-1];''')
rep('''<div><b>${day(CHANGELOG[CHANGELOG.length-1].date)}</b><span>تاريخ أول إصدار رسمي</span></div>''',
    '''<div><b>${day((launch||first).date)}</b><span>${launch?"تاريخ الإطلاق":"تاريخ أول إصدار"}</span></div>''')
rep('''<li><b>الجزء الثالث</b>: إصلاح صغير أو تحديث للمعلومات.</li></ul>''',
    '''<li><b>الجزء الثالث</b>: إصلاح صغير أو تحديث للمعلومات.</li><li><b>الصفر في البداية</b>: الإصدارات التي تبدأ بصفر، مثل 0.8، سبقت الإطلاق الرسمي، والإطلاق هو الإصدار 1.0.</li></ul>''')
rep('ولا نكتب الصفر: بعد 1.4.2 جاء 1.5.','ولا نكتب الصفر: بعد 0.5.2 جاء 0.6.')
rep('''top.append(el("span","cl-v",r.v));if(i===0)top.append(el("span","cl-new","الأحدث"));top.append(t);''',
    '''top.append(el("span","cl-v",r.v));if(i===0)top.append(el("span","cl-new","الأحدث"));if(isPre(r))top.append(el("span","cl-pre-tag","قبل الإطلاق"));top.append(t);''')
rep('.cl-new{font-size:.75rem;font-weight:700;padding:2px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}',
    '.cl-new{font-size:.75rem;font-weight:700;padding:2px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}\n.cl-pre-tag{font-size:.75rem;font-weight:600;padding:1px 10px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}')
open(P,'w',encoding='utf-8').write(s);print('patch37 ok')
