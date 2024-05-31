import os
import json
import datetime
from metadata_manager import get_metadata

def filter_artist(artist):
    name_exceptions = ["Zion & Lennox","AC/DC", "Flamman & Abraxas"]

    for exception in name_exceptions:
        if exception in artist:
            return exception

    dividers = [",", "/", "Ft.", "feat.", "Feat", "&"]
    for fix in dividers:
        artist = artist.split(fix)[0].strip()
    return artist

def new_log(folder_path, log_dict, log_type):
    # Path to the log file

    log_path = os.path.join(folder_path, "{}.json".format(log_type))
    
    # Log information including the current date and time
    log_info = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": log_type,
        "data": log_dict
    }

    # Write logs to JSON file if log generation is enabled
    
    if os.path.exists(log_path):
        os.remove(log_path)
    
    with open(log_path, 'w', encoding='utf-8') as json_file:
        json.dump(log_info, json_file, ensure_ascii=False, indent=4)
        json_file.write('\n')  # Add a blank line between dictionaries

    # Hide the log file by setting it as a hidden file
        os.system(f'attrib +h "{log_path}"')

def gen_log(folder_path, gen_log=True):
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
                        "albumartist" : song_metadata.get("albumartist"),
                        "title": song_metadata["title"],
                        "tracknumber": (str((song_metadata["tracknumber"])).split("/"))[0],
                        "genre": song_metadata.get("genre"),
                        "path": file_path,
                        "extension": (os.path.splitext(file_path))[1]
                    })
    if gen_log:
        new_log(folder_path, song_log, "songs_log")
    if bugs_log:
        new_log(folder_path, bugs_log, "metadataBugs_log")

    return song_log
