import os 
import datetime
from sorwave.logger import gen_log, new_log_file
import winshell
from progress.bar import Bar



def sintaxis_filter(path):
    unit = path[:2]
    path = path[2:]
    invalid_characters = '*?"<>|:/'  
    filtering_path = ''.join(caracter for caracter in path if caracter not in invalid_characters)
    return unit + filtering_path

def remove_empty_folders(path):
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
                    print(f"Missing permissions for {full_path}")

    # Check if the current directory is empty
    if not os.listdir(path):
        os.rmdir(path)
        print(f"Empty directory removed: {path}")

def sort_songs(folder_path, use_api=True):
    sorter_log = {}
    music_library = gen_log(folder_path, use_api, False)
    total_songs = 0
    for albums in music_library.values():
        for songs in albums.values():
            total_songs += len(songs)
    bar = Bar('Processing', max=total_songs)

    for fixed_artist, albums in music_library.items():
        artist_path = os.path.join(folder_path, fixed_artist.replace("/", "-"))

        for album, songs in albums.items():
            album_path = sintaxis_filter(os.path.join(artist_path, album))

            for song in songs:
                song_path = sintaxis_filter(os.path.join(album_path, ("{}. {}{}".format(song["tracknumber"], song["title"], song["extension"]))))
                bar.next()

                if not song_path.upper() == song["path"].upper():

                    if not os.path.exists(album_path):
                        os.makedirs(album_path)
                        os.rename(song["path"], song_path)

                    elif not os.path.exists(song_path):
                        os.rename(song["path"], song_path)
                        sorter_log[song["title"]] = [song["path"], song_path]

                    else:
                        new_song_path = sintaxis_filter(os.path.join(album_path, ("{}. {} (duplicate){}".format(song["tracknumber"], song["title"], song["extension"]))))
                        os.rename(song["path"], new_song_path)
                        sorter_log[song["title"] + " (duplicate)"] = [song["path"], new_song_path]
                            
    remove_empty_folders(folder_path)
    new_log_file((folder_path), sorter_log, f"sorter_log - {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}")
    gen_log(folder_path, use_api, True)

def create_shortcut(file_path, shortcut_path):
    shortcut_path = os.path.abspath(shortcut_path)
    
    with winshell.shortcut(shortcut_path) as link:
        link.path = file_path
        link.working_directory = os.path.dirname(file_path)
        link.description = f"Shortcut to {os.path.basename(file_path)}"

def new_playlist(folder_path, playlist_name):
    playlist_path = os.path.join(folder_path, "Playlists", playlist_name)
    if not os.path.exists(playlist_path):
        os.makedirs(playlist_path)
    return playlist_path    

def add_playlist(folder_path, file_path, playlist_name):
    playlist_path = new_playlist(folder_path, playlist_name)
    new_file_path = os.path.join(playlist_path, os.path.basename(file_path))
    if not os.path.exists(new_file_path):
        create_shortcut(file_path, new_file_path)
    

    