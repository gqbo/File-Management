from os import scandir, rename, path
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer # Waits for any events on the watched directory (when there's a change in the downloads directory)
from watchdog.events import FileSystemEventHandler # Takes action when an event is received

# SET YOUR OWN PATHS HERE.
DOWNLOADS_PATH =    "D:\\Downloads"
DOCUMENTS_PATH =    "D:\\Downloaded_Documents"
IMAGES_PATH =       "D:\\Downloaded_Images"
VIDEOS_PATH =       "D:\\Downloaded_Videos"
AUDIOS_PATH =       "D:\\Downloaded_Audios"
EXE_PATH =          "D:\\Downloaded_Executables"
COMPRESSED_PATH =   "D:\\Downloaded_Compressed"

audio_extensions = {".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"}

image_extensions = {".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"}

video_extensions = {".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"}

document_extensions = {".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"}

compression_extensions = {".gz", ".bz2", ".rar",
                          ".zip", ".7z"}

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = Handler()
        self.observer.schedule(event_handler, DOWNLOADS_PATH, recursive = True)
        self.observer.start()

        try:
            while True:
                sleep(10)
        except KeyboardInterrupt:
            logging.error(f"Error occurred: {str(e)}")
            self.observer.stop()
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            self.observer.stop()

        self.observer.join()

class Handler(FileSystemEventHandler):

    def on_modified(self, event):
        if not event.is_directory:
            with scandir(DOWNLOADS_PATH) as entries:
                for entry in entries:
                    name = entry.name
                    self.check_audio_files(entry, name)
                    self.check_video_files(entry, name)
                    self.check_image_files(entry, name)
                    self.check_document_files(entry, name)
                    self.check_compressed_files(entry, name)
    
    def check_audio_files(self, entry, name):
        if name.endswith(tuple(audio_extensions)):
            move_file(AUDIOS_PATH, entry, name)
            logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        if name.endswith(tuple(video_extensions)):
            move_file(VIDEOS_PATH, entry, name)
            logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        if name.endswith(tuple(image_extensions)):
            move_file(IMAGES_PATH, entry, name)
            logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        if name.endswith(tuple(document_extensions)):
            move_file(DOCUMENTS_PATH, entry, name)
            logging.info(f"Moved document file: {name}")

    def check_compressed_files(self, entry, name):
        if name.endswith(tuple(compression_extensions)):
            move_file(COMPRESSED_PATH, entry, name)
            logging.info(f"Moved compressed file: {name}")

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)

    move(entry, dest)

if __name__ == "__main__":
    watcher = Watcher()
    watcher.run()