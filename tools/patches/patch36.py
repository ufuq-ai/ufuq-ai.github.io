# v1.7.1: BepiColombo entered Mercury orbit (21 Nov 2026), confirmed by ESA.
#  - K266 answer rewritten in the past tense; its source is now Euronews' report quoting ESA's confirmation
#    (ESA's own «Latest updates» page had not been updated yet when this was written)
#  - WEEK_EVENT.after states the confirmed result; until stays as it was
#  - footer 1.7 -> 1.7.1, and the first fixes line of the newest CHANGELOG release
P='/home/claude/ai-horizon.html'
s=open(P,encoding='utf-8').read()
def rep(o,n,count=1):
    global s
    assert s.count(o)==count,(s.count(o),o[:70])
    s=s.replace(o,n)

rep('ومن المقرر أن تدخل المركبة مدار عطارد في 21 نوفمبر 2026، ثم تنفصل المركبتان عن بعضهما في 9 و10 ديسمبر 2026، ويبدأ العمل العلمي في أبريل 2027.", "", "وكالة الفضاء الأوروبية"],',
    'ثم دخلت المركبة مدار عطارد في 21 نوفمبر 2026، وأكدت وكالة الفضاء الأوروبية نجاح دخولها المدار. ومن المقرر أن تنفصل المركبتان عن بعضهما في 9 و10 ديسمبر 2026، ويبدأ العمل العلمي في أبريل 2027.", "", "يورونيوز"],')
rep('"K266": ["https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Latest_updates_BepiColombo_s_arrival_at_Mercury", "وكالة الفضاء الأوروبية"]',
    '"K266": ["https://www.euronews.com/2026/11/22/bepicolombo-space-probe-enters-mercurys-orbit-after-eight-year-journey", "يورونيوز"]')
rep('after:"ننتظر تأكيد وكالة الفضاء الأوروبية لنجاح دخول المدار."',
    'after:"أكدت وكالة الفضاء الأوروبية نجاح دخول بيبي كولومبو مدار عطارد."')
rep('<small class="ver">الإصدار 1.7 · آخر تحديث 22 نوفمبر 2026</small>',
    '<small class="ver">الإصدار 1.7.1 · آخر تحديث 22 نوفمبر 2026</small>')
rep('''  "رقم الإصدار في أسفل الموقع صار رابطًا إلى هذه الصفحة."]},''',
    '''  "رقم الإصدار في أسفل الموقع صار رابطًا إلى هذه الصفحة."],
  fixes:[{v:"1.7.1",date:"2026-11-22",text:"تحديث: بيبي كولومبو دخلت مدار عطارد."}]},''')
open(P,'w',encoding='utf-8').write(s);print('patch36 ok')
