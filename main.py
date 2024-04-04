from mutagen.flac import FLAC
import os 
import re
import json
def extract_flac_metadata(file_path):
    try:
        audio = FLAC(file_path)
        metadata = {}
        
        # Obtener los metadatos del archivo FLAC
        for key, value in audio.items():
            metadata[key] = value[0]

        return metadata
    
    except Exception as e:
        print("Error al extraer los metadatos:", e)
        return None

def sort_by_album_art(folder_path):
    songs = os.listdir(folder_path)
    for song in songs:
        if song.endswith(".flac"):
            file_path = os.path.join(folder_path, song)
            metadata = extract_flac_metadata(file_path)
            new_folder_path_art = os.path.join(folder_path, re.findall(r"^\w+\s?\w*", metadata["artist"])[0])
            new_folder_path_album = os.path.join(new_folder_path_art, metadata["album"])
            if not os.path.exists(new_folder_path_art):
                os.mkdir(new_folder_path_art)
            else:
                if not os.path.exists(new_folder_path_album):
                    os.mkdir(new_folder_path_album)
                else:
                    os.rename(file_path, os.path.join(new_folder_path_album, song))
                        

def log_folders(folder_path):
    log_path = os.path.join(folder_path, "music_log.json")

    if os.path.exists(log_path):
        os.remove(log_path)

    folder_log = {}
    artists_folders = os.listdir(folder_path)

    for artist_folder in artists_folders:
        artist_folder_path = os.path.join(folder_path, artist_folder)
        albums = os.listdir(artist_folder_path)
        albums_dict = {}

        for album in albums:
            songs = os.listdir(os.path.join(artist_folder_path, album))
            albums_dict[album] = songs
        folder_log[artist_folder] = albums_dict

    with open(log_path, "w") as json_file:
        json.dump(folder_log, json_file, indent=4)

    os.system(f'attrib +h "{log_path}"')
    return folder_log

def merge_folders(main_folder_path, source_folder_path):
    main_log = log_folders(main_folder_path)
    source_log = log_folders(source_folder_path)
    
main_folder_path = r"D:\Equipo\Documentos\Base de Datos\Trabajo\Proyectos Secundarios\2024 Music_Sorter\test\Music_Destination"
source_folder_path = r"D:\Equipo\Documentos\Base de Datos\Trabajo\Proyectos Secundarios\2024 Music_Sorter\test\Music_Origin"
sort_by_album_art(main_folder_path)

# sort_by_album_art(folder_path, songs)