import os
import sorwave as sw

def main():
    # Ruta a la carpeta de música
    music_folder = r'C:\Users\abrah\Downloads'

    # Generar el log de canciones
    print("Generando el log de canciones...")
    song_log = sw.gen_log(music_folder)
    print("Log de canciones generado.")

    # Ordenar las canciones
    print("Ordenando las canciones...")
    sw.sort_songs(music_folder)
    print("Canciones ordenadas.")

if __name__ == "__main__":
    main()