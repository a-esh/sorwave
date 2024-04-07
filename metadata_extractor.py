from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import os

file_extensions = [".flac", ".mp3"]
def extract_metadata(file_path):
    file_type = (os.path.splitext(file_path)).lstrip('.')
    try:
        audio = file_type(file_path)
        metadata = {}
        
        # Obtener los metadatos del archivo FLAC
        for key, value in audio.items():
            metadata[key] = value[0]

        return metadata
    except Exception as e:
        print("Error al extraer los metadatos:", e)
        return None