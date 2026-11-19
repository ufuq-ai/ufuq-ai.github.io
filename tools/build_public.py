import sys
import os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'src','ai-horizon.html'),encoding='utf-8').read()
i=src.index('</style>')+len('</style>')
head,body=src[:i],src[i:]
head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
body=body.replace('أفق يجيب الآن من معلومات الموسوعة المحفوظة. للحوار الكامل افتح الموقع داخل Claude.','أفق يجيب هنا من معلومات الموسوعة المحفوظة.')
out=('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="author" content="تركي عبدالكريم الدغيمان، خالد يزيد العنزي"><meta name="copyright" content="© 2026 تركي عبدالكريم الدغيمان وخالد يزيد العنزي. جميع الحقوق محفوظة.">'
 '<meta name="description" content="أفق الذكاء: موسوعة عربية لعلوم الفلك والفضاء ودور الذكاء الاصطناعي فيها، ببحث فوري ومواضيع وأدوات ومختبر واختبارات.">'
 '<meta name="theme-color" content="#0b0822"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><meta property="og:type" content="website"><meta property="og:site_name" content="أفق الذكاء"><meta property="og:locale" content="ar_SA"><meta property="og:url" content="https://ufuq-ai.github.io/"><meta property="og:title" content="أفق الذكاء · موسوعة عربية للفلك والفضاء"><meta property="og:description" content="301 معلومة موثقة بمصادرها، ومساعد «أفق» يجيبك منها، ومختبر للذكاء الاصطناعي، وورشة تبني فيها صاروخك وتطلقه. مشروع طلابي من متوسطة مجمع الملك سعود بن عبدالعزيز."><meta property="og:image" content="https://ufuq-ai.github.io/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="أفق الذكاء: موسوعة عربية للفلك والفضاء والذكاء الاصطناعي"><meta name="twitter:card" content="summary_large_image">'
 '<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
 +head+'</head><body>'+body+'</body></html>')
for p in sys.argv[1:]:
    open(p,'w',encoding='utf-8').write(out)
print('built',len(out))
