# Intermediario/Utils/audio_core.py
# pip install sounddevice numpy
from __future__ import annotations
import numpy as np, threading

try:
    import sounddevice as sd
    _HAS_SD = True
except Exception:
    _HAS_SD = False

# ======== DSP helpers (reusados por todos os SFX) ==========
def env_exp(n, sr, t_decay):
    t = np.arange(n) / sr
    return np.exp(-t / max(1e-4, t_decay)).astype(np.float32)

def sine(freq, dur, sr, phase=0.0):
    n = max(1, int(dur * sr))
    t = np.arange(n, dtype=np.float32) / sr
    return np.sin(2*np.pi*freq*t + phase).astype(np.float32)

def noise_white(dur, sr, amp=0.5):
    n = max(1, int(dur * sr))
    return (np.random.randn(n).astype(np.float32) * amp)

def lowpass_mavg(x, k=64):
    if k <= 1: return x.astype(np.float32, copy=False)
    kernel = np.ones(k, dtype=np.float32) / k
    return np.convolve(x.astype(np.float32, copy=False), kernel, mode="same").astype(np.float32)

def whoosh(dur, sr, start_freq=200, end_freq=2000):
    n = int(dur * sr)
    base = noise_white(dur, sr)
    steps = np.linspace(start_freq, end_freq, 6)
    seg = max(1, n // len(steps))
    out = np.zeros_like(base)
    pos = 0
    for cf in steps:
        k = max(4, int(sr / max(200.0, cf)))
        chunk = base[pos:pos+seg]
        out[pos:pos+seg] = lowpass_mavg(chunk, k)
        pos += seg
    out *= env_exp(n, sr, dur*0.8) * 0.9
    return out.astype(np.float32)

def kick_click(sr, strength=1.0):
    dur = 0.06; n = int(dur*sr)
    body = sine(90, dur, sr)*0.7 + noise_white(dur, sr)*0.3
    out = (body * env_exp(n, sr, 0.045) * 0.9 * float(strength)).astype(np.float32)
    return out

def thud(sr):
    dur = 0.18; n = int(dur*sr)
    body = sine(80, dur, sr)*0.9 + noise_white(dur, sr)*0.35
    return (body * env_exp(n, sr, 0.09) * 0.85).astype(np.float32)

def slap(sr):
    dur = 0.12; n = int(dur*sr)
    body = noise_white(dur, sr)
    tone = sine(1400, 0.04, sr)
    if len(tone) < n:
        tone = np.pad(tone, (0, n-len(tone)))
    body = (body + tone[:n]*0.35)
    return (body * env_exp(n, sr, 0.06) * 0.9).astype(np.float32)

def crowd_loop(sr, seconds=4):
    n = int(seconds*sr)
    base = noise_white(seconds, sr)
    base = lowpass_mavg(base, k=int(sr/200))
    t = np.arange(n)/sr
    lfo = (0.75 + 0.25*np.sin(2*np.pi*0.2*t)).astype(np.float32)
    base += sine(200, seconds, sr) * 0.03
    base = (base * lfo * 0.15).astype(np.float32)
    return base

def goal_cheer(sr):
    dur=1.8; n=int(dur*sr)
    crowd = lowpass_mavg(noise_white(dur, sr), k=int(sr/300))
    swell = np.linspace(0.3, 1.0, n).astype(np.float32)
    crowd = (crowd * 0.22 * swell).astype(np.float32)
    wh = sine(1800, 0.25, sr) * env_exp(int(0.25*sr), sr, 0.12) * 0.45
    out = np.copy(crowd)
    out[:len(wh)] += wh
    return out

def save_groan(sr):
    dur=0.8; n=int(dur*sr)
    crowd = lowpass_mavg(noise_white(dur, sr), k=int(sr/300))
    env = np.linspace(1.0, 0.2, n).astype(np.float32)
    return (crowd * 0.2 * env).astype(np.float32)

# extras genéricos p/ outros minigames
def blip(sr, f=800, dur=0.06):        # clique/nota curtinha
    x = sine(f, dur, sr)
    return (x * env_exp(len(x), sr, dur*0.4) * 0.9).astype(np.float32)

def buzz(sr, f=120, dur=0.25):        # erro/buzz
    x = sine(f, dur, sr) + sine(f*2.01, dur, sr)*0.4
    return (x * env_exp(len(x), sr, dur*0.25) * 0.8).astype(np.float32)

def pop(sr, dur=0.08):                 # comer maçã / squash "pop"
    x = noise_white(dur, sr)*0.4 + sine(900, dur, sr)*0.3
    return (x * env_exp(len(x), sr, dur*0.35) * 0.9).astype(np.float32)

def chime(sr, dur=0.22):               # bonus/hit
    x = sine(1200, dur, sr) + sine(1600, dur, sr)*0.45
    return (x * env_exp(len(x), sr, dur*0.5) * 0.7).astype(np.float32)

def riser(sr, dur=0.4, f0=300, f1=1200):  # combo-up
    n = int(dur*sr)
    t = np.arange(n)/sr
    f = np.linspace(f0, f1, n)
    x = np.sin(2*np.pi*np.cumsum(f)/sr).astype(np.float32)
    return (x * env_exp(n, sr, dur*0.8) * 0.8).astype(np.float32)

# ============ Engine/mixer compartilhado =============
class _Voice:
    __slots__ = ("buf","idx","gain")
    def __init__(self, buf: np.ndarray, gain: float = 1.0):
        self.buf = buf.astype(np.float32, copy=False)
        self.idx = 0
        self.gain = float(gain)

class AudioEngineBase:
    def close(self): pass
    def start_ambient(self, buf: np.ndarray, vol=0.2): pass
    def stop_ambient(self): pass
    def play(self, buf: np.ndarray, gain=1.0): pass
    @property
    def samplerate(self): return 44100

class AudioEngine(AudioEngineBase):
    def __init__(self, samplerate=44100, blocksize=1024):
        if not _HAS_SD:
            self._silent = True
            self._sr = int(samplerate)
            self._voices = []
            self._ambient = None
            return
        self._silent = False
        self._sr = int(samplerate)
        self._block = int(blocksize)
        self._voices: list[_Voice] = []
        self._ambient: _Voice|None = None
        self._lock = threading.RLock()
        self._stream = sd.OutputStream(
            channels=1, samplerate=self._sr, blocksize=self._block,
            dtype="float32", callback=self._callback
        )
        self._stream.start()

    @property
    def samplerate(self): return self._sr

    def _callback(self, outdata, frames, tinfo, status):
        mix = np.zeros(frames, dtype=np.float32)
        with self._lock:
            if self._ambient is not None:
                v = self._ambient
                remain = frames; pos = 0
                while remain > 0:
                    c = min(remain, len(v.buf)-v.idx)
                    if c <= 0:
                        v.idx = 0
                        continue
                    mix[pos:pos+c] += v.buf[v.idx:v.idx+c]*v.gain
                    v.idx += c; pos += c; remain -= c
            alive = []
            for v in self._voices:
                c = min(frames, len(v.buf)-v.idx)
                if c > 0:
                    mix[:c] += v.buf[v.idx:v.idx+c]*v.gain
                    v.idx += c
                if v.idx < len(v.buf): alive.append(v)
            self._voices = alive
        np.clip(mix, -1.0, 1.0, out=mix)
        outdata[:,0] = mix

    def play(self, buf: np.ndarray, gain=1.0):
        if self._silent: return
        if buf is None or len(buf)==0: return
        with self._lock:
            self._voices.append(_Voice(buf, gain=gain))

    def start_ambient(self, buf: np.ndarray, vol=0.2):
        if self._silent: return
        if buf is None or len(buf)==0: return
        with self._lock:
            self._ambient = _Voice(buf, gain=float(vol))

    def stop_ambient(self):
        if self._silent: return
        with self._lock:
            self._ambient = None

    def close(self):
        if self._silent: return
        try:
            self._stream.stop(); self._stream.close()
        except Exception:
            pass

# fallback silencioso (mesma API)
if not _HAS_SD:
    class AudioEngine(AudioEngineBase):
        def __init__(self, *a, **k): self._sr = 44100
