import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fingerprints.db")

con = sqlite3.connect(db_path)
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


def add_song(hashes, title):
    cur.execute("SELECT COUNT(DISTINCT song_id) FROM fingerprints")
    existing_count = cur.fetchone()[0]
    song_id = f"{existing_count + 1:04d}"

    cur.execute("INSERT INTO songs (song_id, title) VALUES (?, ?)", (song_id, title))

    for hash_value, timestamp in hashes:
        cur.execute("INSERT INTO fingerprints (hash, song_id, timestamp) VALUES (?, ?, ?)", (hash_value, song_id, timestamp))

    con.commit()


def list_titles():
    cur.execute("SELECT song_id, title FROM songs")
    return cur.fetchall()

def hash_match(hash_value):
    cur.execute("SELECT song_id, timestamp FROM fingerprints WHERE hash = ?", (hash_value,))
    return cur.fetchall()


def title_extract(song_id):
    cur.execute("SELECT title FROM songs WHERE song_id = ?", (song_id,))
    return cur.fetchone()[0]

