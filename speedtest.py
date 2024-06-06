from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import subprocess


class CSVHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            subprocess.call(["python", "dynamicPlot.py", self.file_path])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Monitor CSV file and update plot dynamically."
    )
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print(f"File {args.file_path} does not exist.")
    else:
        event_handler = CSVHandler(args.file_path)
        observer = Observer()
        observer.schedule(
            event_handler, path=os.path.dirname(args.file_path), recursive=False
        )
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
