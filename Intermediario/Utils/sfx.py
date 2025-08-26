# utils/sfx.py
# Requisitos: pip install sounddevice numpy
from __future__ import annotations
import threading
import numpy as np

try:
    import sounddevice as sd
    _HAS_SD = True
except Exception:
    _HAS_SD = False


def _env_exp(n, sr, t_decay):
    """Envelope exponencial simples (decay)."""
    t = np.arange(n) / sr
    return np.exp(-t / max(1e-4, t_decay))


def _sine(freq, dur, sr, phase=0.0):
    n = int(dur * sr)
    t = (np.arange(n) / sr)
    return np.sin(2*np.pi*freq*t + phase).astype(np.float32)


def _noise_white(dur, sr):
    n = int(dur * sr)
    return (np.random.randn(n) * 0.5).astype(np.float32)


def _lowpass_mavg(x, k=64):
    """Filtro passa-baixas simples por média móvel."""
    if k <= 1:
        return x
    kernel = np.ones(k, dtype=np.float32) / k
    y = np.convolve(x, kernel, mode="same").astype(np.float32)
    return y


def _whoosh(dur, sr, start_freq=200, end_freq=2000):
    """Ruído filtrado com varredura de low-pass -> sensação de 'sopro'."""
    n = int(dur * sr)
    base = _noise_white(dur, sr)
    # varre cutoff pela duração
    steps = np.linspace(start_freq, end_freq, 6)
    seg = max(1, n // len(steps))
    out = np.zeros_like(base)
    pos = 0
    for cf in steps:
        k = max(4, int(sr / max(200.0, cf)))  # kernel ~ inverso da "freq"
        chunk = base[pos:pos+seg]
        out[pos:pos+seg] = _lowpass_mavg(chunk, k)
        pos += seg
    env = _env_exp(n, sr, t_decay=dur*0.8)
    return (out * env * 0.9).astype(np.float32)


def _kick_click(sr, strength=1.0):
    """Clique de chute/passe (transiente curto)."""
    dur = 0.06
    n = int(dur * sr)
    # transiente: seno grave curtíssimo + ruído
    body = _sine(90, dur, sr) * 0.7 + _noise_white(dur, sr) * 0.3
    env = _env_exp(n, sr, t_decay=0.045)
    return (body * env * 0.9 * strength).astype(np.float32)


def _thud(sr):
    """Impacto 'carrinho' (grave curto + ruído)."""
    dur = 0.18
    n = int(dur * sr)
    body = _sine(80, dur, sr) * 0.9 + _noise_white(dur, sr) * 0.35
    env = _env_exp(n, sr, t_decay=0.09)
    return (body * env * 0.85).astype(np.float32)


def _slap(sr):
    """'Defesa' (luva na bola): transiente médio com ruído."""
    dur = 0.12
    n = int(dur * sr)

    noise = _noise_white(dur, sr)            # 0.12s -> n amostras
    snap  = _sine(1400, 0.04, sr) * 0.35     # 0.04s -> menor

    # pad no 'snap' pra bater o tamanho do 'noise'
    if len(snap) < n:
        snap = np.pad(snap, (0, n - len(snap)))
    else:
        snap = snap[:n]

    body = noise + snap
    env = _env_exp(n, sr, t_decay=0.06)
    return (body * env * 0.9).astype(np.float32)



def _crowd_loop(sr, seconds=6):
    """Loop de torcida: ruído filtrado + grave de estádio + LFO de volume."""
    n = int(seconds * sr)

    # base de ruído -> passa-baixa (corta agudos)
    base = _noise_white(seconds, sr)
    base = _lowpass_mavg(base, k=max(8, int(sr / 500)))  # ~500 Hz

    # “rumble” de estádio (subgrave leve)
    rumble = (_sine(90, seconds, sr) * 0.25 +
              _sine(180, seconds, sr) * 0.12).astype(np.float32)

    # LFO de volume (0.18 Hz) pra dar vida
    t = np.arange(n) / sr
    lfo = (0.70 + 0.30 * np.sin(2*np.pi*0.18 * t)).astype(np.float32)

    out = (base * 0.65 + rumble * 0.35)
    out *= lfo

    # normaliza um pouco alto; volume final é controlado pelo gain do voice
    peak = float(np.max(np.abs(out))) or 1.0
    out = (out / peak) * 0.6
    return out.astype(np.float32)


def _goal_cheer(sr):
    """Animação de gol: crowd swell + apito curto (sine agudo)."""
    dur = 1.8
    n = int(dur * sr)
    crowd = _noise_white(dur, sr)
    crowd = _lowpass_mavg(crowd, k=int(sr/300))
    # swell (subindo)
    swell = np.linspace(0.3, 1.0, n).astype(np.float32)
    crowd = (crowd * 0.22 * swell).astype(np.float32)
    # apito
    wh = _sine(1800, 0.25, sr) * _env_exp(int(0.25*sr), sr, 0.12) * 0.45
    out = np.copy(crowd)
    out[:len(wh)] += wh
    return out


def _save_groan(sr):
    """Reação de 'ohhh' curta pra defesa/perda (crowd caindo)."""
    dur = 0.8
    n = int(dur * sr)
    crowd = _noise_white(dur, sr)
    crowd = _lowpass_mavg(crowd, k=int(sr/300))
    env = np.linspace(1.0, 0.2, n).astype(np.float32)
    return (crowd * 0.2 * env).astype(np.float32)


def _mix_pad(*waves, gain=1.0):
    """
    Soma buffers 1D de tamanhos diferentes com zero-padding.
    Normaliza se clipar (>1.0).
    """
    waves = [w.astype(np.float32, copy=False) for w in waves if w is not None]
    if not waves:
        return np.zeros(1, dtype=np.float32)
    L = max(w.shape[0] for w in waves)
    out = np.zeros(L, dtype=np.float32)
    for w in waves:
        out[:w.shape[0]] += w
    out *= float(gain)
    peak = float(np.max(np.abs(out)))
    if peak > 1.0:
        out /= peak
    return out


class _Voice:
    __slots__ = ("buf", "idx", "loop", "gain")

    def __init__(self, buf: np.ndarray, gain: float = 1.0, loop: bool = False):
        self.buf = buf.astype(np.float32, copy=False)
        self.idx = 0
        self.loop = loop
        self.gain = float(gain)


class SFXBase:
    """Interface base (e também fallback silencioso)."""
    def start(self): pass
    def close(self): pass
    def start_ambient(self, vol=0.18): pass
    def stop_ambient(self): pass
    def pass_kick(self): pass
    def dribble(self): pass
    def tackle(self): pass
    def shot(self): pass
    def goal(self): pass
    def save(self): pass


class SFX(SFXBase):
    def __init__(self, samplerate=44100, blocksize=1024):
        if not _HAS_SD:
            # fallback silencioso se sounddevice não estiver disponível
            self._silent = True
            return

        self._silent = False
        self.sr = int(samplerate)
        self.blocksize = int(blocksize)
        self._voices: list[_Voice] = []
        self._lock = threading.RLock()
        self._ambient = None  # _Voice ou None

        # pré-gerados
        self._buf_crowd = _crowd_loop(self.sr, seconds=4)
        self._buf_pass  = _kick_click(self.sr, strength=0.7)

        # NUNCA faça "_whoosh = ..." (isso sombreia a função e dá UnboundLocalError)
        kick   = _kick_click(self.sr, strength=1.0)          # ~0.06s
        whoosh = _whoosh(0.25, self.sr, 400, 2800)           # ~0.25s

        # Deixa os dois com o MESMO tamanho antes de somar (evita ValueError de shapes)
        L = max(len(kick), len(whoosh))
        if len(kick) < L:
            kick = np.pad(kick, (0, L - len(kick)))
        if len(whoosh) < L:
            whoosh = np.pad(whoosh, (0, L - len(whoosh)))

        self._buf_shot = (kick + whoosh).astype(np.float32)

        self._buf_drib  = _whoosh(0.22, self.sr, 300, 2000)
        self._buf_thud  = _thud(self.sr)
        self._buf_slap  = _slap(self.sr)
        self._buf_goal  = _goal_cheer(self.sr)
        self._buf_save  = _save_groan(self.sr)

        self._stream = sd.OutputStream(
            channels=1,
            samplerate=self.sr,
            blocksize=self.blocksize,
            dtype="float32",
            callback=self._callback
        )
        self._stream.start()


    # STREAM / MIX -------------------------------------------------
    def _callback(self, outdata, frames, tinfo, status):
        if self._silent:
            outdata[:] = 0
            return
        mix = np.zeros(frames, dtype=np.float32)

        with self._lock:
            # AMBIENT loop
            if self._ambient is not None:
                v = self._ambient
                # copia circular
                remain = frames
                pos = 0
                while remain > 0:
                    copy_n = min(remain, len(v.buf) - v.idx)
                    if copy_n <= 0:
                        v.idx = 0
                        continue
                    mix[pos:pos+copy_n] += v.buf[v.idx:v.idx+copy_n] * v.gain
                    v.idx += copy_n
                    pos += copy_n
                    remain -= copy_n

            # one-shots
            alive = []
            for v in self._voices:
                copy_n = min(frames, len(v.buf) - v.idx)
                if copy_n > 0:
                    mix[:copy_n] += v.buf[v.idx:v.idx+copy_n] * v.gain
                    v.idx += copy_n
                if v.idx < len(v.buf):
                    alive.append(v)
            self._voices = alive

        # evita clipping
        np.clip(mix, -1.0, 1.0, out=mix)
        outdata[:, 0] = mix

    def _push(self, buf: np.ndarray, gain=1.0):
        if self._silent:
            return
        with self._lock:
            self._voices.append(_Voice(buf, gain=gain, loop=False))

    # API ----------------------------------------------------------
    def start(self):  # mantido por compat
        pass

    def close(self):
        if self._silent:
            return
        try:
            if self._stream:
                self._stream.stop(); self._stream.close()
        except Exception:
            pass

    def start_ambient(self, vol=0.18):
        if self._silent:
            return
        with self._lock:
            self._ambient = _Voice(self._buf_crowd, gain=float(vol), loop=True)

    def stop_ambient(self):
        if self._silent:
            return
        with self._lock:
            self._ambient = None

    # Eventos de jogo ---------------------------------------------
    def pass_kick(self): self._push(self._buf_pass, gain=0.9)
    def dribble(self):   self._push(self._buf_drib, gain=0.8)
    def tackle(self):    self._push(self._buf_thud, gain=1.0)
    def shot(self):      self._push(self._buf_shot, gain=1.0)
    def goal(self):      self._push(self._buf_goal, gain=1.0)
    def save(self):      self._push(self._buf_slap, gain=1.0); self._push(self._buf_save, gain=1.0)


# Fallback silencioso (se sounddevice indisponível)
if not _HAS_SD:
    class SFX(SFXBase):
        pass
