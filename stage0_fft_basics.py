"""
Stage 0: FFT on a synthetic signal — no audio files yet.

Goal: build a signal where we KNOW the answer in advance (we chose the
frequencies ourselves), run it through np.fft.fft, and confirm the FFT
finds exactly the frequencies we put in. This is the sanity check you
want in place before trusting any FFT on real audio.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Build a synthetic signal -------------------------------------------

fs = 1000          # sample rate in Hz (samples per second) — we're choosing this,
                    # for real audio this comes from the file itself
duration = 1.0      # seconds
n_samples = int(fs * duration)

# np.linspace(start, stop, num, endpoint=False) gives us n_samples evenly
# spaced time points from 0 up to (but not including) `duration`.
# endpoint=False matters: with it True you'd get n_samples points spanning
# 0..duration INCLUSIVE, which subtly shifts your sample spacing.
t = np.linspace(0, duration, n_samples, endpoint=False)

freq1, freq2 = 50, 120   # Hz — two tones we're mixing together
signal = (
    1.0 * np.sin(2 * np.pi * freq1 * t) +
    0.5 * np.sin(2 * np.pi * freq2 * t)
)

# --- 2. FFT ------------------------------------------------------------

spectrum = np.fft.fft(signal)          # complex array, length n_samples
freqs = np.fft.fftfreq(n_samples, d=1 / fs)  # the frequency (Hz) each bin corresponds to

# spectrum is symmetric for a real-valued input signal (negative frequencies
# mirror the positive ones), so we only care about the first half.
half = n_samples // 2
freqs_pos = freqs[:half]
magnitude = np.abs(spectrum[:half]) / n_samples * 2   # normalize so amplitude reads correctly


# --- 3. Plot -----------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))

ax1.plot(t[:200], signal[:200])   # just the first 200 samples, full second is too dense to see
ax1.set_title("Time domain (first 0.2s)")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Amplitude")

ax2.plot(freqs_pos, magnitude)
ax2.set_title("Frequency domain (FFT)")
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Magnitude")
ax2.set_xlim(0, 200)

plt.tight_layout()
plt.show()
