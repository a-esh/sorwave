import os
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3

file_extensions = {'.flac': FLAC, '.mp3': EasyID3}

def get_file_extension(file_path):
    return os.path.splitext(file_path)[-1].lower()

def get_metadata(file_path):
    """
    Extracts metadata from an audio file.
    Args:
        file_path (str): The path to the audio file.
    Returns:
        dict: A dictionary containing the extracted metadata, where keys are metadata fields and values are the corresponding metadata values.
    Raises:
        Exception: If there is an error extracting metadata, an exception is caught and an error message is printed.
    """

    file_path = os.path.abspath(file_path)
    try:
        ext = get_file_extension(file_path)
        if ext in file_extensions:
            audio = file_extensions[ext](file_path)
            audio_items = {key: value[0] for key, value in audio.items()}

        return audio_items
    except Exception as e:
        print('Error extracting metadata:', e)
