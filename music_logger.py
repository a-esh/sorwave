import os
import json
from metadata_extractor import get_metadata

def generate_log(folder_path, generate_log=True):
    song_log = {}
    log_path = os.path.join(folder_path, "music_log.json")

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.flac') or file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                song_metadata = get_metadata(file_path)
                artist = song_metadata["artist"]
                album = song_metadata["album"]
                title = song_metadata["title"]
                if artist not in song_log:
                    song_log[artist] = {}
                if album not in song_log[artist]:
                    song_log[artist][album] = []
                song_log[artist][album].append({"title": title, "path": file_path})

    if generate_log == True:
        if os.path.exists(log_path):
            os.remove(log_path)
        with open(log_path, 'w', encoding='utf-8') as json_file:
            json.dump(song_log, json_file, ensure_ascii=False, indent=4)
        os.system(f'attrib +h "{log_path}"')

    return song_log