import os
import pandas as pd
from music_logger import gen_log
from song_sorter import sort_songs
a pd.DataFrame
def main():
    # Ruta a la carpeta de música
    music_folder = r'C:\Users\abrah\Downloads'

    # Generar el log de canciones
    print("Generando el log de canciones...")
    song_log = gen_log(music_folder)
    print("Log de canciones generado.")

    # Ordenar las canciones
    print("Ordenando las canciones...")
    sort_songs(music_folder)
    print("Canciones ordenadas.")

if __name__ == "__main__":
    main()