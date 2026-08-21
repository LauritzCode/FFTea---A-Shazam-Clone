from database import add_song
from fingerprinting import spectrogram, extract_constellation, hashing
from record_sound import record_audio
import os

def import_song(path):
    filename = os.path.basename(path)
    title = os.path.splitext(filename)[0]

    song_frequency, freq_axis, timestamps = spectrogram(path)
    constellation = extract_constellation(song_frequency, freq_axis, timestamps)
    hashes = hashing(constellation)
    add_song(hashes, title)


def import_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            full_path = os.path.join(folder_path, filename)
            import_song(full_path)


def process_recording(path,duration):
    record_audio(duration, path)
    song_frequency, freq_axis, timestamps = spectrogram(path)
    constellation = extract_constellation(song_frequency, freq_axis, timestamps)
    hashes = hashing(constellation)
    os.remove(path)
    return hashes


