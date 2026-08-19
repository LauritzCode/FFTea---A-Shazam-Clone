
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

path = "music/song_1.wav"

sample_rate, data = wavfile.read(path)

t = np.linspace(0,1,sample_rate,endpoint=False)

# fig, (ax1,ax2) = plt.subplots(2,1, figsize=(9,6))

# ax1.plot(t, data[:sample_rate,0])
# ax2.plot(t, data[:sample_rate,1])


# plt.tight_layout()
# plt.show()

mono = np.mean(data, axis=1)



mono_1 = signal.decimate(mono, 4)

print(len(mono_1))
print(len(mono_1) / (sample_rate/4))

fig, ax3 = plt.subplots(1,1, figsize = (9,6))

ax3.plot(t, mono_1[:sample_rate])
plt.tight_layout()
plt.show()