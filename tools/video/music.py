# 60 s ambient space track for the Ufuq video: pads + bass + sparkles, a swell at "أفق يجيبك",
# a launch rumble when the rocket lifts off (~41.5 s), and a closing chime.
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 60.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 2
    e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l
    R[i:i + len(sig)] += sig * gain * r

def pad_voice(f, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.zeros(n)
    for det in (-0.12, 0.0, 0.11):           # cents-ish detune in Hz ratio
        ff = f * (1 + det / 100)
        for h in range(1, 7):                 # soft saw: few harmonics
            s += np.sin(2 * np.pi * ff * h * tt + rng.uniform(0, 6.28)) / (h ** 1.35)
    vib = 1 + 0.15 * np.sin(2 * np.pi * 0.2 * tt + rng.uniform(0, 6.28))
    return s * vib / 6

# D minor-ish progression (MIDI): Dm9, Bbmaj7, Fmaj7/A, C6/9 — each chord 4 s, 1.6 s crossfade
CH = [[50, 57, 62, 64, 65, 69], [46, 53, 57, 62, 65, 69], [45, 53, 57, 60, 64, 69], [48, 55, 60, 62, 64, 67]]
step = 4.0
for k in range(int(DUR / step) + 1):
    ch = CH[k % 4]
    st = k * step - 0.8
    d = step + 1.6
    for j, m in enumerate(ch[1:]):
        v = pad_voice(hz(m), d) * env(int(d * SR), 1.4, 1.6)
        add(v, max(st, 0), gain=0.055, pan=(-0.6 + 1.2 * j / 4))
    b = np.sin(2 * np.pi * hz(ch[0] - 12) * np.arange(int(d * SR)) / SR)
    b += 0.3 * np.sin(2 * np.pi * hz(ch[0]) * np.arange(int(d * SR)) / SR)
    add(b * env(int(d * SR), 1.0, 1.6), max(st, 0), gain=0.12 if k * step > 11.5 else 0.06)

# sparkles: chord tones two octaves up, bell-ish sine with decay
def bell(f, dur=1.4):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2.01 * tt) * np.exp(-tt * 6)
    return s * np.exp(-tt * 3.2) * np.minimum(1, tt * 400)

tt0 = 2.0
while tt0 < 57.5:
    k = int(tt0 // step) % 4
    ch = CH[k]
    m = ch[rng.integers(2, len(ch))] + 12 * (1 if rng.random() < .6 else 2)
    dense = 37.0 < tt0 < 49.5
    g = 0.05 if tt0 < 12 else 0.07
    add(bell(hz(m)), tt0, gain=g * rng.uniform(.6, 1), pan=rng.uniform(-.8, .8))
    tt0 += 0.25 if dense else (0.5 if tt0 > 12 else 0.75)

# swell + chime on «أفق يجيبك» (~10 s)
n = int(2.0 * SR); tt = np.arange(n) / SR
noise = rng.standard_normal(n)
sos = butter(2, [800, 6000], btype='band', fs=SR, output='sos')
sw = sosfilt(sos, noise) * (tt / 2.0) ** 3 * 0.25
add(sw, 8.0, gain=1.0)
for m, dt in ((74, 0), (81, .06), (86, .12)):
    add(bell(hz(m), 3.0), 10.0 + dt, gain=0.12, pan=(m - 81) / 10)

# launch: riser 37.5→41.5, boom + rumble at liftoff 41.5
n = int(4.0 * SR); tt = np.arange(n) / SR
sos = butter(2, 2500, btype='low', fs=SR, output='sos')
ri = sosfilt(sos, rng.standard_normal(n)) * (tt / 4.0) ** 2.5 * 0.35
add(ri, 37.5)
n = int(6.0 * SR); tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * (55 * np.exp(-tt * 0.6)) * tt) * np.exp(-tt * 1.1)
sos = butter(2, 260, btype='low', fs=SR, output='sos')
rumble = sosfilt(sos, rng.standard_normal(n)) * np.exp(-tt * 0.55) * np.minimum(1, tt * 8)
add(boom * 0.55 + rumble * 0.9, 41.5)

# closing chime on the outro (~55 s)
for m, dt in ((62, 0), (69, .08), (74, .16), (78, .24)):
    add(bell(hz(m), 4.0), 55.2 + dt, gain=0.11, pan=(m - 70) / 12)

# reverb: exponentially decaying noise impulse
irn = int(2.6 * SR); it = np.arange(irn) / SR
ir = rng.standard_normal(irn) * np.exp(-it * 2.4); ir /= np.abs(ir).sum() ** 0.5 * 18
wetL = fftconvolve(L, ir)[:N]; wetR = fftconvolve(R, ir[::-1].copy() if False else rng.permutation(ir))[:N]
L2 = L * 0.75 + wetL * 0.9; R2 = R * 0.75 + wetR * 0.9

# master fade and normalise
fade = np.ones(N)
fi, fo = int(1.2 * SR), int(2.2 * SR)
fade[:fi] = np.linspace(0, 1, fi) ** 2
fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
L2 *= fade; R2 *= fade
pk = max(np.abs(L2).max(), np.abs(R2).max())
st = np.stack([L2, R2], 1) / pk
st = np.tanh(st * 1.9) / np.tanh(1.9) * 0.89  # gentle saturation to lift the quiet pads
wavfile.write('music.wav', SR, (st * 32767).astype(np.int16))
rms = np.sqrt((st ** 2).mean())
print('ok peak', round(pk, 3), 'rms dBFS', round(20 * np.log10(rms), 1))
