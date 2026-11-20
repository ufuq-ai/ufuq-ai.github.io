#!/usr/bin/env python3
"""روابط مصادر الموسوعة المطلوب فحصها هذا الأسبوع، بالتناوب 20 رابطًا كل أسبوع.

python3 tools/linkcheck.py            دفعة هذا الأسبوع
python3 tools/linkcheck.py --batch 3  دفعة محددة (تبدأ من 1)
python3 tools/linkcheck.py --all      كل الروابط

يقرأ خريطة SRC من tools/src/ai-horizon.html كما تقرؤها الصفحة: آخر Object.assign يغلب ما قبله.
الروابط المشتركة بين أكثر من معلومة تظهر مرة واحدة مع كل أرقامها.
"""
import datetime
import json
import math
import os
import re
import sys

SIZE = 20
EPOCH = datetime.date(2026, 11, 24)  # أول فحص

here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, 'src', 'ai-horizon.html'), encoding='utf-8').read()

src = {}
for i, u, n in re.findall(r'"(K\d+)":\s*\["(https?://[^"]+)",\s*"([^"]*)"\]', s):
    src[i] = (u, n)  # later blocks override earlier ones, like Object.assign

questions = {}
for m in re.finditer(r'\[\s*"(K\d+)"\s*,\s*"([a-z_]+)"\s*,\s*"((?:[^"\\]|\\.)*)"', s):
    questions.setdefault(m.group(1), m.group(3))

by_url = {}
for i, (u, n) in src.items():
    by_url.setdefault(u, {'url': u, 'name': n, 'ids': []})['ids'].append(i)
items = sorted(by_url.values(), key=lambda x: min(int(i[1:]) for i in x['ids']))
for it in items:
    it['ids'].sort(key=lambda i: int(i[1:]))
    it['questions'] = [questions.get(i, '') for i in it['ids']][:3]

batches = max(1, math.ceil(len(items) / SIZE))
args = sys.argv[1:]
if '--all' in args:
    sel, label = items, f'all {len(items)} urls'
else:
    if '--batch' in args:
        k = (int(args[args.index('--batch') + 1]) - 1) % batches
    else:
        k = ((datetime.date.today() - EPOCH).days // 7) % batches
    sel, label = items[k * SIZE:(k + 1) * SIZE], f'batch {k + 1} of {batches}'

print(json.dumps({'label': label, 'total_urls': len(items), 'urls': sel}, ensure_ascii=False, indent=1))
