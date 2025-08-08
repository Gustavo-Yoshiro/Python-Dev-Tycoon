import numpy as np
import sounddevice as sd

def jingle_parabens():
    fs = 44100
    notas = [
        (523, 0.18),  # C
        (587, 0.14),  # D
        (659, 0.14),  # E
        (698, 0.13),  # F
        (784, 0.2),   # G
        (880, 0.16),  # A
        (1046, 0.25), # C (alto, fim)
    ]
    ondas = []
    for freq, dur in notas:
        t = np.linspace(0, dur, int(fs*dur), False)
        env = np.exp(-2 * t)
        onda = 0.48 * np.sin(2 * np.pi * freq * t) * env
        # Harmônico suave para brilho
        onda += 0.09 * np.sin(2 * np.pi * freq * 2 * t) * env
        ondas.append(onda)
        ondas.append(np.zeros(int(fs*0.011)))
    som = np.concatenate(ondas)
    sd.play(som, fs)
    sd.wait()

def erro_fail():
    fs = 44100
    t = np.linspace(0, 0.7, int(fs*0.7), False)
    # Tom descendo (de 700 pra 180 Hz)
    freq = np.linspace(700, 180, t.shape[0])
    env = np.exp(-2.2 * t)
    onda = 0.5 * np.sin(2 * np.pi * freq * t) * env
    # Um pequeno “blip” para reforçar o fail
    blip_t = np.linspace(0, 0.11, int(fs*0.11), False)
    blip = 0.3 * np.sin(2*np.pi*160*blip_t) * np.exp(-12*blip_t)
    som = np.concatenate([onda, blip])
    sd.play(som, fs)
    sd.wait()

erro_fail()
jingle_parabens()
