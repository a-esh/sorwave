import os 
import platform
from .logger import gen_log, new_log_file
from progress.bar import Bar
from win32com.client import Dispatch

def sintaxis_filter(path):
    """
    This function takes a file path as input and removes any characters that are 
    considered invalid for file paths in most operating systems. The invalid 
    characters filtered out are: '*', '?', '<', '>', '|', ':', and '/'.

    Parameters:
    path (str): The file path to be filtered.

    Returns:
    str: The filtered file path with invalid characters removed.
    """

    unit = path[:2]
    path = path[2:]
    invalid_characters = "*?'<>|:/"
    filtering_path = ''.join(char for char in path if char not in invalid_characters)
    return unit + filtering_path

def remove_empty_folders(path):
    """
    This function traverses the directory tree rooted at the specified path,
    and removes any empty folders it encounters. If a folder contains only
    a 'desktop.ini' file, it is also considered empty and will be removed.
    The function handles permission errors by attempting to change the file
    permissions before retrying the removal.

    Parameters:
    path (str): The root directory path to start the search for empty folders.
    Raises:

    PermissionError: If the function lacks the necessary permissions to remove
                     a file or directory, it will print a message indicating
                     the missing permissions.
    """
    for current_dir, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            full_path = os.path.join(current_dir, dir_name)
            if not os.listdir(full_path) or (len(os.listdir(full_path)) == 1 and os.listdir(full_path)[0].lower() == 'desktop.ini'):
                # Remove files in the directory
                try:
                    for file_name in os.listdir(full_path):
                        file_path = os.path.join(full_path, file_name)
                        try:
                            os.remove(file_path)
                        except PermissionError:
                            os.chmod(file_path, 0o777)
                            os.remove(file_path)
                    
                    # Remove the directory itself
                    try:
                        os.rmdir(full_path)
                    except PermissionError:
                        os.chmod(full_path, 0o777)
                        os.rmdir(full_path)
                        
                except PermissionError:
                    print(f'Missing permissions for {full_path}')

    # Check if the current directory is empty
    if not os.listdir(path):
        os.rmdir(path)
        print(f'Empty directory removed: {path}')

def sort_song(file_path, library_path):
    """
    Sorts a song file into a structured music library.
    This function takes a song file and organizes it into a music library
    based on the song's metadata. It creates directories for the artist and
    album if they do not exist, and moves the song file to the appropriate
    location. If a song with the same name already exists, it appends
    "(duplicate)" to the filename.
    Args:
        file_path (str): The path to the song file to be sorted.
        library_path (str): The root path of the music library.
    Returns:
        dict: A dictionary containing the log of moved files. The keys are
              the song titles, and the values are lists with the original
              and new file paths.
    Example:
        sorter_log = sort_song('/path/to/song.mp3', '/path/to/music/library')
        print(sorter_log)
    """

    song_data = gen_log(file_path, library_path,  False)
    artist = list(song_data.keys())[0]
    album = list(song_data[artist].keys())[0]
    song = song_data[artist][album][0]
    
    artist_path = os.path.abspath(os.path.join(library_path, artist))
    album_path = sintaxis_filter(os.path.join(artist_path, album))
    song_path = sintaxis_filter(os.path.join(album_path, ('{}. {}{}'.format(song['tracknumber'], song['title'], song['extension']))))
    
    sorter_log = {}

    if not song_path.upper() == song['path'].upper():

        if not os.path.exists(album_path):
            os.makedirs(album_path)
            os.rename(song['path'], song_path)

        elif not os.path.exists(song_path):
            os.rename(song['path'], song_path)
            sorter_log[song['title']] = [song['path'], song_path]

        else:
            new_song_path = sintaxis_filter(os.path.join(album_path, ('{}. {} (duplicate){}'.format(song['tracknumber'], song['title'], song['extension']))))
            os.rename(song['path'], new_song_path)
            sorter_log[song['title'] + ' (duplicate)'] = [song['path'], new_song_path]

    remove_empty_folders(library_path)
    new_log_file(library_path, song_data, 'sorter_log', sorter_log)

    return sorter_log

