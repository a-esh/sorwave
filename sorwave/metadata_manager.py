import os
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import musicbrainzngs
import json
from .musicbrainzngs_API import set_useragent
from .logger import new_log


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

def fix_metadata(file_path, library_path):
    """
    This function retrieves the current metadata of the specified audio file,
    searches for the correct metadata using the MusicBrainz database, and updates
    the file with the new metadata if found. It also logs the changes made to the metadata.
    Args:
        file_path (str): The path to the audio file whose metadata needs to be fixed.
        library_path (str): The path to the library where the log of metadata changes will be stored.
    Returns:
        dict: A dictionary containing the old and new metadata of the audio file.
    Raises:
        Exception: If there is an error while updating the metadata.
    Example:
        metadata_changes = fix_metadata('/path/to/audio/file.mp3', '/path/to/library')
    """
    metadata_changes = {}
    metadata = get_metadata(file_path, True)
    metadata_changes['old_metadata'] = {key: value for key, value in metadata.items() if not value}

    file_path = os.path.abspath(file_path)
    set_useragent()
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    try:
        result = musicbrainzngs.search_recordings(recording=file_name, limit=1)
        if result['recording-list']:
            recording = result['recording-list'][0]
            metadata = {
            'title': recording['title'],
            'artist': recording['artist-credit'][0]['artist']['name'],
            'album': recording['release-list'][0]['title'] if 'release-list' in recording else None,
            'genre': recording['tag-list'][0]['name'] if 'tag-list' in recording else None,
            'tracknumber': recording['medium-list'][0]['track-list'][0]['number'] if 'medium-list' in recording else None,
            'albumartist': recording['artist-credit'][0]['artist']['name'] if 'artist-credit' in recording else None
            }
            
            ext = get_file_extension(file_path)
            audio = file_extensions[ext](file_path)
            
            metadata_changes['new_metadata'] = metadata
            audio.save()

            if metadata_changes['old_metadata'] != metadata_changes['new_metadata']:
                new_log(library_path, metadata_changes, 'metadata_changes')

    except Exception as e:
        print('Error updating metadata:', e)

    return metadata_changes

def previw_fix_metadata(file_path):
    """
    Preview and fix metadata of a given file.
    This function retrieves the current metadata of the specified file,
    prints it, fixes the metadata using the `fix_metadata` function, 
    retrieves the new metadata, prints it, and returns both the old 
    and new metadata.
    Args:
        file_path (str): The path to the file whose metadata needs to be fixed.
    Returns:
        tuple: A tuple containing two elements:
            - old_metadata: The metadata of the file before fixing.
            - new_metadata: The metadata of the file after fixing.
    """

    metadata = get_metadata(file_path)
    print('Old metadata:', metadata)
    old_metadata = metadata

    fix_metadata(file_path)

    metadata = get_metadata(file_path)
    print('New metadata:', metadata)
    new_metadata = metadata

    return old_metadata, new_metadata

def backup(file_path, backup_file):
    """
    Restores the metadata of the specified audio file from a backup JSON file.
    Args:
        file_path (str): The path to the audio file whose metadata needs to be restored.
        backup_file (str): The path to the backup JSON file containing the old metadata.
    Raises:
        Exception: If there is an error while restoring the metadata.
    """
    try:
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        old_metadata = backup_data.get('old_metadata', {})
        
        ext = get_file_extension(file_path)
        if ext in file_extensions:
            audio = file_extensions[ext](file_path)
            for key, value in old_metadata.items():
                audio[key] = value
            audio.save()
        
        print('Metadata restored successfully.')
    except Exception as e:
        print('Error restoring metadata:', e)