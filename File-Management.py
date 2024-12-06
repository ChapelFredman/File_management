import os
from os import scandir, rename, makedirs
from os.path import splitext, exists, join, isdir
from shutil import move
from time import sleep

import logging
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = r"c:\Users\Eden\Downloads"
dest_dir_sfx = r"c:\Users\Eden\Desktop\Descargas\Sound"
dest_dir_music = r"c:\Users\Eden\Desktop\Descargas\Music"
dest_dir_video = r"c:\Users\Eden\Desktop\Descargas\Video"
dest_dir_image = r"c:\Users\Eden\Desktop\Descargas\Image"
dest_dir_excel = r"c:\Users\Eden\Desktop\Descargas\Excels"
dest_dir_pdf = r"c:\Users\Eden\Desktop\Descargas\PDF"
dest_dir_word = r"c:\Users\Eden\Desktop\Descargas\Word"

# Define file extensions
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
word_extensions = [".doc", ".docx", ".docm", ".dotx", ".dotm", ".txt"]
excel_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xml", ".csv"]
pdf_extensions = [".pdf"]

file_type_map = {
    tuple(image_extensions): dest_dir_image,
    tuple(video_extensions): dest_dir_video,
    tuple(audio_extensions): dest_dir_music,
    tuple(word_extensions): dest_dir_word,
    tuple(excel_extensions): dest_dir_excel,
    tuple(pdf_extensions): dest_dir_pdf,
}

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if not isdir(dest):
        makedirs(dest, exist_ok=True)

    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        dest = join(dest, unique_name)

    try:
        move(entry, dest)
        logging.info(f"Moved file: {name} to {dest}")
    except Exception as e:
        logging.error(f"Error moving file {name}: {str(e)}")

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not isdir(source_dir):
            logging.error(f"Source directory '{source_dir}' does not exist.")
            return

        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                for file_types, dest in file_type_map.items():
                    if any(name.endswith(ext) or name.endswith(ext.upper()) for ext in file_types):
                        move_file(dest, entry, name)
                        break  # Exit the loop after a match is found

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                          format='%(asctime)s - %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()