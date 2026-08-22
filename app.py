import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from flask import Flask, jsonify, send_from_directory
from live_detection import live_identify_recording

app = Flask(__name__, static_folder="frontend", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/identify", methods=["POST"])
def identify():
    title = live_identify_recording()
    return jsonify({"title": title})


if __name__ == "__main__":
    app.run(debug=True)
