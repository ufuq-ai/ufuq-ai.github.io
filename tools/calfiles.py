#!/usr/bin/env python3
"""ملفات التقويم لأحداث السماء: cal/YYYYMMDD.ics

يستعملها build_public.py: تقرأ قائمة allEvents() و WEEK_EVENT من الصفحة، وتكتب لكل حدث قادم ملف تقويم اسمه تاريخ الحدث
بتوقيت السعودية. زر «أضف إلى تقويمك» في الآيفون يفتح هذا الملف، لأن سفاري لا يقبل ملفات التقويم المصنوعة داخل الصفحة.
الأحداث السنوية (nextAnnual) تُكتب لسنتين حتى يبقى الملف موجودًا حين ينتقل الموقع إلى موعد السنة التالية.
تجربة: python3 tools/calfiles.py   (يطبع الأحداث وأسماء ملفاتها دون أن يكتب شيئًا)
"""
import datetime as dt
import hashlib
import json
import os
import re
import sys

RIY = dt.timezone(dt.timedelta(hours=3))
SITE = 'https://ufuq-ai.github.io/'
STR = r'"((?:[^"\\]|\\.)*)"'
ITEM = re.compile(r'\{t:' + STR + r',d:(?:new Date\(Date\.UTC\(([^)]*)\)\)|nextAnnual\((\d+),(\d+)\)),note:' + STR + r'([^}]*)\}')
WEEK = re.compile(r'const WEEK_EVENT=\{title:' + STR + r',note:' + STR + r',date:"(\d{4}-\d{2}-\d{2})"[^}]*?entry:"([KG]?\d*)"')


def _js(s):
    return json.loads('"' + s + '"')


def events(src, now=None):
    """Upcoming events as dicts with t, note, key (Saudi date YYYYMMDD), hash, and start/end (UTC) or day."""
    now = now or dt.datetime.now(dt.timezone.utc)
    out = []
    m = re.search(r'function allEvents\(\)\{\s*return \[(.*?)\]\.sort', src, re.S)
    for t, utc, am, ad, note, flags in ITEM.findall(m.group(1) if m else ''):
        starts = []
        if utc:
            p = [int(x) for x in utc.split(',')] + [0] * 5
            starts.append(dt.datetime(p[0], p[1] + 1, p[2], p[3], p[4], tzinfo=dt.timezone.utc))
        else:  # same rule as nextAnnual() in the page: 22:00 on that day, this year or the next
            y = now.astimezone(RIY).year
            for yy in (y, y + 1, y + 2):
                s = dt.datetime(yy, int(am), int(ad), 22, 0, tzinfo=RIY)
                if s >= now - dt.timedelta(days=1):
                    starts.append(s.astimezone(dt.timezone.utc))
            starts = starts[:2]
        for start in starts:
            if start <= now:
                continue
            out.append({'t': _js(t), 'note': _js(note), 'start': start, 'end': start + dt.timedelta(minutes=60),
                        'hash': '#saudi' if 'big:true' in flags else '#tools', 'key': start.astimezone(RIY).strftime('%Y%m%d')})
    w = WEEK.search(src)
    if w:
        t, note, day, entry = w.groups()
        d = dt.date.fromisoformat(day)
        if d >= now.astimezone(RIY).date():
            out.append({'t': _js(t), 'note': _js(note), 'day': d, 'hash': ('#k-' + entry) if entry else '', 'key': d.strftime('%Y%m%d')})
    return out


def _esc(t):
    return t.replace('\\', '\\\\').replace('\r\n', '\n').replace('\n', '\\n').replace(',', '\\,').replace(';', '\\;')


def _fold(line):
    out, cur, n, lim = [], '', 0, 75
    for ch in line:
        b = len(ch.encode('utf-8'))
        if n + b > lim:
            out.append(cur)
            cur, n, lim = '', 0, 74
        cur += ch
        n += b
    out.append(cur)
    return '\r\n '.join(out)


def _vevent(e):
    link = SITE + e['hash']
    if 'day' in e:
        a, b = e['day'].strftime('%Y%m%d'), (e['day'] + dt.timedelta(days=1)).strftime('%Y%m%d')
        span, trig, stamp = ['DTSTART;VALUE=DATE:' + a, 'DTEND;VALUE=DATE:' + b], 'PT9H', a + 'T000000Z'
    else:
        f = '%Y%m%dT%H%M00Z'
        a = e['start'].strftime(f)
        span, trig, stamp = ['DTSTART:' + a, 'DTEND:' + e['end'].strftime(f)], '-PT1H', a  # stable stamp: no churn between builds
    uid = hashlib.sha1((e['t'] + a).encode('utf-8')).hexdigest()[:12] + '-' + a + '@ufuq-ai.github.io'
    desc = (e['note'] + '\n\n' if e['note'] else '') + 'من «أفق الذكاء»: ' + link
    return (['BEGIN:VEVENT', 'UID:' + uid, 'DTSTAMP:' + stamp] + span +
            ['SUMMARY:' + _esc(e['t']), 'DESCRIPTION:' + _esc(desc), 'URL:' + link,
             'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + _esc(e['t']), 'TRIGGER:' + trig, 'END:VALARM', 'END:VEVENT'])


def write(src, outdir, now=None):
    """Rewrite outdir/cal/*.ics for the upcoming events. Returns the number of files."""
    d = os.path.join(outdir, 'cal')
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.ics'):
            os.remove(os.path.join(d, f))
    by = {}
    for e in events(src, now):
        by.setdefault(e['key'], []).append(e)
    for k, evs in by.items():
        lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Ufuq AI//Arabic//AR', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH']
        for e in evs:
            lines += _vevent(e)
        lines.append('END:VCALENDAR')
        with open(os.path.join(d, k + '.ics'), 'w', encoding='utf-8', newline='') as fh:
            fh.write('\r\n'.join(_fold(x) for x in lines) + '\r\n')
    return len(by)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'src', 'ai-horizon.html')
    for e in events(open(path, encoding='utf-8').read()):
        print('cal/%s.ics' % e['key'], e.get('day') or e['start'].astimezone(RIY).strftime('%Y-%m-%d %H:%M'), e['t'])
