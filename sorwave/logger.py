import os
import json
import datetime
from progress.bar import Bar
from .metadata_manager import get_metadata
from .musicbrainzngs_API import set_useragent


def filter_artist(artist):
    dividers = [",", "/", "Ft.", "feat.", "Feat", "&"]
    for fix in dividers:
        artist = artist.split(fix)[0].strip()
    return artist

def new_log_file(folder_path, log_dict, log_type, sorter_log):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    log_path = os.path.join(folder_path, f"{log_type} {date.replace(':', '-')}.json")
    log_info = {
        "date": date,
        "type": log_type,
        "data": log_dict,
    }
    if log_type == "sorter_log":
        log_info["sorter_log"] = sorter_log

    if os.path.exists(log_path):
        os.remove(log_path)
    with open(log_path, 'w', encoding='utf-8') as json_file:
        json.dump(log_info, json_file, ensure_ascii=False, indent=4)
        json_file.write('\n')

    # Hide the log file (Windows-specific)
    if os.name == 'nt':
        os.system(f'attrib +h "{log_path}"')

def gen_log(folder_path, use_api=False, gen_log=True):
    song_log = {}
    bugs_log = {}
    
    total_files = sum([len(files) for r, d, files in os.walk(folder_path) if any(f.endswith(('.flac', '.mp3')) for f in files)])
    bar = Bar('Processing', max=total_files)

    # Iterate through files and update the progress bar
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.flac') or file.endswith('.mp3'):
                bar.next()
                file_path = os.path.join(root, file)
                song_metadata = get_metadata(file_path, use_api,)
                if not song_metadata:
                    bugs_log["Metadata error"] = file_path
                else:
                    artist = song_metadata.get("albumartist")
                    if not artist:
                        artist = song_metadata.get("artist")
                    artist = filter_artist(artist)
                    album = song_metadata.get("album", song_metadata.get("title"))
                    album = album.replace("/", "-")
                    song_metadata["tracknumber"] = song_metadata.get("tracknumber", 1)

                    if artist not in song_log:
                        song_log[artist] = {}
                    if album not in song_log[artist]:
                        song_log[artist][album] = []
                    song_log[artist][album].append({
                        "artist": song_metadata.get("artist"),
                        "albumartist": song_metadata.get("albumartist"),
                        "title": song_metadata["title"],
                        "tracknumber": str(song_metadata["tracknumber"]).split("/")[0],
                        "genre": song_metadata.get("genre"),
                        "path": file_path,
                        "extension": os.path.splitext(file_path)[1],
                    })

    if gen_log:
        new_log_file(folder_path, song_log, "songs_log")
    if bugs_log:
        new_log_file(folder_path, bugs_log, "metadataBugs_log")

    return song_log