import sys
import os
import re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fingerprint as fp
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src','ai-horizon.html'),encoding='utf-8').read()
i=src.index('</style>')+len('</style>')
head,body=src[:i],src[i:]
head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
body=body.replace('أفق يجيب الآن من معلومات الموسوعة المحفوظة. للحوار الكامل افتح الموقع داخل Claude.','أفق يجيب هنا من معلومات الموسوعة المحفوظة.')
ver=re.search(r'الإصدار ([0-9.]+)',src);bid=fp.build_id(src,ver.group(1) if ver else '0')
body,marked=fp.mark_kb(body)
SIG='<!-- أفق الذكاء (AI Horizon) · https://ufuq-ai.github.io/ · © 2026 تركي عبدالكريم الدغيمان وخالد يزيد العنزي. جميع الحقوق محفوظة. نسخ الكود أو المحتوى أو إعادة نشره دون إذن مكتوب مخالف للترخيص. بصمة الإصدار: '+bid+' --><meta name="ufuq-build" content="'+bid+'">'
GUARD=('<script>/* أفق الذكاء · '+bid+' */(function(){try{'
 'var o=["oi.buhtig.ia-qufu"].map(function(s){return s.split("").reverse().join("")}),h=(location.hostname||"").toLowerCase(),p=location.protocol;'
 'console.log("%cأفق الذكاء","font:700 20px sans-serif;color:#7b45ff","\\n© 2026 تركي عبدالكريم الدغيمان وخالد يزيد العنزي. جميع الحقوق محفوظة.\\nالموقع الأصلي: https://ufuq-ai.github.io/\\nنسخ الكود أو المحتوى دون إذن مكتوب مخالف للترخيص.\\nبصمة الإصدار: '+bid+'");'
 'if(p==="file:"||!h||h==="localhost"||h==="127.0.0.1"||o.indexOf(h)>=0||/\\.translate\\.goog$/.test(h)||h==="web.archive.org")return;'
 'var b=document.createElement("div");b.setAttribute("role","note");b.className="ufq-copy";'
 'b.style.cssText="position:relative;z-index:60;background:#ffd796;color:#2a1a00;text-align:center;font:700 14px/1.7 Tahoma,sans-serif;padding:8px 14px;direction:rtl";'
 'b.innerHTML="هذه نسخة منقولة من «أفق الذكاء». الموقع الأصلي: <a href=\\"https://ufuq-ai.github.io/\\" dir=\\"ltr\\" style=\\"color:#5a2d00;text-decoration:underline;white-space:nowrap;unicode-bidi:isolate\\">ufuq-ai.github.io</a> · من إعداد تركي عبدالكريم الدغيمان وخالد يزيد العنزي";'
 'document.body.insertBefore(b,document.body.firstChild);'
 '}catch(e){}})();</script>')
out=('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'+SIG+'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="author" content="تركي عبدالكريم الدغيمان، خالد يزيد العنزي"><meta name="copyright" content="© 2026 تركي عبدالكريم الدغيمان وخالد يزيد العنزي. جميع الحقوق محفوظة.">'
 '<meta name="description" content="أفق الذكاء: موسوعة عربية لعلوم الفلك والفضاء ودور الذكاء الاصطناعي فيها، ببحث فوري ومواضيع وأدوات ومختبر واختبارات.">'
 '<meta name="theme-color" content="#0b0822"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta property="og:type" content="website"><meta property="og:site_name" content="أفق الذكاء"><meta property="og:locale" content="ar_SA"><meta property="og:url" content="https://ufuq-ai.github.io/"><meta property="og:title" content="أفق الذكاء · موسوعة عربية للفلك والفضاء"><meta property="og:description" content="301 معلومة موثقة بمصادرها، ومساعد «أفق» يجيبك منها، ومختبر للذكاء الاصطناعي، وورشة تبني فيها صاروخك وتطلقه. مشروع طلابي من متوسطة مجمع الملك سعود بن عبدالعزيز."><meta property="og:image" content="https://ufuq-ai.github.io/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="أفق الذكاء: موسوعة عربية للفلك والفضاء والذكاء الاصطناعي"><meta name="twitter:card" content="summary_large_image">'
 '<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
 +head+'</head><body>'+body+GUARD+'</body></html>')
for p in sys.argv[1:]:
    open(p,'w',encoding='utf-8').write(out)
print('built',len(out),'marked',marked,'build',bid)
