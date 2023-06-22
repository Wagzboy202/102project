import sys
import time
import random
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
        else:
            print(f"File created: {event.src_path}")
            self.handle_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            print(f"Directory modified: {event.src_path}")
        else:
            print(f"File modified: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            print(f"Directory moved/renamed: {event.src_path} -> {event.dest_path}")
        else:
            print(f"File moved/renamed: {event.src_path} -> {event.dest_path}")

    def on_deleted(self, event):
        if event.is_directory:
            print(f"Directory deleted: {event.src_path}")
        else:
            print(f"File deleted: {event.src_path}")

    def handle_file(self, file_path):
        from_dir = 'Document_Files'
        to_dir = "Destination"

        list_of_files = os.listdir(from_dir)

        for file_name in list_of_files:
            name, extension = os.path.splitext(file_name)
            if extension == '':
                continue
            else:
                if extension in ['.txt', '.doc', '.docs', '.pdf']:
                    source_path = os.path.join(from_dir, file_name)
                    destination_path = os.path.join(to_dir, 'Document_Files', file_name)

                    if os.path.exists(destination_path):
                        print("Moving " + file_name + "...")
                        shutil.move(source_path, destination_path)
                    else:
                        print('Destination directory does not exist')
                        print('Creating directory...')
                        os.makedirs(os.path.join(to_dir, 'Document_Files'))
                        print('Directory created')
                        print("Moving " + file_name + "...")
                        shutil.move(source_path, destination_path)


# Set the path for the directory to track changes
from_dir = "<Set path for tracking file system events>"
event_handler = FileEventHandler()
observer = Observer()
observer.schedule(event_handler, from_dir, recursive=True)
observer.start()

# Add code to stop the observer program when any key is pressed
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()

