# practice and tests of chopping the audio data into smaller pieces, and 
# applying windowing functions (hanning) before applying the FFT to each. 
# We are trying to avoid spectral leakage with the windowing functions. 


from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

frame_size = 2048

path = "music/song_1.wav"

sample_rate, data = wavfile.read(path)

# t = np.linspace(0,1,sample_rate,endpoint=False)

mono = np.mean(data, axis=1)
mono_1 = signal.decimate(mono, 4)

song_freq_1 = []
song_timestamps_1 = []
freq_axis = np.fft.fftfreq(frame_size, d=1/(sample_rate/4)) # remember only first half kept


for i in range(0, len(mono_1), frame_size):
    chunk = mono_1[i : i+frame_size]
    N = frame_size
    window = np.hamming(N)
    if len(chunk) < N: 
        continue
    chunk_fft = np.fft.fft(chunk * window)
    magnitude = abs(2*chunk_fft[:N//2]/N)
    song_freq_1.append(magnitude)
    song_timestamps_1.append((i)/(sample_rate/4))


song_1_frequency = np.array(song_freq_1)
freq_axis = freq_axis[:N//2]
song_1_db = 20*np.log10(song_1_frequency)

plt.pcolormesh(song_timestamps_1, freq_axis, song_1_db.T, vmin=-60, vmax=80)

plt.show()