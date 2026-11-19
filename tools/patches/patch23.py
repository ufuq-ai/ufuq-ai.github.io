# v1.1.1: link-preview image + site icon live in build_public.py and the repo root; here only the footer version.
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
o='<small class="ver">الإصدار 1.1 · آخر تحديث 19 نوفمبر 2026</small>'
assert s.count(o)==1
s=s.replace(o,'<small class="ver">الإصدار 1.1.1 · آخر تحديث 20 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch23 ok')
