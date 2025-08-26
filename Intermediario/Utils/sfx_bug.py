# Intermediario/Utils/sfx_bug.py
from __future__ import annotations
from .audio_core import AudioEngine, blip, pop, buzz, chime, riser, noise_white, lowpass_mavg

class SFXBug:
    """Usar em BugSquashArcade: squash/miss/hint/combo/etc."""
    def __init__(self, engine: AudioEngine):
        self.e = engine
        sr = self.e.samplerate
        self.buf_spawn  = blip(sr, 900, 0.04)
        self.buf_squash = pop(sr, 0.09)
        self.buf_miss   = buzz(sr, 110, 0.25)
        self.buf_hint   = blip(sr, 1200, 0.05)
        self.buf_combo  = riser(sr, 0.35, 280, 1200)
        # stinger curtinho p/ fim de round
        tail = lowpass_mavg(noise_white(0.15, sr, 0.35), k=int(sr/400))
        self.buf_round_end = (chime(sr, 0.18)[:len(tail)] + tail*0.5)

    def start_ambient(self, vol=0.0): pass   # sem ambiente por padrão
    def stop_ambient(self): pass

    def spawn_bug(self):   self.e.play(self.buf_spawn, 0.8)
    def squash(self):      self.e.play(self.buf_squash, 1.0)
    def miss(self):        self.e.play(self.buf_miss,  0.9)
    def hint(self):        self.e.play(self.buf_hint,  0.7)
    def combo_up(self):    self.e.play(self.buf_combo, 1.0)
    def round_end(self):   self.e.play(self.buf_round_end, 0.9)
