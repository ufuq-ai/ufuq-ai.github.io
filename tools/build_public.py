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
 '<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
 +head+'</head><body>'+body+'</body></html>')
for p in sys.argv[1:]:
    open(p,'w',encoding='utf-8').write(out)
print('built',len(out))
