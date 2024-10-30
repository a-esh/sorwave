from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.aac import ACC
import os

file_extensions = {".flac": FLAC, ".mp3": EasyID3}

def get_metadata(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()

    if file_extension in file_extensions:

        try:
            if file_extension in file_extensions:
                class_extension = file_extensions[file_extension]
                audio = class_extension(file_path)
                metadata = {}
                for key, value in audio.items():
                        metadata[key] = value[0]
                return metadata
        except Exception as e:
            print("Error al extraer los metadatos:", e)
            return None
    else:
        print("Extensión de archivo no compatible:", file_extension)
        return None