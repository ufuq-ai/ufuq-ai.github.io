"""Apply reviewed corrections to existing knowledge entries (answer text, tag, source)."""
import json, re, sys
P = '/home/claude/ai-horizon.html'
s = open(P, encoding='utf-8').read()
a0 = s.index('const KB_RAW = ['); b0 = s.index('const SRC', a0)
def row_span(kid):
    m = re.search(r'^\["%s",.*\],?$' % kid, s[a0:b0], re.M); assert m, kid
    return a0 + m.start(), a0 + m.end()
def edit(kid, a=None, sub=None, tag=None):
    global s
    i, j = row_span(kid); line = s[i:j]; comma = line.endswith(',')
    r = json.loads(line.rstrip(','))
    if a is not None: r[4] = a
    for o, n in (sub or []):
        assert o in r[4], (kid, o); r[4] = r[4].replace(o, n)
    if tag is not None: r[5] = tag
    s = s[:i] + json.dumps(r, ensure_ascii=False) + (',' if comma else '') + s[j:]
SRC = {}
def src(kid, url, name): SRC[kid] = [url, name]

edit('K13', a='تقترب أندروميدا منا، وكانت التوقعات القديمة ترجّح أن تندمج المجرتان. ثم قدّرت دراسة عام 2025 احتمال الاندماج خلال 10 مليارات سنة بنحو 50% فقط بسبب تأثير مجرات مجاورة. لكن دراسة نُشرت عام 2026 بقياسات أدق لحركة أندروميدا رفعت الاحتمال إلى نحو 90%، بعد نحو 6.5 مليار سنة في المتوسط. فالمسألة لم تُحسم بعد، وتحتاج قياسات أدق. وحتى لو حدث الاندماج، فاصطدام نجمين مباشرة نادر جدًا لأن المسافات بين النجوم هائلة.')
src('K13', 'https://kiaa.pku.edu.cn/info/1031/11252.htm', 'معهد كافلي للفلك والفيزياء الفلكية - جامعة بكين')
edit('K17', a='أبعد مجرة مؤكدة حتى الآن هي MoM-z14، التي أكّد تلسكوب جيمس ويب أنها كانت موجودة بعد نحو 280 مليون سنة فقط من الانفجار العظيم، وانزياحها نحو الأحمر 14.44. والأرقام القياسية في هذا المجال تتغير مع كل اكتشاف جديد.')
src('K17', 'https://www.esa.int/Science_Exploration/Space_Science/Webb/Webb_gazes_further_back_in_time', 'وكالة الفضاء الأوروبية')
edit('K11', a='قدّرت دراسة اعتمدت على بيانات تلسكوب هابل عام 2016 أن الكون المرئي يضم عشرة أضعاف ما كان يُظن على الأقل، أي نحو تريليوني مجرة بدل 100 إلى 200 مليار، وأن نحو 90% منها أخفت وأبعد من أن نرصدها حاليًا. والرقم تقدير يعتمد على نماذج لعدد المجرات الخافتة، وقد يتغير.', tag='تقدير')
src('K11', 'https://esahubble.org/news/heic1620/', 'وكالة الفضاء الأوروبية (هابل)')
edit('K25', a='زحل صاحب أكبر عدد من الأقمار المعروفة، إذ بلغ عدد أقماره المؤكدة 293 قمرًا حتى أغسطس 2026 بحسب ناسا، يليه المشتري. وهذه الأرقام تتغير مع الاكتشافات الجديدة، ومعظم هذه الأقمار صغيرة جدًا.')
src('K25', 'https://science.nasa.gov/saturn/moons/', 'ناسا')
i, j = row_span('K54'); r = json.loads(s[i:j].rstrip(','))
k = r[4].index('وفوييجر 1 أبعد جسم')
edit('K54', a=r[4][:k] + 'وفوييجر 1 أبعد جسم صنعه الإنسان، وموعد بلوغه مسافة يوم ضوئي كامل عن الأرض، أي نحو 25.9 مليار كيلومتر، هو 18 نوفمبر 2026 بحسب حسابات ناسا، فتحتاج إشارة الراديو يومًا كاملًا لتصل إليه.')
src('K54', 'https://science.nasa.gov/blogs/voyager/2026/10/29/nasas-voyager-1-conserves-power-resolves-brief-communications-pause/', 'ناسا')
i, j = row_span('K174'); r = json.loads(s[i:j].rstrip(','))
edit('K174', a=r[4].rstrip() + ' وبحسب صفحة ناسا المحدّثة عام 2026 بلغ عدد الكواكب التي أثبتها ExoMiner من بيانات كبلر 370 كوكبًا.')
src('K174', 'https://science.nasa.gov/open-science/deep-learning-exoplanets-tess/', 'ناسا')
edit('K176', sub=[('صُمّم ليلتقط', 'بدأ مسحه رسميًا عام 2026، ويلتقط')])
edit('K179', sub=[('فكانت النتيجة 500 عدسة مرشحة', 'فكانت النتيجة أكثر من 500 عدسة مرشحة')])
i, j = row_span('K179'); r = json.loads(s[i:j].rstrip(','))
m = re.search(r'\s*ويُتوقع أن يصل العدد[^.]*\.', r[4]); assert m; edit('K179', a=r[4][:m.start()] + r[4][m.end():])
src('K179', 'https://www.ift.uam-csic.es/en/euclid-opens-data-treasure-trove-to-study-the-dark-universe/', 'معهد الفيزياء النظرية بمدريد (اتحاد إقليدس)')
edit('K178', sub=[('استمرت شهرًا صنّف 9,976 متطوعًا', 'انطلقت في أغسطس 2024 صنّف آلاف المتطوعين')])
src('K178', 'https://www.ift.uam-csic.es/en/euclid-opens-data-treasure-trove-to-study-the-dark-universe/', 'معهد الفيزياء النظرية بمدريد (اتحاد إقليدس)')
src('K180', 'https://www.eurekalert.org/news-releases/985842', 'معهد الدراسات المتقدمة (IAS)')
edit('K166', a='ألّف البيروني (973–1048م) «القانون المسعودي» في الفلك وحركات الشمس والقمر والكواكب. أما ابن الهيثم (توفي نحو 1040م) فاشتهر بكتاب «المناظر» في علم الضوء والإبصار.')
edit('K162', a='عبد الرحمن الصوفي (903–986م) فلكي ألّف كتاب «صور الكواكب الثابتة» ورسم فيه الكوكبات نجمًا نجمًا. وتذكر ناسا أن كتابه، الذي يعود إلى عام 964م، يحوي أول وصف معروف لمجرة أندروميدا، التي تُرى بالعين المجردة لطخةً خافتة.')
src('K162', 'https://science.nasa.gov/mission/hubble/science/explore-the-night-sky/hubble-messier-catalog/messier-31/', 'ناسا')
i, j = row_span('K62'); r = json.loads(s[i:j].rstrip(','))
m = re.search(r'\s*وفي الربع الخالي فوهات وبار[^.]*\.', r[4]); assert m; edit('K62', a=r[4][:m.start()] + r[4][m.end():])
edit('K167', a='في العلا أربعة مواقع اعتمدتها منظمة DarkSky الدولية متنزهات للسماء المظلمة: منارة العلا ومحمية الغراميل، وهما الأولان في السعودية والخليج، ثم شرعان ووادي نخلة، بمساحة إجمالية 6,146 كيلومترًا مربعًا. واعتُمد عام 2025 أيضًا متنزه النفود للسماء المظلمة في حائل. وعمومًا كلما ابتعدت عن أضواء المدن ظهرت لك نجوم أكثر.')
src('K167', 'https://darksky.org/news/alula-expands-dark-sky-certification/', 'منظمة DarkSky الدولية')
i, j = row_span('K69'); r = json.loads(s[i:j].rstrip(','))
m = re.search(r'في جدة يبدأ الكسوف الكلي[^.]*\.', r[4]); assert m
edit('K69', a=r[4][:m.start()] + 'في جدة يبدأ الكسوف الكلي بعد الساعة 1:20 ظهرًا بقليل ويستمر قرابة 6 دقائق (نحو 5 دقائق و50 ثانية بحسب وكالة الفضاء السعودية)، وتختلف الأرقام قليلًا حسب الموقع داخل المدينة.' + r[4][m.end():])
src('K69', 'https://gulfnews.com/world/saudi-arabias-total-solar-eclipse-six-minutes-of-darkness-first-in-75-years-and-best-places-to-watch-1.500626094', 'غلف نيوز (عن وكالة الفضاء السعودية)')
k = s.index('const KB = [')
s = s[:k] + '/* تصحيحات نوفمبر 2026 */\nObject.assign(SRC,' + json.dumps(SRC, ensure_ascii=False) + ');\n' + s[k:]
open(P, 'w', encoding='utf-8').write(s)
print('fixed', 'K13 K17 K11 K25 K54 K174 K176 K179 K178 K180 K166 K162 K62 K167 K69')
