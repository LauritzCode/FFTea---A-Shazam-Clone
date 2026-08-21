from database import add_song
from fingerprinting import spectrogram, extract_constellation, hashing
from record_sound import record_audio
import os

def import_song(title, path):
    song_frequency, freq_axis, timestamps = spectrogram(path)
    constellation = extract_constellation(song_frequency, freq_axis, timestamps)
    hashes = hashing(constellation)
    add_song(hashes, title)


def process_recording(path,duration):
    record_audio(duration, path)
    song_frequency, freq_axis, timestamps = spectrogram(path)
    constellation = extract_constellation(song_frequency, freq_axis, timestamps)
    hashes = hashing(constellation)
    os.remove(path)
    return hashes[:10]


