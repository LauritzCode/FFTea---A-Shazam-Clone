import os
import subprocess

from fingerprinting import spectrogram, extract_constellation, hashing
from detection import identify_recording

temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_recs")
os.makedirs(temp_dir, exist_ok=True)

EXTENSION_BY_MIMETYPE = {
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/mp4": "mp4",
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
}


def _save_upload_as_wav(uploaded_file):
    extension = EXTENSION_BY_MIMETYPE.get(uploaded_file.mimetype, "webm")
    raw_path = os.path.join(temp_dir, f"chunk_raw.{extension}")
    wav_path = os.path.join(temp_dir, "chunk.wav")

    uploaded_file.save(raw_path)

    # ffmpeg decodes whatever the browser recorded (usually webm/opus),
    # and -ac 2 forces stereo output even if the source is mono, since
    # the rest of the pipeline expects two channels to average down itself
    subprocess.run(
        ["ffmpeg", "-y", "-i", raw_path, "-ac", "2", "-ar", "44100", wav_path],
        check=True,
        capture_output=True,
    )

    os.remove(raw_path)
    return wav_path


def process_chunk(uploaded_file, elapsed, tally):
    wav_path = _save_upload_as_wav(uploaded_file)

    song_frequency, freq_axis, timestamps = spectrogram(wav_path)
    constellation = extract_constellation(song_frequency, freq_axis, timestamps)
    hashes = hashing(constellation)

    shifted_hashes = [(hash_value, timestamp + elapsed) for hash_value, timestamp in hashes]
    identify_recording(shifted_hashes, tally)

    os.remove(wav_path)
