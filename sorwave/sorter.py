import os 
import datetime
import platform
from sorwave.logger import gen_log, new_log_file
from progress.bar import Bar
from win32com.client import Dispatch



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

def sort_songs(folder_path, use_api=False):
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
    bar.finish()

def create_shortcut(target_path, shortcut_folder):
    try:
            if not os.path.exists(target_path):
                raise FileNotFoundError(f"Target path does not exist: {target_path}")
            
            # Ensure the shortcut folder exists
            os.makedirs(shortcut_folder, exist_ok=True)

            # Get the target's name without the extension
            shortcut_name = os.path.splitext(os.path.basename(target_path))[0]
            shortcut_path = os.path.join(shortcut_folder, shortcut_name)
            
            if platform.system() == "Windows":
                # Add .lnk extension for Windows shortcuts
                shortcut_path += ".lnk"
                
                # Create the shortcut
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(shortcut_path)
                shortcut.TargetPath = target_path
                shortcut.WorkingDirectory = os.path.dirname(target_path)
                shortcut.save()
                print(f"Windows shortcut created: {shortcut_path}")
            
            elif platform.system() == "Linux":
                # Create a symbolic link for Linux
                os.symlink(target_path, shortcut_path)
                print(f"Linux symbolic link created: {shortcut_path}")
            
            else:
                raise OSError("Unsupported operating system")
        
    except Exception as e:
        print(f"Error: {e}")

def new_playlist(folder_path, playlist_name):
    playlist_path = os.path.join(folder_path, "Playlists", playlist_name)
    if not os.path.exists(playlist_path):
        os.makedirs(playlist_path)
    return playlist_path    

def add_playlist(folder_path, file_path, playlist_name):
    playlist_path = new_playlist(folder_path, playlist_name)
    create_shortcut(file_path, playlist_path)
    

    