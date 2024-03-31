from mutagen.flac import FLAC
import os 
import re
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

def sort_by_album_art(folder_path, songs):
    for song in songs:
        if song.endswith(".flac"):
            file_path = folder_path + "\\" + song
            metadata = extract_flac_metadata(file_path)
            new_folder_path_art = folder_path + "\\" + re.findall(r"^\w+\s?\w*", metadata["artist"])[0]
            new_folder_path_album = new_folder_path_art + "\\" + metadata["album"]
            if not os.path.exists(new_folder_path_art):
                os.mkdir(new_folder_path_art)
            else:
                if not os.path.exists(new_folder_path_album):
                    os.mkdir(new_folder_path_album)
                else:
                        try:
                            os.rename(file_path, new_folder_path_album + "\\" + song )
                        except PermissionError:
                            print("El archivo " + song + " se esta usando por otra aplicación")
                            print(song + " : \n" + folder_path + "- > " + new_folder_path_album)

def move_songs(folder_path, new_folder_path):
    try:
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        
        for item in os.listdir(folder_path):
            source_item = os.path.join(folder_path, item)
            destination_item = os.path.join(new_folder_path, item)
            os.rename(source_item, destination_item)
        
        os.rmdir(folder_path)
        
        print("La carpeta se ha movido correctamente.")
    except Exception as e:
        print("Error al mover la carpeta:", e)


new_folder_path = r"D:\Equipo\Musica"
folder_path = r"D:\Equipo\Download\Telegram Desktop"
songs = os.listdir(folder_path)

sort_by_album_art(folder_path, songs)