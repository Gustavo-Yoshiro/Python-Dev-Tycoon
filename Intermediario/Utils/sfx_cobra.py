# Intermediario/Utils/sfx_cobra.py
from __future__ import annotations
from .audio_core import AudioEngine, blip, pop, thud, chime
import random

class SFXCobra:
    """Usar em Cobra Código: move/eat/crash/bonus.
    Move agora é mais suave/baixo, com micro variação de pitch para não cansar.
    """
    def __init__(self, engine: AudioEngine):
        self.e = engine
        sr = self.e.samplerate

        # --- MOVE (suave): blips graves, curtos, com pequenas variações
        # faixas escolhidas p/ ficar "woop" discreto (não agudo)
        self._move_freqs = [300, 320, 340, 360, 380, 400]
        self._move_dur   = 0.040  # 40 ms (curto, porém audível)
        # pré-gera um pequeno banco de variantes
        self._move_bufs = [blip(sr, f, self._move_dur) for f in self._move_freqs]
        self._move_i = 0
        self._move_vol = 0.24     # menos volume que antes

        # --- DEMAIS SONS (mantidos)
        self.buf_eat   = pop(sr, 0.08)   # comer peça
        self.buf_crash = thud(sr)        # bater
        self.buf_bonus = chime(sr, 0.25) # bônus

    # (sem ambiente na cobrinha)
    def start_ambient(self, vol=0.0): pass
    def stop_ambient(self): pass

    def move_tick(self):
        """Toca um 'tick' suave, alternando levemente o pitch."""
        # escolhe próximo buffer e ocasionalmente um aleatório próximo
        if random.random() < 0.25:
            buf = random.choice(self._move_bufs)
        else:
            buf = self._move_bufs[self._move_i]
            self._move_i = (self._move_i + 1) % len(self._move_bufs)
        self.e.play(buf, self._move_vol)

    def eat(self):   self.e.play(self.buf_eat,   0.9)
    def crash(self): self.e.play(self.buf_crash, 1.0)
    def bonus(self): self.e.play(self.buf_bonus, 0.9)
