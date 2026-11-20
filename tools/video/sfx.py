# Sound design for the 60 s Ufuq video (no music): a quiet space bed plus effects tied to what is on screen.
import json, math
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100; DUR = 60.0; N = int(SR * DUR)
rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N)
EV = json.load(open('events.json'))

def add(sig, start, gain=1.0, pan=0.0):
    i = int(round(start * SR))
    if i < 0: sig = sig[-i:]; i = 0
    if i >= N: return
    sig = sig[: N - i]
    a = (pan + 1) * math.pi / 4
    L[i:i + len(sig)] += sig * gain * math.cos(a)
    R[i:i + len(sig)] += sig * gain * math.sin(a)

def tt(d): return np.arange(int(d * SR)) / SR
def white(d): return rng.standard_normal(int(d * SR))
def filt(x, kind, f): return sosfilt(butter(2, f, btype=kind, fs=SR, output='sos'), x)

def svf_bp(x, fc, q=1.6):
    """state-variable band-pass with a per-sample cutoff array fc"""
    y = np.empty_like(x); lp = bp = 0.0; d = 1.0 / q
    for n in range(len(x)):
        f = 2 * math.sin(math.pi * min(fc[n], SR / 6) / SR)
        hp = x[n] - lp - d * bp
        bp += f * hp; lp += f * bp
        y[n] = bp
    return y

def whoosh(d, f0, f1, peak=0.6, q=1.4):
    t = tt(d); x = white(d)
    fc = f0 * (f1 / f0) ** (t / d)
    e = np.sin(np.pi * np.clip(t / d, 0, 1) ** (math.log(0.5) / math.log(peak))) ** 2
    y = svf_bp(x, fc, q) * e
    return y / (np.abs(y).max() + 1e-9)

def riser(d, f0=250, f1=6000):
    t = tt(d); x = white(d)
    y = svf_bp(x, f0 * (f1 / f0) ** (t / d), 2.5) * (t / d) ** 2.6
    y += 0.25 * np.sin(2 * np.pi * (180 * t + (700 - 180) * t * t / (2 * d))) * (t / d) ** 2
    return y / (np.abs(y).max() + 1e-9)

def impact(d=2.2, sub=52, shimmer=0.5):
    t = tt(d)
    boom = np.sin(2 * np.pi * (sub * t - 8 * t * t)) * np.exp(-t * 2.2)
    thump = filt(white(d), 'low', 220) * np.exp(-t * 9) * 6
    sh = filt(white(d), 'high', 5500) * np.exp(-t * 2.0) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * t)) * shimmer
    y = boom + thump + sh
    y *= np.minimum(1, t * 300)
    return y / (np.abs(y).max() + 1e-9)

def bubble(f0, d=0.16):
    t = tt(d)
    f = f0 * (1 + 1.1 * (1 - np.exp(-t * 45)))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * np.minimum(1, t * 600)
    return y

def tick(f=2600, d=0.05):
    t = tt(d)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 260) + filt(white(d), 'band', [2000, 7000]) * np.exp(-t * 500) * 0.5
    return y

def key():
    d = 0.06; t = tt(d)
    y = filt(white(d), 'band', [1800, 5200]) * np.exp(-t * 320) * 0.9
    y += np.sin(2 * np.pi * rng.uniform(150, 210) * t) * np.exp(-t * 90) * 0.6
    return y

def bell(f, d=2.0):
    t = tt(d)
    y = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)
    return y * np.exp(-t * 2.8) * np.minimum(1, t * 500)

def beep(f, d):
    t = tt(d)
    e = np.minimum(1, t * 200) * np.minimum(1, (d - t) * 60)
    return (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)) * e

def clank(scale=1.0):
    d = 0.9; t = tt(d); y = np.zeros_like(t)
    for f, dec, a in ((410, 7, 1), (1135, 11, .7), (1880, 15, .5), (2690, 20, .35), (3720, 26, .25)):
        y += a * np.sin(2 * np.pi * f * scale * t + rng.uniform(0, 6.28)) * np.exp(-t * dec)
    y += filt(white(d), 'band', [600, 4000]) * np.exp(-t * 120) * 1.4
    return y / np.abs(y).max()

