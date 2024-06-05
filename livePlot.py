import matplotlib.pyplot as plt
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import os


class DataHandler(FileSystemEventHandler):
    def __init__(self, file_path, ax):
        self.file_path = file_path
        self.ax = ax
        (self.line_download,) = ax.plot([], [], linestyle="-", label="Download (Mbps)")
        (self.line_upload,) = ax.plot([], [], linestyle="--", label="Upload (Mbps)")
        (self.line_ping,) = ax.plot([], [], linestyle="-.", label="Ping (ms)")
        self.ax.legend()
        self.update_plot()

    def on_modified(self, event):
        if event.src_path == self.file_path:
            self.update_plot()

    def update_plot(self):
        data = pd.read_csv(self.file_path)
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data.sort_values("timestamp", inplace=True)

        self.line_download.set_data(data["timestamp"], data["download"])
        self.line_upload.set_data(data["timestamp"], data["upload"])
        self.line_ping.set_data(data["timestamp"], data["ping"])

        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.xaxis.set_major_formatter(
            plt.matplotlib.dates.DateFormatter("%H:%M:%S")
        )
        plt.draw()


def main():
    if len(sys.argv) != 2:
        print("Usage: python livePlot.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("Time")
    ax.set_ylabel("Speed/Latency")
    ax.set_title(f"Live Speed Test Data - {os.path.basename(file_path)}")

    event_handler = DataHandler(file_path, ax)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            plt.pause(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
