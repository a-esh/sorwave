from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import os

file_extensions = {".flac": FLAC, ".mp3": MP3}

def extract_metadata(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()

    if file_extension in file_extensions:
        audio_class = file_extensions[file_extension]

        try:
            audio = audio_class(file_path)
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
