import os
import json
import datetime
from .metadata_extractor import get_metadata
from progress.bar import Bar

def get_main_artist(artist):
    """
    Extracts the main artist's name from a string that may contain multiple artists.
    This function takes a string representing an artist or multiple artists and 
    returns the main artist's name by splitting the string at common dividers 
    such as ',', '/', 'Ft.', 'feat.', 'Feat', and '&'. It assumes that the main 
    artist's name appears before any of these dividers.
    Args:
        artist (str): A string containing the artist's name(s).
    Returns:
        str: The main artist's name.
    """

    dividers = [',', '/', 'Ft.', 'feat.', 'Feat', '&']
    for fix in dividers:
        artist = artist.split(fix)[0].strip()
    return artist

def new_log_file(folder_path, log_dict, log_type, sorter_log=None):
    """
    Creates a new log file in the specified folder with the given log data.
    Args:
        folder_path (str): The path to the folder where the log file will be created.
        log_dict (dict): The dictionary containing the log data to be saved.
        log_type (str): The type of log being created. This will be included in the log file name.
        sorter_log (optional): Additional log information specific to 'sorter_log' type. Defaults to None.
    Returns:
        None
    Raises:
        OSError: If there is an issue creating or writing to the log file.
    Notes:
        - The log file is named using the log type and the current date and time.
        - If a log file with the same name already exists, it will be overwritten.
        - On Windows, the log file is hidden after creation.
    """
    date = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    log_path = os.path.join(folder_path, f'{log_type} {date.replace(':', '-')}.json')
    log_info = {
        'date': date,
        'type': log_type,
        'data': log_dict,
    }
    if log_type == 'sorter_log':
        log_info['sorter_log'] = sorter_log

    if os.path.exists(log_path):
        os.remove(log_path)
    with open(log_path, 'w', encoding='utf-8') as json_file:
        json.dump(log_info, json_file, ensure_ascii=False, indent=4)
        json_file.write('\n')

    # Hide the log file (Windows-specific)
    if os.name == 'nt':
        os.system(f'attrib +h "{log_path}"')

def gen_log(path, library_path=False , gen_log=True):
    def gen_log(path, library_path=False, gen_log=True):
        """
        Generates a log of song metadata from a given directory or file path.
        Args:
            path (str): The path to the directory or file to process.
            library_path (str, optional): The path where the log files will be saved. Defaults to False.
            gen_log (bool, optional): Whether to generate log files. Defaults to True.
        Returns:
            dict: A dictionary containing the song metadata log.
        The function processes all `.flac` and `.mp3` files in the specified directory or file path.
        It extracts metadata from each song file and organizes it by artist and album.
        If metadata errors are encountered, they are logged separately.
        Example:
            song_log = gen_log('/path/to/music/library')
        """

    def process_file(file_path, song_log, bugs_log):
        song_metadata = get_metadata(file_path)
        if not song_metadata:
            bugs_log['Metadata error'] = file_path
        else:
            artist = song_metadata.get('albumartist', song_metadata.get('artist'))
            artist = get_main_artist(artist)
            album = song_metadata.get('album', song_metadata.get('title'))
            album = album.replace('/', '-')
            song_metadata['tracknumber'] = song_metadata.get('tracknumber', 1)

            if artist not in song_log:
                song_log[artist] = {}
            if album not in song_log[artist]:
                song_log[artist][album] = []
            song_log[artist][album].append({
                'artist': song_metadata.get('artist'),
                'albumartist': song_metadata.get('albumartist'),
                'title': song_metadata['title'],
                'tracknumber': str(song_metadata['tracknumber']).split('/')[0],
                'genre': song_metadata.get('genre'),
                'path': file_path,
                'extension': os.path.splitext(file_path)[1],
            })

    song_log = {}
    bugs_log = {}

    if not library_path:
        library_path = path


    if os.path.isdir(path):
        total_files = sum([len(files) for r, d, files in os.walk(path) if any(f.endswith(('.flac', '.mp3')) for f in files)])
        bar = Bar('Processing', max=total_files)

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.flac') or file.endswith('.mp3'):
                    bar.next()
                    file_path = os.path.join(root, file)
                    process_file(file_path, song_log, bugs_log)

        bar.finish()
    elif os.path.isfile(path) and path.endswith(('.flac', '.mp3')):
        process_file(path, song_log, bugs_log)

    if gen_log:
        new_log_file(library_path, song_log, 'songs_log')
    if bugs_log:
        new_log_file(library_path, bugs_log, 'metadataBugs_log')

    return song_log