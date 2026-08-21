from database import hash_match, title_extract

def identify_recording(hashes, tally):
    for hash_value, query_timestamp in hashes:
        matches = hash_match(hash_value)
        for db_song_id, db_timestamp in matches:
            offset = db_timestamp - query_timestamp
            tally.append((db_song_id, offset))












