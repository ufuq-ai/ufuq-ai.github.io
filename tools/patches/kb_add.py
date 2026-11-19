"""Add verified research entries (🟢 only) to the knowledge base.
usage: python3 kb_add.py [exclude_keys_comma_separated] [--dry]"""
import json, glob, re, sys, shutil
P = '/home/claude/ai-horizon.html'
D = '/home/claude/research_notes/توسيع مخزون أفق المعرفي/'
args = [x for x in sys.argv[1:] if not x.startswith('--')]
DRY = '--dry' in sys.argv
EXCLUDE = set(args[0].split(',')) if args and args[0] else set()
INCLUDE = set(args[1].split(',')) if len(args)>1 and args[1] else set()
FIX = {'phenomena_observing:8': [('نحو الساعة 7:52 مساءً', 'نحو الساعة 7:53 مساءً')]}
s = open(P, encoding='utf-8').read()
a = s.index('const KB_RAW = ['); b = s.index('const SRC', a)
existing = re.findall(r'\["(K\d+)",\s*"(\w+)",\s*"([^"]*)"', s[a:b])
maxid = max(int(k[1:]) for k, _, _ in existing)
def norm(t):
    t = re.sub(r'[ً-ْـ؟?!.،,\s«»"\'()]', '', t)
    return t.translate(str.maketrans('أإآةى', 'اااهي'))
seen = {norm(t) for _, _, t in existing}
ORDER = ['astronomy', 'galaxies', 'planets', 'blackholes', 'astrophysics', 'exploration', 'phenomena', 'ai']
cands, skipped = [], []
for f in sorted(glob.glob(D + '*.json')):
    data = json.load(open(f, encoding='utf-8'))
    for i, e in enumerate(data.get('entries', [])):
        key = f.split('/')[-1][:-5] + ':' + str(i)
        why = None
        if key in EXCLUDE: why = 'excluded'
        elif not str(e.get('confidence', '')).startswith('🟢') and key not in INCLUDE: why = 'not green'
        elif e.get('section') not in ORDER: why = 'bad section'
        elif not str(e.get('url', '')).startswith('http'): why = 'no url'
        elif norm(e['q']) in seen: why = 'duplicate'
        if why: skipped.append((key, why, e.get('q'))); continue
        seen.add(norm(e['q'])); cands.append((key, e))
cands.sort(key=lambda x: ORDER.index(x[1]['section']))
rows, srcs, manifest = [], {}, []
for n, (key, e) in enumerate(cands, start=maxid + 1):
    kid = 'K%d' % n
    a_txt = re.sub(r'\s+', ' ', e['a']).strip().replace('**', '')
    for o, n in FIX.get(key, []): assert o in a_txt, (key, o); a_txt = a_txt.replace(o, n)
    rows.append(json.dumps([kid, e['section'], e['q'].strip(), e['keywords'].strip(), a_txt,
                            'استنتاج' if e.get('inference') else '', e['source_name'].strip()], ensure_ascii=False))
    srcs[kid] = [e['url'].strip(), e['source_name'].strip()]
    manifest.append({'key': key, 'id': kid, 'section': e['section'], 'q': e['q'], 'url': e['url']})
print('add', len(rows), 'skip', len(skipped))
for k in skipped: print('  skip', *k)
if DRY: sys.exit()
shutil.copy(P, '/home/claude/ai-horizon-v2/pre-kb2.html')
end = s.index('\n];\n', a); assert end < b
s = s[:end] + '\n/* إضافات نوفمبر 2026 */\n' + ',\n'.join(rows) + ',' + s[end:]
k = s.index('const KB = [')
s = s[:k] + 'Object.assign(SRC,' + json.dumps(srcs, ensure_ascii=False) + ');\n' + s[k:]
open(P, 'w', encoding='utf-8').write(s)
json.dump(manifest, open(D + '../kb2_manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', manifest[0]['id'], '..', manifest[-1]['id'])
