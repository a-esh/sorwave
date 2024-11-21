import os
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from tinytag import TinyTag
import musicbrainzngs
from .musicbrainzngs_API import set_useragent



file_extensions = {".flac": FLAC, ".mp3": EasyID3}

def get_file_extension(file_path):
    return os.path.splitext(file_path)[-1].lower()

def get_metadata(file_path, repair=False):
    try:
        ext = get_file_extension(file_path)
        if ext in file_extensions:
            metadata = (TinyTag.get(file_path)).__dict__

        if repair and (not metadata.get('artist') or not metadata.get('albumartist') or not metadata.get('title') or not metadata.get('album')):   
            repair_metadata(file_path) 
            metadata = get_metadata(file_path, False)
        
        if not metadata.get('album'):
            metadata['album'] = metadata['title']

        return metadata
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None

def repair_metadata(file_path):
    """
    Repairs the metadata of an audio file using the MusicBrainz database.
    """
    file_path = os.path.abspath(file_path)
    set_useragent()
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    try:
        result = musicbrainzngs.search_recordings(recording=file_name, limit=1)
        
        # Verifica que 'recording-list' esté presente y sea una lista
        if isinstance(result.get('recording-list', None), list) and result['recording-list']:
            recording = result['recording-list'][0]
            
            # Usa .get() para acceder a las claves y evitar errores si no existen
            title = recording.get('title')
            artist_credit = recording.get('artist-credit', [])
            release_list = recording.get('release-list', [])
            tag_list = recording.get('tag-list', [])
            medium_list = recording.get('medium-list', [])

            print('\n')
            print("Title:", title)
            print("Artist Credit:", artist_credit)
            print("Release List:", release_list)
            print("Tag List:", tag_list)
            print("Medium List:", medium_list)

            metadata = {
                'title': title,
                'artist': artist_credit[0]['artist']['name'] if artist_credit else None,
                'album': release_list[0]['title'] if release_list else None,
                'genre': tag_list[0]['name'] if tag_list else None,
                'tracknumber': medium_list[0]['track-list'][0]['number'] if medium_list else None,
                'albumartist': artist_credit[0]['artist']['name'] if artist_credit else None
            }
            print (metadata)
            # Procesar el archivo de audio dependiendo de la extensión
            ext = get_file_extension(file_path)
            audio = file_extensions[ext](file_path)
            
            # Actualiza los metadatos
            for key, value in metadata.items():
                if value:
                    audio[key] = value
            
            audio.save()
            
        else:
            print("No se encontró una lista válida en 'recording-list'.")
    except Exception as e:
        print("Error updating metadata:", e)