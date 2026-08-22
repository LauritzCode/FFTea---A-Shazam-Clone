import os
from collections import Counter
from detection import identify_recording
from add_song import process_recording
from database import title_extract

def live_identify_recording():
    tally = []
    elapsed = 0
    src_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(src_dir, "temp_recs", "rec.wav")

    while True:
        print("searching...")

        hashes = process_recording(path, 3)
        new_hashes = []
        for hash, timestamp in hashes:
            new_hashes.append((hash, timestamp + 2*elapsed))

        identify_recording(new_hashes, tally)

        if len(tally) > 0:
            match = Counter(tally).most_common(1)[0][1]
            if match > 10:
                break

        elapsed = elapsed + 1

    return title_extract(Counter(tally).most_common(1)[0][0][0])

if __name__ == "__main__":
    title = live_identify_recording()
    print(title)
