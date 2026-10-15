import wave, math, struct, base64, json

def create_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for s in samples:
            val = max(-32767, min(32767, int(s * 32767)))
            wav.writeframesraw(struct.pack('<h', val))

def synth_key_click(sr=44100):
    duration = 0.04
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 120)
        # Mix transient click + mechanical resonance
        s = 0.6 * math.sin(2 * math.pi * 1800 * t) * math.exp(-t * 300)
        s += 0.4 * math.sin(2 * math.pi * 750 * t) * env
        samples.append(s)
    return samples

def synth_backspace(sr=44100):
    duration = 0.05
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 90)
        s = 0.7 * math.sin(2 * math.pi * 320 * t) * env
        s += 0.3 * math.sin(2 * math.pi * 160 * t) * env
        samples.append(s)
    return samples

def synth_correct(sr=44100):
    duration = 0.28
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 12)
        # Crystal chime: fundamental 880Hz + octave harmonic 1760Hz
        s = 0.7 * math.sin(2 * math.pi * 880 * t) * env
        s += 0.3 * math.sin(2 * math.pi * 1760 * t) * math.exp(-t * 20)
        samples.append(s)
    return samples

def synth_present(sr=44100):
    duration = 0.22
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 14)
        # Warm chime: 554Hz (C#5)
        s = 0.75 * math.sin(2 * math.pi * 554.37 * t) * env
        s += 0.25 * math.sin(2 * math.pi * 1108.73 * t) * math.exp(-t * 25)
        samples.append(s)
    return samples

def synth_absent(sr=44100):
    duration = 0.12
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 35)
        s = 0.8 * math.sin(2 * math.pi * 260 * t) * env
        samples.append(s)
    return samples

def synth_buzz(sr=44100):
    duration = 0.18
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 10)
        # Dual retro saw tone
        s = 0.5 * (2 * (t * 130 - math.floor(0.5 + t * 130))) * env
        s += 0.5 * (2 * (t * 165 - math.floor(0.5 + t * 165))) * env
        samples.append(s)
    return samples

def synth_win(sr=44100):
    duration = 0.65
    n = int(sr * duration)
    samples = [0.0] * n
    notes = [(0.0, 523.25), (0.09, 659.25), (0.18, 783.99), (0.27, 987.77), (0.36, 1046.50)]
    for start_t, freq in notes:
        start_idx = int(start_t * sr)
        note_n = int(0.26 * sr)
        for i in range(note_n):
            if start_idx + i < n:
                t = i / sr
                env = math.exp(-t * 10)
                samples[start_idx + i] += 0.25 * math.sin(2 * math.pi * freq * t) * env
    return samples

def synth_pop(sr=44100):
    duration = 0.08
    n = int(sr * duration)
    samples = []
    for i in range(n):
        t = i / sr
        env = math.exp(-t * 40)
        freq = 800 + 400 * (1 - t / duration)
        samples.append(0.7 * math.sin(2 * math.pi * freq * t) * env)
    return samples

sounds = {
    'key': synth_key_click(),
    'backspace': synth_backspace(),
    'correct': synth_correct(),
    'present': synth_present(),
    'absent': synth_absent(),
    'buzz': synth_buzz(),
    'win': synth_win(),
    'pop': synth_pop()
}

base64_sounds = {}
for name, smp in sounds.items():
    fname = f"sound_{name}.wav"
    create_wav(fname, smp)
    with open(fname, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        base64_sounds[name] = f"data:audio/wav;base64,{b64}"

with open('sounds.js', 'w', encoding='utf-8') as f:
    f.write('// Audio Assets for Howler.js\nwindow.HOWLER_AUDIO_DATA = ' + json.dumps(base64_sounds, indent=2) + ';\n')

print("All sounds generated and written to sounds.js!")