def blip(f):
    d = 0.09; t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t * 400) * np.exp(-t * 38)

def swish(d):
    t = tt(d)
    y = filt(white(d), 'band', [1800, 7000]) * np.sin(np.pi * t / d) ** 2
    return y / (np.abs(y).max() + 1e-9)

# ---------- space bed (whole video) ----------
b = np.cumsum(rng.standard_normal(N)); b = filt(b, 'high', 25); b = filt(b, 'low', 320)
b /= np.abs(b).max()
air = filt(rng.standard_normal(N), 'band', [2500, 6000]); air /= np.abs(air).max()
T = np.arange(N) / SR
bed = b * (0.8 + 0.2 * np.sin(2 * np.pi * T / 13)) + air * 0.06 * (0.6 + 0.4 * np.sin(2 * np.pi * T / 7.3 + 1))
add(bed, 0, gain=0.085)

# ---------- intro ----------
add(whoosh(0.75, 300, 3200, peak=.85), 0.0, 0.32)
add(impact(2.4, 48, .6), 0.7, 0.62)
add(whoosh(0.6, 900, 4200, peak=.5), 1.05, 0.16, pan=-.2)
add(tick(2200), 1.9, 0.10, pan=.2); add(tick(2500), 2.7, 0.09, pan=-.2)
add(whoosh(0.8, 4200, 380, peak=.3), 5.85, 0.26)
# ---------- hook ----------
for i, (st, f) in enumerate(((6.8, 420), (7.8, 500), (8.8, 600))):
    add(bubble(f), st, 0.42, pan=(-.3, .3, 0)[i])
add(riser(1.05), 8.9, 0.24)
add(impact(2.6, 55, .8), 9.95, 0.72)
add(bell(1046.5, 2.4), 9.97, 0.10, pan=-.3); add(bell(1568, 2.4), 10.0, 0.08, pan=.3)
add(whoosh(1.1, 260, 2600, peak=.6), 11.5, 0.34)
# ---------- encyclopedia ----------
last = 0
for i in range(int(1.8 * 600)):
    t = 12.6 + i / 600; x = min(1, (t - 12.6) / 1.8); n = round(301 * (1 - (1 - x) ** 3))
    if n // 10 > last // 10:
        add(tick(2900, .04), t, 0.075, pan=rng.uniform(-.3, .3)); last = n
add(bell(1318.5, 1.6), 14.42, 0.13)
add(swish(2.2), 13.0, 0.035)
add(whoosh(0.4, 1500, 5000, peak=.5), 16.4, 0.12, pan=.3)
add(swish(3.6), 17.2, 0.03)
# ---------- ask Ufuq ----------
add(whoosh(0.6, 3600, 500, peak=.4), 20.75, 0.22)
for k in range(10):
    add(key(), 21.95 + k * 0.1 + rng.uniform(-.025, .025), 0.2, pan=rng.uniform(-.25, .25))
add(whoosh(0.35, 700, 5200, peak=.7), 24.25, 0.22, pan=-.2)
add(bubble(760, .2), 24.55, 0.36, pan=.2)
# ---------- lab ----------
add(whoosh(0.6, 3600, 500, peak=.4), 28.75, 0.22)
t = 30.0
PENT = [1046.5, 1174.7, 1318.5, 1568, 1760, 2093]
while t < 35.6:
    add(blip(PENT[rng.integers(0, len(PENT))]), t, 0.08, pan=rng.uniform(-.6, .6)); t += rng.uniform(.28, .5)
