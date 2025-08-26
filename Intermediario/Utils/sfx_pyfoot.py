# Intermediario/Utils/sfx_pyfoot.py
from __future__ import annotations
import numpy as np
from .audio_core import AudioEngine, kick_click, whoosh, thud, slap, crowd_loop, goal_cheer, save_groan

class SFXPyFoot:
    def __init__(self, engine: AudioEngine):
        self.e = engine
        sr = self.e.samplerate
        self.buf_crowd = crowd_loop(sr, seconds=4)
        kick = kick_click(sr, 1.0)
        wh   = whoosh(0.25, sr, 400, 2800)
        L = max(len(kick), len(wh))
        if len(kick) < L: kick = np.pad(kick, (0, L-len(kick)))
        if len(wh)   < L: wh   = np.pad(wh,   (0, L-len(wh)))
        self.buf_shot = (kick + wh).astype(np.float32)
        self.buf_pass = kick_click(sr, 0.7)
        self.buf_drib = whoosh(0.22, sr, 300, 2000)
        self.buf_thud = thud(sr)
        self.buf_slap = slap(sr)
        self.buf_goal = goal_cheer(sr)
        self.buf_save = save_groan(sr)

    # ambient
    def start_ambient(self, vol=0.2): self.e.start_ambient(self.buf_crowd, vol)
    def stop_ambient(self):            self.e.stop_ambient()

    # eventos
    def pass_kick(self): self.e.play(self.buf_pass, 0.9)
    def dribble(self):   self.e.play(self.buf_drib, 0.8)
    def tackle(self):    self.e.play(self.buf_thud, 1.0)
    def shot(self):      self.e.play(self.buf_shot, 1.0)
    def goal(self):      self.e.play(self.buf_goal, 1.0)
    def save(self):
        self.e.play(self.buf_slap, 1.0)
        self.e.play(self.buf_save, 1.0)
