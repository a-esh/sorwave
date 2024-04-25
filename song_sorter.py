import os 
import re
from metadata_extractor import get_metadata
from music_logger import generate_log

def sintaxis_filter(path):
    invalid_characters = '*?"<>|'  
    filtering_path = ''.join(caracter for caracter in path if caracter not in invalid_characters)
    return filtering_path


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
                    
def sort_songs(folder_path):
    music_library = generate_log(folder_path, generate_log=False)
    
    for fixed_artist, albums in music_library.items():
        artist_path = os.path.join(folder_path, fixed_artist)
        for album, songs in albums.items():
            album_path = os.path.join(artist_path, album)
            for song in songs:
                song_path = sintaxis_filter(os.path.join(album_path, ("{}. {}{}".format(song["tracknumber"], song["title"], song["extension"]))))
                if not os.path.exists(album_path):
                    os.makedirs(album_path)
                    os.rename(song["path"], song_path)
                elif not os.path.exists(song_path):
                    os.rename(song["path"], song_path)
    