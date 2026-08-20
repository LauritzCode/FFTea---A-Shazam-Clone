from scipy.io import wavfile
from scipy import signal
import numpy as np

def spectrogram(path):
    frame_size = 2048
    path_song = path

    sample_rate, data = wavfile.read(path_song)

    mono_set = np.mean(data, axis=1)
    mono = signal.decimate(mono_set, 4)

    song_freq_1 = []
    song_timestamps = []
    freq_axis = np.fft.fftfreq(frame_size, d=1/(sample_rate/4))

    for i in range(0, len(mono), frame_size):
        chunk = mono[i : i+frame_size]
        N = frame_size
        window = np.hamming(N)
        if len(chunk) < N: 
            continue
        chunk_fft = np.fft.fft(chunk * window)
        magnitude = abs(2*chunk_fft[:N//2]/N)
        song_freq_1.append(magnitude)
        song_timestamps.append((i)/(sample_rate/4))

    song_frequency = np.array(song_freq_1)
    freq_axis = freq_axis[:N//2]

    return song_frequency, freq_axis, song_timestamps


def extract_constellation(song_frequency, freq_axis, timestamps):
    constellation = []

    bands = np.geomspace(10, 44100//8 ,num=7)

    for i in range(len(song_frequency)):
        frame_peaks = []
        for b in range(len(bands)-1):
            best_freq = 0
            best_band = 0
            low = bands[b]
            high = bands[b+1]
            for j in range(len(freq_axis)):
                if(low <= freq_axis[j] and freq_axis[j] < high):
                    if(song_frequency[i,j] > best_band):
                        best_band = song_frequency[i,j]
                        best_freq = j
            frame_peaks.append((best_freq, best_band))
        avg = np.average(np.array(frame_peaks)[:,1])
        for a in range(len(frame_peaks)):
            if(frame_peaks[a][1] > avg):
                constellation.append((frame_peaks[a][0], frame_peaks[a][1], timestamps[i]))

    return constellation


def hashing(constellation):
    hashes = []

    for i in range(len(constellation)):
        bin_index, mag, timestamp = constellation[i]
        hash_entry = []
        for j in range(i + 1, len(constellation)):
            if (constellation[j][2] - timestamp) < 5 and len(hash_entry) < 5:
                hash_entry.append((constellation[j][0], constellation[j][1], constellation[j][2]))
            else:
                break

        for target in hash_entry:
            target_bin = target[0]
            target_timestamp = target[2]
            delta_scaled = round((target_timestamp - timestamp) * 100)
            hash_value = (bin_index << 22) | (target_bin << 12) | delta_scaled
            hashes.append((hash_value, timestamp))

    return hashes