# ---------- workshop ----------
add(whoosh(0.6, 3600, 500, peak=.4), 36.75, 0.22)
add(clank(1.0), 37.6, 0.16, pan=-.2); add(clank(1.18), 38.35, 0.13, pan=.2)
# engine roar: ignited at T-3 (before the flight shot), full at liftoff, gone after the Kármán line
fs = EV['flight_start']; lo = EV['liftoff']; km = EV['karman']; s1 = EV['sep1']; i2 = EV['ign2']
d = km + 0.8 - (fs - 0.25); t = tt(d) + fs - 0.25
roar = filt(np.cumsum(rng.standard_normal(len(t))), 'high', 30); roar = filt(roar, 'low', 520); roar /= np.abs(roar).max()
crk = filt(rng.standard_normal(len(t)) * (rng.random(len(t)) < .004) * 8, 'band', [800, 3500])
env = np.interp(t, [fs - .25, fs, lo - .4, lo, lo + .6, s1 - .05, s1, s1 + .05, i2, i2 + .15, km - .15, km + .55],
                   [0, .35, .5, 1.0, 1.0, .9, .15, .15, .2, .6, .45, 0])
add((roar + crk * .5) * env, fs - 0.25, 0.55)
add(beep(880, .14), EV['T-2'] + .02, 0.16); add(beep(880, .14), EV['T-1'], 0.16)
add(beep(1320, .45), lo, 0.17)
add(impact(2.8, 42, .3), lo, 0.62)
add(clank(.8), s1, 0.2); add(impact(1.0, 70, 0), s1, 0.18)
add(clank(1.1), EV['sep2'], 0.1)
add(bell(1568, 1.4), EV['orbit'], 0.10, pan=-.2); add(bell(2093, 1.4), EV['orbit'] + .08, 0.08, pan=.2)
add(whoosh(EV['cutoff'] - EV['tli'], 400, 2400, peak=.4) * 1.0, EV['tli'], 0.10)
add(tick(1900, .05), EV['probe'], 0.10)
add(riser(EV['arrive'] - EV['soi'] + .05, 500, 4000), EV['soi'], 0.12)
for k, f in enumerate((1046.5, 1318.5, 1568, 2093)):
    add(bell(f, 2.0), EV['arrive'] + k * .07, 0.12, pan=-.3 + .2 * k)
for k, f in enumerate((1568, 1760, 2093)):            # the three stars
    add(bell(f, 1.0), EV['result'] + .15 + k * .14, 0.11, pan=-.3 + .3 * k)
add(whoosh(0.75, 2800, 260, peak=.35), 49.35, 0.26)
# ---------- more ----------
add(whoosh(0.5, 700, 3800, peak=.5), 49.95, 0.14)
for k in range(4):
    add(bubble(520 + 70 * k, .14), 50.25 + k * .2, 0.26, pan=(-.4, .4, -.2, .2)[k])
add(whoosh(0.7, 3600, 400, peak=.35), 54.35, 0.22)
# ---------- outro ----------
add(impact(3.0, 46, .7), 55.35, 0.6)
add(bell(1046.5, 2.6), 56.05, 0.12, pan=-.2); add(bell(1568, 2.6), 56.11, 0.10, pan=.2)
add(tick(2300), 56.65, 0.08); add(tick(2500), 57.05, 0.07); add(tick(2700), 57.35, 0.06)

# ---------- small room reverb, master ----------
ir_t = tt(1.6); ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.6); ir[0] = 0
ir /= np.sqrt((ir ** 2).sum()) * 6
L2 = L + fftconvolve(L, ir)[:N] * .5; R2 = R + fftconvolve(R, rng.permutation(ir))[:N] * .5
fade = np.ones(N); fade[:int(.3 * SR)] = np.linspace(0, 1, int(.3 * SR)); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)) ** 1.5
st = np.stack([L2 * fade, R2 * fade], 1)
st /= np.abs(st).max()
st = np.tanh(st * 1.6) / np.tanh(1.6) * 0.9
wavfile.write('sfx.wav', SR, (st * 32767).astype(np.int16))
for a in range(0, 60, 5):
    s = st[a * SR:(a + 5) * SR]; print(a, round(20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9), 1), end='  ')
print()
