# hide the "report an error" button for now (reports from the public site had no way to reach the team)
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:80];s=s.replace(o,n)
rep('ومع كل معلومة رابط لمصدرها. وجدت خطأ؟ افتح السؤال واضغط «بلّغ عن خطأ».</small>','ومع كل معلومة رابط لمصدرها.</small>')
rep('    acts.append(more,rb);ans.append(acts,rbox);','    acts.append(more);ans.append(acts,rbox);')
rep('كل معلومة في هذه الصفحة من مخزون «أفق»، ومعها رابط مصدرها. وجدت خطأ؟ افتح المعلومة في الموسوعة واضغط «بلّغ عن خطأ».</p>','كل معلومة في هذه الصفحة من مخزون «أفق»، ومعها رابط مصدرها.</p>')
open(P,'w',encoding='utf-8').write(s);print('patch20 ok')
