import numpy as np
import matplotlib.pyplot as plt

fs = 1000
duration = 1.0
n_samples = int(fs*duration)
t = np.linspace(0, duration, n_samples ,endpoint= False)

freq1, freq2 = 50, 200

signal = (np.sin(freq1*t*np.pi) + 0.5*np.sin(freq2*t*np.pi))

spectrum = np.fft.fft(signal)
freqs = np.fft.fftfreq(n_samples, d=1/fs)

half_n = n_samples // 2
freq_pos = freqs[:half_n]
magnitude = 2*np.abs(spectrum[:half_n])/n_samples

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(9,6))

ax1.plot(t[:200], signal[:200])
ax1.set_title("Time domain (first 0.2s)")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Amplitude")

plt.tight_layout()
plt.show()