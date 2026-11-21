# v1.4: hidden fingerprint in the public build (tools/fingerprint.py via build_public.py). Here: the search
# normalizer strips the fingerprint's invisible characters, and the version line.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,(s.count(o),o[:70])
    s=s.replace(o,n)
rep('function knorm(s){return String(s).toLowerCase()','function knorm(s){return String(s).replace(/[\\u200B\\u2060-\\u2064]/g,"").toLowerCase()')
rep('<small class="ver">الإصدار 1.3.1 · آخر تحديث 20 نوفمبر 2026</small>','<small class="ver">الإصدار 1.4 · آخر تحديث 21 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch28 ok')
