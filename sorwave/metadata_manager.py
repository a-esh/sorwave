import os
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from musicbrainzngs_API import set_useragent
import musicbrainzngs

file_extensions = {".flac": FLAC, ".mp3": EasyID3}

def get_file_extension(file_path):
    return os.path.splitext(file_path)[-1].lower()

def get_metadata(file_path,repair = False):
    try:
        ext = get_file_extension(file_path)
        if ext in file_extensions:
            audio = file_extensions[ext](file_path)
            audio_items = {key: value[0] for key, value in audio.items()}
            
        if repair and (not audio_items.get('artist') or not audio_items.get('title') or not audio_items.get('album')):   
            repair_metadata(file_path) 
            audio_items = get_metadata(file_path, False)
        return audio_items
    except Exception as e:
        print("Error extracting metadata:", e)
    return None

def repair_metadata(file_path):
    """
    Repairs the metadata of an audio file using the MusicBrainz database.
    """
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
            
            for key, value in metadata.items():
                if value:
                    audio[key] = value
            
            audio.save()
    except Exception as e:
        print("Error updating metadata:", e)

