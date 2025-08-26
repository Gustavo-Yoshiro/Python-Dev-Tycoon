# Intermediario/Utils/sfx_hero.py
from __future__ import annotations
import numpy as np
from .audio_core import (
    AudioEngine, sine, noise_white, env_exp, lowpass_mavg,
    kick_click, slap, chime, buzz, riser, thud
)

class SFXHero:
    """
    SFX do Python Hero: efeitos e música de fundo (loop).
    Expõe a API que a tela usa: hit/wrong/miss/combo_up/finish/wave_start/...
    """
    def __init__(self, engine: AudioEngine):
        self.e = engine
        self._silent = bool(getattr(engine, "_silent", False))
        if self._silent:
            print("[SFXHero] AudioEngine em modo silencioso (sem 'sounddevice'). "
                  "Instale: pip install sounddevice numpy")
        sr = self.e.samplerate
        # buffers de SFX curtos
        self.buf_hit       = chime(sr, 0.16)
        self.buf_hit_soft  = chime(sr, 0.12)
        self.buf_miss      = buzz(sr, 100, 0.25)
        self.buf_streak    = riser(sr, 0.45, 300, 1500)
        self.buf_fail      = thud(sr)
        # loop musical gerado na primeira vez que ligar
        self._ambient_buf = None

    # ===== Música de fundo =====
    def _mk_hero_loop(self, bpm=120, bars=4):
        """Gera um loop de ~8s: kick+snare+hat, baixo e arpejo."""
        sr = self.e.samplerate
        beats_per_bar = 4
        total_beats = beats_per_bar * bars
        spb = 60.0 / float(bpm)          # seconds per beat
        total_sec = total_beats * spb
        n = int(total_sec * sr)
        out = np.zeros(n, dtype=np.float32)

        def place(buf, t_sec, gain=1.0):
            i = int(t_sec * sr)
            if i >= n: return
            L = min(len(buf), n - i)
            out[i:i+L] += buf[:L] * float(gain)

        # --- Percussão ---
        k = kick_click(sr, 1.0)
        sn = slap(sr) * 0.9
        # hi-hat: white noise curtinho + envelope
        def hat():
            dur = 0.045
            base = noise_white(dur, sr, amp=0.35)
            env = env_exp(len(base), sr, dur*0.35)
            return (base * env * 0.8).astype(np.float32)

        # Kicks nos tempos 1 e 3, snare nos 2 e 4
        for beat in range(total_beats):
            t = beat * spb
            if beat % 4 in (0, 2): place(k, t, 0.90)  # 1,3
            else:                   place(sn, t, 0.85) # 2,4
        # hats em colcheias (8ths)
        for half in range(total_beats * 2):
            t = half * (spb/2.0)
            place(hat(), t, 0.45)

        # --- Baixo (A-C-D-E padrão) em semínimas ---
        bass_notes = [110.0, 130.81, 146.83, 164.81]  # A2, C3, D3, E3
        for beat in range(total_beats):
            f = bass_notes[(beat // 4) % len(bass_notes)]
            dur = spb * 0.92
            x = sine(f, dur, sr) * 0.35
            x *= env_exp(len(x), sr, dur*0.85)
            place(x, beat*spb, 0.65)

        # --- Arpejinho leve no topo ---
        lead_scale = [659.26, 880.0, 739.99, 987.77]  # E5, A5, F#5, B5
        for bar in range(bars):
            base_t = bar * beats_per_bar * spb
            for step in (0.5, 1.5, 2.5, 3.0):
                f = lead_scale[(bar + int(step*2)) % len(lead_scale)]
                dur = spb * 0.30
                x = sine(f, dur, sr) * 0.22
                x += sine(f*2, dur, sr) * 0.10
                x = lowpass_mavg(x, k=max(3, int(sr/1200)))
                x *= env_exp(len(x), sr, dur*0.7)
                place(x, base_t + step*spb, 0.75)

        # leve compressão/clamp
        np.clip(out, -1.0, 1.0, out)
        return out

    def start_ambient(self, vol=0.25):
        if self._silent: 
            return
        if self._ambient_buf is None:
            self._ambient_buf = self._mk_hero_loop(bpm=120, bars=4)
        self.e.start_ambient(self._ambient_buf, vol=float(vol))

    def stop_ambient(self):
        if self._silent: 
            return
        self.e.stop_ambient()

    # ===== API antiga (compat) =====
    def note_hit(self):   self.e.play(self.buf_hit,    0.9)
    def note_miss(self):  self.e.play(self.buf_miss,   0.9)
    def streak(self):     self.e.play(self.buf_streak, 1.0)
    def fail(self):       self.e.play(self.buf_fail,   1.0)

    # ===== API usada pela tela =====
    def hit(self, quality: str = "good"):
        q = (quality or "").lower()
        if q == "perfect":
            self.e.play(self.buf_hit, 1.0)
        elif q in ("good", "late"):
            self.e.play(self.buf_hit, 0.8)
        else:
            self.e.play(self.buf_hit_soft, 0.6)

    def wrong(self): self.note_miss()
    def miss(self):  self.note_miss()

    def combo_up(self, combo: int = 0):
        if combo and combo % 5 == 0:
            self.streak()
        else:
            self.e.play(self.buf_hit, 0.6)

    def finish(self, passed: bool, score: int = 0):
        if passed:
            self.streak()
        else:
            self.fail()

    def wave_start(self, prompt: str = ""):
        # ping leve a cada pergunta
        self.e.play(self.buf_hit, 0.5)

    def wave_end(self, *a, **k): pass
    def spawn_note(self, *a, **k): pass
