#


from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

con = sqlite3.connect("fingerprints.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS fingerprints (
        hash INTEGER,
        song_id TEXT,
        timestamp REAL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id TEXT,
        title TEXT
    )
""")

con.commit()


frame_size = 2048

path = "music/song_1.wav"

sample_rate, data = wavfile.read(path)

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

constellation = []
bands = np.geomspace(10, 44100//8 ,num=7)


for i in range(len(song_1_frequency)):
    frame_peaks = []
    for b in range(len(bands)-1):
        best_freq = 0
        best_band = 0
        low = bands[b]
        high = bands[b+1]
        for j in range(len(freq_axis)):
            if(low <= freq_axis[j] and freq_axis[j] < high):
                if(song_1_frequency[i,j] > best_band):
                    best_band = song_1_frequency[i,j]
                    best_freq = j
        frame_peaks.append((best_freq, best_band))
    avg = np.average(np.array(frame_peaks)[:,1])
    for a in range(len(frame_peaks)):
        if(frame_peaks[a][1] > avg):
            constellation.append((frame_peaks[a][0], frame_peaks[a][1], song_timestamps_1[i]))

cur.execute("SELECT COUNT(DISTINCT song_id) FROM fingerprints")
existing_count = cur.fetchone()[0]
song_id = f"{existing_count + 1:04d}"

cur.execute("INSERT INTO songs (song_id, title) VALUES (?, ?)", (song_id, path))
con.commit()

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

        cur.execute("INSERT INTO fingerprints (hash, song_id, timestamp) VALUES (?, ?, ?)", (hash_value, song_id, timestamp))
    con.commit()