def sort_library(folder_path):
    """
    Sorts a music library by organizing songs into artist and album folders.
    Args:
        folder_path (str): The path to the folder containing the music library.
    Returns:
        dict: A log of the sorting process, with song titles as keys and lists of 
              original and new paths as values.
    This function performs the following steps:
    1. Generates a log of the music library.
    2. Counts the total number of songs.
    3. Iterates through the music library, organizing songs into artist and album folders.
    4. Renames and moves songs to their new locations.
    5. Handles duplicate songs by appending "(duplicate)" to their filenames.
    6. Removes empty folders.
    7. Creates a new log file documenting the sorting process.
    Example:
        sorter_log = sort_library('/path/to/music/library')
    """

    sorter_log = {}
    folder_path = os.path.abspath(folder_path)
    print('Getting songs data:')
    music_library = gen_log(folder_path, False)
    print('\nSorting songs:')
    total_songs = 0
    
    for albums in music_library.values():
        for songs in albums.values():
            total_songs += len(songs)
    bar = Bar('Processing', max=total_songs)

    for artist, albums in music_library.items():
        artist_path = os.path.join(folder_path, artist.replace('/', '-'))

        for album, songs in albums.items():
            album_path = sintaxis_filter(os.path.join(artist_path, album))

            for song in songs:
                bar.next()
                song_path = sintaxis_filter(os.path.join(album_path, ('{}. {}{}'.format(song['tracknumber'], song['title'], song['extension']))))
                
                if not song_path.upper() == song['path'].upper():

                    if not os.path.exists(album_path):
                        os.makedirs(album_path)
                        os.rename(song['path'], song_path)

                    elif not os.path.exists(song_path):
                        os.rename(song['path'], song_path)
                        sorter_log[song['title']] = [song['path'], song_path]

                    else:
                        new_song_path = sintaxis_filter(os.path.join(album_path, ('{}. {} (duplicate){}'.format(song['tracknumber'], song['title'], song['extension']))))
                        os.rename(song['path'], new_song_path)
                        sorter_log[song['title'] + ' (duplicate)'] = [song['path'], new_song_path]

    remove_empty_folders(folder_path)
    new_log_file(folder_path, music_library, 'sorter_log', sorter_log)
    bar.finish()

    return sorter_log

def create_shortcut(target_path, shortcut_folder):
    '''
    Creates a shortcut to the target path in the specified folder.
    '''
    try:
        if not os.path.exists(target_path):
            raise FileNotFoundError(f'Target path does not exist: {target_path}')
        
        # Ensure the shortcut folder exists
        os.makedirs(shortcut_folder, exist_ok=True)

        # Get the target's name without the extension
        shortcut_name = os.path.splitext(os.path.basename(target_path))[0]
        shortcut_path = os.path.join(shortcut_folder, shortcut_name)
        
        if platform.system() == 'Windows':
            # Add .lnk extension for Windows shortcuts
            shortcut_path += '.lnk'
            
            # Create the shortcut
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = target_path
            shortcut.WorkingDirectory = os.path.dirname(target_path)
            shortcut.save()
            print(f'Windows shortcut created: {shortcut_path}')
        
        elif platform.system() == 'Linux':
            # Create a symbolic link for Linux
            os.symlink(target_path, shortcut_path)
            print(f'Linux symbolic link created: {shortcut_path}')
        
        else:
            raise OSError('Unsupported operating system')
    
    except Exception as e:
        print(f'Error: {e}')

def new_playlist(folder_path, playlist_name):
    '''
    Creates a new playlist folder.
    '''
    folder_path = os.path.abspath(folder_path)
    playlist_path = os.path.join(folder_path, 'Playlists', playlist_name)
    if not os.path.exists(playlist_path):
        os.makedirs(playlist_path)
    return playlist_path    

def add_playlist(folder_path, file_path, playlist_name):
    '''
    Adds a file to a playlist by creating a shortcut in the playlist folder.
    '''
    file_path = os.path.abspath(file_path)
    folder_path = os.path.abspath(folder_path)
    playlist_path = new_playlist(folder_path, playlist_name)
    create_shortcut(file_path, playlist_path)
    print(f'Added to playlist: {playlist_path}')