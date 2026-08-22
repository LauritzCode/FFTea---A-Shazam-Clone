import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from flask import Flask, jsonify, request, send_from_directory
from live_chunk import process_chunk
from database import title_extract

app = Flask(__name__, static_folder="frontend", static_url_path="")

CHUNK_SECONDS = 3
MATCH_THRESHOLD = 4

# only ever one visitor identifies a song at a time, so a single shared
# in-memory state is enough, no per-session bookkeeping needed
listening_state = {"tally": [], "elapsed": 0}


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/identify-start", methods=["POST"])
def identify_start():
    listening_state["tally"] = []
    listening_state["elapsed"] = 0
    return jsonify({"ok": True})


@app.route("/api/identify-chunk", methods=["POST"])
def identify_chunk():
    uploaded_file = request.files["audio"]
    tally = listening_state["tally"]
    elapsed = listening_state["elapsed"]

    process_chunk(uploaded_file, elapsed, tally)
    listening_state["elapsed"] = elapsed + CHUNK_SECONDS

    if len(tally) > 0:
        best_match, best_count = Counter(tally).most_common(1)[0]
        if best_count > MATCH_THRESHOLD:
            song_id = best_match[0]
            title = title_extract(song_id)
            listening_state["tally"] = []
            listening_state["elapsed"] = 0
            return jsonify({"found": True, "title": title})

    return jsonify({"found": False})


if __name__ == "__main__":
    app.run(debug=True)
