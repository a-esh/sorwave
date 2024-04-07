import os 
import re
from metadata_extractor import get_metadata


def sort_path(folder_path):
    songs = os.listdir(folder_path)
    for song in songs:
        if song.endswith(".flac"):
            file_path = os.path.join(folder_path, song)
            metadata = get_metadata(file_path)
            new_folder_path_art = os.path.join(folder_path, re.findall(r"^\w+\s?\w*", metadata["artist"])[0])
            new_folder_path_album = os.path.join(new_folder_path_art, metadata["album"])
            if not os.path.exists(new_folder_path_art):
                os.mkdir(new_folder_path_art)
            else:
                if not os.path.exists(new_folder_path_album):
                    os.mkdir(new_folder_path_album)
                else:
                    os.rename(file_path, os.path.join(new_folder_path_album, song))
                        