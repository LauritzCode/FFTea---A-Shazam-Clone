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


def add_song(hashes, title):
    cur.execute("SELECT COUNT(DISTINCT song_id) FROM fingerprints")
    existing_count = cur.fetchone()[0]
    song_id = f"{existing_count + 1:04d}"

    cur.execute("INSERT INTO songs (song_id, title) VALUES (?, ?)", (song_id, title))

    for hash_value, timestamp in hashes:
        cur.execute("INSERT INTO fingerprints (hash, song_id, timestamp) VALUES (?, ?, ?)", (hash_value, song_id, timestamp))

    con.commit()

