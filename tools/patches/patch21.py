# version label and last-update date in the footer (version 1.0, first official release at ufuq-ai.github.io)
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
o='    <small>المعلومات مبسطة لأغراض تعليمية، ومع كل معلومة رابط لمصدرها.</small>\n'
assert s.count(o)==1
s=s.replace(o,o+'    <small class="ver">الإصدار 1.0 · آخر تحديث 19 نوفمبر 2026</small>\n')
o='.sr-only{'
assert s.count(o)==1
s=s.replace(o,'footer .ver{display:block;margin-top:6px;opacity:.85}\n.sr-only{')
open(P,'w',encoding='utf-8').write(s);print('patch21 ok')
