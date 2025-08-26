# Intermediario/Utils/sfx_cobra.py
from __future__ import annotations
from .audio_core import AudioEngine, blip, pop, thud, chime

class SFXCobra:
    """Usar em Cobra Código: move/eat/crash/bonus."""
    def __init__(self, engine: AudioEngine):
        self.e = engine
        sr = self.e.samplerate
        self.buf_move  = blip(sr, 700, 0.03)      # movimento discreto
        self.buf_eat   = pop(sr, 0.08)            # come maçã
        self.buf_crash = thud(sr)                 # bateu
        self.buf_bonus = chime(sr, 0.25)

    def start_ambient(self, vol=0.0): pass
    def stop_ambient(self): pass

    def move_tick(self): self.e.play(self.buf_move, 0.4)
    def eat(self):       self.e.play(self.buf_eat,  0.9)
    def crash(self):     self.e.play(self.buf_crash,1.0)
    def bonus(self):     self.e.play(self.buf_bonus,0.9)
