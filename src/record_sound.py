import sounddevice as sd
from scipy.io import wavfile

def record_audio(duration, path):
    fs = 48000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wavfile.write(path, fs, recording)
    return path


