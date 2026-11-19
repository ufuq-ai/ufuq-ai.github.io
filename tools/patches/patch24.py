# v1.1.2: new logo (planet horizon with rising sun) in the header; same art in favicon.svg, PNG icons and og.jpg (tools/brand).
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n):
    global s
    assert s.count(o)==1,o[:60]
    s=s.replace(o,n)
rep('<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="none" stroke="#efebfa" stroke-opacity=".35"/><path d="M2 16.5c6-3 16-3 22 0" fill="none" stroke="#c4abff" stroke-width="2" stroke-linecap="round"/><circle cx="17.5" cy="8" r="1.6" fill="#ffcd7a"/></svg>',
    '<svg class="logo" width="32" height="32" viewBox="0 0 64 64" aria-hidden="true"><defs><radialGradient id="lg-bg" cx="30%" cy="18%" r="100%"><stop offset="0" stop-color="#3d1f96"/><stop offset=".55" stop-color="#1a1245"/><stop offset="1" stop-color="#0b0822"/></radialGradient><linearGradient id="lg-pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cff"/><stop offset=".6" stop-color="#3b2296"/><stop offset="1" stop-color="#1b1150"/></linearGradient><radialGradient id="lg-gl"><stop offset="0" stop-color="#ffcd7a" stop-opacity=".55"/><stop offset="1" stop-color="#ffcd7a" stop-opacity="0"/></radialGradient><clipPath id="lg-cl"><rect width="64" height="64" rx="15"/></clipPath></defs><rect width="64" height="64" rx="15" fill="url(#lg-bg)"/><g clip-path="url(#lg-cl)"><circle cx="20" cy="17" r=".9" fill="#fff" opacity=".8"/><circle cx="50" cy="26" r=".8" fill="#fff" opacity=".6"/><circle cx="13" cy="31" r=".7" fill="#fff" opacity=".6"/><circle cx="41" cy="22" r="9" fill="url(#lg-gl)"/><circle cx="41" cy="22" r="5" fill="#ffcd7a"/><path d="M-2 47Q32 31 66 47V66H-2z" fill="url(#lg-pl)"/><path d="M-2 47Q32 31 66 47" fill="none" stroke="#e6dbff" stroke-width="2.4"/></g><rect x=".75" y=".75" width="62.5" height="62.5" rx="14.3" fill="none" stroke="#c4abff" stroke-opacity=".3" stroke-width="1.5"/></svg>')
rep('.brand{display:flex;','.brand .logo{flex:none;display:block;border-radius:8px;box-shadow:0 0 14px rgba(150,110,255,.35)}\n.brand{display:flex;')
rep('<small class="ver">الإصدار 1.1.1 · آخر تحديث 20 نوفمبر 2026</small>','<small class="ver">الإصدار 1.1.2 · آخر تحديث 20 نوفمبر 2026</small>')
open(P,'w',encoding='utf-8').write(s);print('patch24 ok')
