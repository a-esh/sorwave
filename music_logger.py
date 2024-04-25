import os
import json
import re
import datetime
from metadata_extractor import get_metadata

def filter_artist(artist):
    name_exceptions = ["Zion & Lennox","AC/DC", "Flamman & Abraxas"]

    for exception in name_exceptions:
        if exception in artist:
            return exception

    dividers = [",", "/", "Ft.", "feat.", "Feat", "&"]
    for fix in dividers:
        artist = artist.split(fix)[0].strip()

    return artist

def new_log(folder_path, song_log, bugs_log):
    # Path to the log file
    log_path = os.path.join(folder_path, "music_log.json")
    
    # Log information including the current date and time
    log_info = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bugs_log": bool(bugs_log)  # Indicate if there are any bugs logged
    }

    # Write logs to JSON file if log generation is enabled
    if generate_log:
        if os.path.exists(log_path):
            os.remove(log_path)
        with open(log_path, 'w', encoding='utf-8') as json_file:
            if log_info:
                json.dump(log_info, json_file, ensure_ascii=False, indent=4)
                json_file.write('\n')  # Add a blank line between dictionaries
            if bugs_log:
                json.dump(bugs_log, json_file, ensure_ascii=False, indent=4)
                json_file.write('\n')  # Add a blank line between dictionaries
            if song_log:
                json.dump(song_log, json_file, ensure_ascii=False, indent=4)
                json_file.write('\n')

        # Hide the log file by setting it as a hidden file
        os.system(f'attrib +h "{log_path}"')

def generate_log(folder_path, generate_log=True):
    # Dictionary to store song information
    song_log = {}
    # Dictionary to store bugs information
    bugs_log = {}

    # Walk through the folder path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a FLAC or MP3 file
            if file.endswith('.flac') or file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                song_metadata = get_metadata(file_path)
                # Check if metadata is available
                if len(song_metadata.keys()) == 0:
                    bugs_log["Metadata error"] = file_path
                else:
                    # Extract artist information
                    try:
                        artist = song_metadata["albumartist"]
                    except KeyError:
                        artist = song_metadata["artist"]
                    
                    artist = filter_artist(artist)

                    # Extract album information
                    try:
                        album = song_metadata["album"]
                    except KeyError:
                        album = song_metadata["title"]
                        song_metadata["tracknumber"] = 1

                    #Replace sidebars for visible routing problems
                    album = album.replace("/", "-")

                    # Update song log with song information
                    if artist not in song_log:
                        song_log[artist] = {}
                    if album not in song_log[artist]:
                        song_log[artist][album] = []
                    song_log[artist][album].append({
                        "artist": song_metadata.get("artist"),
                        "fixed_artist" : filter_artist(artist),
                        "albumartist" : song_metadata.get("albumartist"),
                        "title": song_metadata["title"],
                        "tracknumber": song_metadata["tracknumber"],
                        "genre": song_metadata.get("genre"),
                        "path": file_path,
                        "extension": (os.path.splitext(file_path))[1]
                    })

    new_log(folder_path, song_log, bugs_log)

    return song_log
