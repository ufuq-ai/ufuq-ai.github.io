# Minimal QR Code generator (byte mode, ECC level M, versions 1-10), after Nayuki's reference algorithm.
import sys
ECC_M = [None, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26]
BLK_M = [None, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5]

def raw_modules(v):
    r = (16 * v + 128) * v + 64
    if v >= 2:
        n = v // 7 + 2
        r -= (25 * n - 10) * n - 55
        if v >= 7:
            r -= 36
    return r

def data_cw(v):
    return raw_modules(v) // 8 - ECC_M[v] * BLK_M[v]

def gf_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z & 0xFF

def rs_divisor(deg):
    res = [0] * (deg - 1) + [1]
    root = 1
    for _ in range(deg):
        for j in range(deg):
            res[j] = gf_mul(res[j], root)
            if j + 1 < deg:
                res[j] ^= res[j + 1]
        root = gf_mul(root, 0x02)
    return res

def rs_rem(data, div):
    res = [0] * len(div)
    for b in data:
        f = b ^ res.pop(0)
        res.append(0)
        for i, c in enumerate(div):
            res[i] ^= gf_mul(c, f)
    return res

def encode(text):
    data = text.encode('utf-8')
    for v in range(1, 11):
        cap = data_cw(v) * 8
        cc = 8 if v <= 9 else 16
        if 4 + cc + 8 * len(data) <= cap:
            break
    else:
        raise ValueError('too long')
    bits = []
    def app(val, n):
        for i in range(n - 1, -1, -1):
            bits.append((val >> i) & 1)
    app(4, 4); app(len(data), cc)
    for b in data: app(b, 8)
    app(0, min(4, cap - len(bits)))
    app(0, (-len(bits)) % 8)
    pad = 0xEC
    while len(bits) < cap:
        app(pad, 8); pad ^= 0xEC ^ 0x11
    cws = [int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    # interleave with ECC
    nb, ecl = BLK_M[v], ECC_M[v]
    raw = raw_modules(v) // 8
    short_n = nb - raw % nb
    short_len = raw // nb
    div = rs_divisor(ecl)
    blocks = []; k = 0
    for i in range(nb):
        dl = short_len - ecl + (0 if i < short_n else 1)
        dat = cws[k:k + dl]; k += dl
        ec = rs_rem(dat, div)
        if i < short_n: dat = dat + [None]
        blocks.append(dat + ec)
    allcw = []
    for i in range(len(blocks[0])):
        for j, b in enumerate(blocks):
            if i != short_len - ecl or j >= short_n:
                allcw.append(b[i])
    return v, allcw

def build(text):
    v, cw = encode(text)
    size = v * 4 + 17
    M = [[0] * size for _ in range(size)]
    F = [[False] * size for _ in range(size)]
    def setf(x, y, d):
        M[y][x] = 1 if d else 0; F[y][x] = True
    for i in range(size):
        setf(6, i, i % 2 == 0); setf(i, 6, i % 2 == 0)
    def finder(cx, cy):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                d = max(abs(dx), abs(dy)); x, y = cx + dx, cy + dy
                if 0 <= x < size and 0 <= y < size:
                    setf(x, y, d not in (2, 4))
    finder(3, 3); finder(size - 4, 3); finder(3, size - 4)
    if v >= 2:
        n = v // 7 + 2
        step = 26 if v == 32 else (v * 4 + n * 2 + 1) // (n * 2 - 2) * 2
        pos = [6] + [size - 7 - i * step for i in range(n - 1)][::-1]
        for i in range(n):
            for j in range(n):
                if (i == 0 and j == 0) or (i == 0 and j == n - 1) or (i == n - 1 and j == 0):
                    continue
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        setf(pos[i] + dx, pos[j] + dy, max(abs(dx), abs(dy)) != 1)
    def draw_format(mask):
        data = (0 << 3) | mask  # ECC M bits = 00
        rem = data
        for _ in range(10): rem = (rem << 1) ^ ((rem >> 9) * 0x537)
        b = ((data << 10) | rem) ^ 0x5412
        g = lambda i: (b >> i) & 1
        for i in range(6): setf(8, i, g(i))
        setf(8, 7, g(6)); setf(8, 8, g(7)); setf(7, 8, g(8))
        for i in range(9, 15): setf(14 - i, 8, g(i))
        for i in range(8): setf(size - 1 - i, 8, g(i))
        for i in range(8, 15): setf(8, size - 15 + i, g(i))
        setf(8, size - 8, 1)
    draw_format(0)
    # data
    bits = []
    for c in cw:
        for i in range(7, -1, -1): bits.append((c >> i) & 1)
    i = 0; right = size - 1
    while right >= 1:
        if right == 6: right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j
                upward = ((right + 1) & 2) == 0
                y = size - 1 - vert if upward else vert
                if not F[y][x] and i < len(bits):
                    M[y][x] = bits[i]; i += 1
        right -= 2
    masks = [lambda x, y: (x + y) % 2 == 0, lambda x, y: y % 2 == 0, lambda x, y: x % 3 == 0,
             lambda x, y: (x + y) % 3 == 0, lambda x, y: (x // 3 + y // 2) % 2 == 0,
             lambda x, y: x * y % 2 + x * y % 3 == 0, lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
             lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0]
    def apply(mk):
        for y in range(size):
            for x in range(size):
                if not F[y][x] and masks[mk](x, y): M[y][x] ^= 1
    def penalty():
        p = 0
        for grid in (M, [list(c) for c in zip(*M)]):
            for row in grid:
                run = 1
                for k in range(1, size):
                    if row[k] == row[k - 1]:
                        run += 1
                    else:
                        if run >= 5: p += run - 2
                        run = 1
                if run >= 5: p += run - 2
                s = ''.join(map(str, row))
                p += 40 * (s.count('10111010000') + s.count('00001011101'))
        for y in range(size - 1):
            for x in range(size - 1):
                if M[y][x] == M[y][x + 1] == M[y + 1][x] == M[y + 1][x + 1]: p += 3
        dark = sum(map(sum, M)); total = size * size
        p += (abs(dark * 20 - total * 10) + total - 1) // total - 1 if False else (abs(dark * 20 - total * 10) // total) * 10
        return p
    best = None
    for mk in range(8):
        apply(mk); draw_format(mk); pen = penalty()
        if best is None or pen < best[0]: best = (pen, mk)
        apply(mk)
    apply(best[1]); draw_format(best[1])
    return M, v, best[1]

def svg(M, scale=10, border=4, fg='#1b1242', bg='#ffffff'):
    n = len(M); s = (n + 2 * border)
    path = ''.join(f'M{x+border},{y+border}h1v1h-1z' for y in range(n) for x in range(n) if M[y][x])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s*scale}" height="{s*scale}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="{bg}"/><path d="{path}" fill="{fg}"/></svg>'

if __name__ == '__main__':
    text = sys.argv[1]; out = sys.argv[2]
    M, v, mk = build(text)
    from PIL import Image
    n = len(M); sc = 12; b = 4
    img = Image.new('RGB', ((n + 2 * b) * sc,) * 2, 'white')
    px = img.load()
    for y in range(n):
        for x in range(n):
            if M[y][x]:
                for yy in range(sc):
                    for xx in range(sc):
                        px[(x + b) * sc + xx, (y + b) * sc + yy] = (27, 18, 66)
    img.save(out)
    open(out.rsplit('.', 1)[0] + '.svg', 'w').write(svg(M))
    print('version', v, 'mask', mk, 'size', n)
