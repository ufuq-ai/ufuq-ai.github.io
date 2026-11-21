#!/usr/bin/env python3
"""بصمة أفق المخفية.

يستعملها build_public.py ليضع في كل معلومة من الموسوعة (في النسخة العامة فقط) بصمتين من حروف لا تُرى،
فيها رقم المعلومة. من ينسخ النص من الموقع تنتقل معه البصمة دون أن يراها.

كشف البصمة في نص مشبوه:
  python3 tools/fingerprint.py check ملف.txt      (أو ملف HTML محفوظ من موقع آخر)
  python3 tools/fingerprint.py check < نص.txt
"""
import hashlib
import re
import sys

# 2-bit symbols and a marker, all default-ignorable format characters: invisible, no effect on Arabic joining
# (they sit right after a space), ignored by the site's search.
SYM = ['​', '⁠', '⁡', '⁢']
MARK = '⁣'
TAG = 0xAF
ALL = ''.join(SYM) + MARK
STRIP_RE = re.compile('[' + ALL + ']')
FIND_RE = re.compile(MARK + '([' + ''.join(SYM) + ']{16})' + MARK)


def _sym(byte):
    return ''.join(SYM[(byte >> s) & 3] for s in (6, 4, 2, 0))


def encode(n):
    hi, lo = (n >> 8) & 255, n & 255
    data = [TAG, hi, lo, TAG ^ hi ^ lo ^ 0x5A]
    return MARK + ''.join(_sym(b) for b in data) + MARK


def decode(chunk):
    vals = [SYM.index(c) for c in chunk]
    data = [(vals[i] << 6) | (vals[i + 1] << 4) | (vals[i + 2] << 2) | vals[i + 3] for i in range(0, 16, 4)]
    if data[0] != TAG or data[3] != (TAG ^ data[1] ^ data[2] ^ 0x5A):
        return None
    return (data[1] << 8) | data[2]


def mark_text(text, n, at=(0.2, 0.65)):
    """Insert the mark for entry number n right after a space near each relative position."""
    sig = encode(n)
    out, used = text, set()
    for frac in sorted(at, reverse=True):  # from the end, so earlier positions stay valid
        i = out.find(' ', int(len(out) * frac))
        if i < 0 or i in used:
            continue
        used.add(i)
        out = out[:i + 1] + sig + out[i + 1:]
    return out


# a KB_RAW row up to the opening quote of its 5th field (the answer), with either spacing style
ROW_RE = re.compile(r'(\[\s*"K(\d+)"\s*,\s*"[a-z_]+"\s*,\s*"(?:[^"\\]|\\.)*"\s*,\s*"(?:[^"\\]|\\.)*"\s*,\s*")((?:[^"\\]|\\.)*)"')


def mark_kb(html):
    """Mark every encyclopedia answer (5th field of each KB_RAW row). Returns (html, count)."""
    count = 0

    def sub(m):
        nonlocal count
        count += 1
        return m.group(1) + mark_text(m.group(3), int(m.group(2))) + '"'
    return ROW_RE.sub(sub, html), count


def build_id(src, version):
    return 'v%s-%s' % (version, hashlib.sha256(src.encode('utf-8')).hexdigest()[:8])


def find(text):
    return [n for n in (decode(c) for c in FIND_RE.findall(text)) if n is not None]


def main():
    if len(sys.argv) < 2 or sys.argv[1] != 'check':
        print(__doc__)
        return
    text = open(sys.argv[2], encoding='utf-8', errors='replace').read() if len(sys.argv) > 2 else sys.stdin.read()
    ids = find(text)
    sig = 'UFUQ-AI' in text or 'ufuq-ai.github.io' in text
    if ids:
        uniq = sorted(set(ids))
        print('وُجدت بصمة أفق المخفية %d مرة، من %d معلومة: %s' % (len(ids), len(uniq), '، '.join('K%d' % n for n in uniq[:40])))
    else:
        print('لا توجد بصمة نصية مخفية.')
    if sig:
        print('ويوجد في النص توقيع أفق أو رابطه.')
    stray = len(STRIP_RE.findall(text))
    if stray and not ids:
        print('تنبيه: في النص %d حرفًا خفيًا من حروف البصمة بلا بصمة كاملة، ربما نُسخ جزء منها.' % stray)


if __name__ == '__main__':
    main()
