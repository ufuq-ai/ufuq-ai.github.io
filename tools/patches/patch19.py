# new public address after moving the repository to the ufuq-ai organization
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
o='x.fillText("wfz52vvjf5-dev.github.io/ai-horizon",800,1035);'
assert s.count(o)==1;s=s.replace(o,'x.fillText("ufuq-ai.github.io",800,1035);')
open(P,'w',encoding='utf-8').write(s);print('patch19 ok')
