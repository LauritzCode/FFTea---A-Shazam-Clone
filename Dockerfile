FROM python:3.13-slim

# ffmpeg is a system package, not a pip package, needed to decode whatever
# format the browser's MediaRecorder sends (usually webm/opus)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY src/ src/
COPY frontend/ frontend/
COPY fingerprints.db .

# --workers 1 matters here, not just a default choice: the "currently
# listening" state lives in a plain in-memory dict in app.py, shared across
# requests within one worker process. More than one worker would mean each
# has its own separate copy, silently breaking the chunk-by-chunk accumulation.
CMD ["sh", "-c", "gunicorn --workers 1 --bind 0.0.0.0:${PORT:-8000} app:app"]
