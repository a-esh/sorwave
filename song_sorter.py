import os 
import re
import datetime
from metadata_manager import get_metadata
from music_logger import generate_log
from music_logger import new_log

def sintaxis_filter(path):
    invalid_characters = '*?"<>|'  
    filtering_path = ''.join(caracter for caracter in path if caracter not in invalid_characters)
    return filtering_path

def sort_songs(folder_path):
    sorter_log = {}
    music_library = generate_log(folder_path, False)
    
    for fixed_artist, albums in music_library.items():
        artist_path = os.path.join(folder_path, fixed_artist)

        for album, songs in albums.items():
            album_path = os.path.join(artist_path, album)

            for song in songs:
                song_path = sintaxis_filter(os.path.join(album_path, ("{}. {}{}".format(song["tracknumber"], song["title"], song["extension"]))))

                if not song_path == song["path"]:

                    if not os.path.exists(album_path):
                        os.makedirs(album_path)
                        os.rename(song["path"], song_path)

                    elif not os.path.exists(song_path):
                        os.rename(song["path"], song_path)
                        sorter_log[song["title"]]= [song["path"], song_path]

                    else:
                        if "y" == input(print("La cancion {} esta duplicada, desea eliminarla? y/n".format(song["title"]))):
                            os.remove(song["path"])
                            
    new_log(r"logs\song_sorter.log", sorter_log, "sorter_log - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")))
    generate_log(folder_path)
    