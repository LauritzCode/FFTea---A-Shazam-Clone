"""
Reference spectrogram using librosa, to compare against the from-scratch
pipeline in stage_2_windowing.py. Settings matched as closely as possible:
same sample rate (11025 Hz), same frame size (2048), same hop (2048, no
overlap), same window (hamming).
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt

path = "music/song_1.wav"
frame_size = 2048

y, sr = librosa.load(path, sr=11025, mono=True)

stft = librosa.stft(y, n_fft=frame_size, hop_length=frame_size, window="hamming")
magnitude = abs(stft)
db = librosa.amplitude_to_db(magnitude, ref=1.0)

plt.figure(figsize=(16, 9))
librosa.display.specshow(db, sr=sr, hop_length=frame_size, x_axis="time", y_axis="hz")
plt.colorbar(format="%+2.0f dB")
plt.title("librosa reference spectrogram")
plt.tight_layout()
plt.show()
