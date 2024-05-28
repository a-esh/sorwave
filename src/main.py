
from music_logger import generate_log
from song_sorter import  sort_songs


def merge_folders(main_folder_path, source_folder_path):
    main_log = generate_log(main_folder_path)
    source_log = generate_log(source_folder_path)
    
main_folder_path = r"C:\Users\abrah\Music"
sort_songs(main_folder_path)