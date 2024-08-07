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

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]

word_extensions = [".doc", ".docx", ".docm", ".dotx", ".dotm", ".txt"]

excel_extensions = [".xlsx", ".xls", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xml", ".csv"]

pdf_extensions = [".pdf"]

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

    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not isdir(source_dir):
            logging.error(f"Source directory '{source_dir}' does not exist.")
            return
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_word_files(entry, name)
                self.check_excel_files(entry, name)
                self.check_pdf_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_word_files(self, entry, name):
        for word_extension in word_extensions:
            if name.endswith(word_extension) or name.endswith(word_extension.upper()):
                move_file(dest_dir_word, entry, name)
                logging.info(f"Moved word file: {name}")

    def check_excel_files(self, entry, name):
        for excel_extension in excel_extensions:
            if name.endswith(excel_extension) or name.endswith(excel_extension.upper()):
                move_file(dest_dir_excel, entry, name)
                logging.info(f"Moved excel file: {name}")

    def check_pdf_files(self, entry, name):
        for pdf_extension in pdf_extensions:
            if name.endswith(pdf_extension) or name.endswith(pdf_extension.upper()):
                move_file(dest_dir_pdf, entry, name)
                logging.info(f"Moved pdf file: {name}")

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