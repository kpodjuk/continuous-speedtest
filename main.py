import os
import subprocess
import time
import csv
import signal
import sys
import json
from datetime import datetime
import pytz

def signal_handler(sig, frame):
    print("Exiting the script.")
    sys.exit(0)


def run_speedtest():
    try:
        result = subprocess.run(
            ["speedtest-cli", "--json"], capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running speedtest-cli: {e}")
        return None


def append_to_log(data, log_file):
    # print(data)
    if data:
        fieldnames = ["timestamp", "download", "upload", "ping", "server"]
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "timestamp": data["timestamp"],
                    "download": data["download"] / 1e6,  # Convert from bps to Mbps
                    "upload": data["upload"] / 1e6,  # Convert from bps to Mbps
                    "ping": data["ping"],
                    "server": data["server"]["host"],
                }
            )


def list_files(directory):
    files = os.listdir(directory)
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    return files


def main():

    # Create output folder
    os.makedirs("output", exist_ok=True)

    log_file = ""
    # Ask the user for the desired CSV filename or 'p' to plot data
    user_input = input(
        "Enter the desired filename for the CSV log (without .csv extension), enter 'p' if you want to plot recorded data: "
    )

    if user_input.lower() == "p":
        files = list_files("output")
        if not files:
            print("No files found in the 'output' directory.")
            return

        print("Select a file to plot:")
        for i, filename in enumerate(files, start=1):
            print(f"{i} - {filename}")

        file_index = int(input("Enter the number corresponding to the file: ")) - 1
        if 0 <= file_index < len(files):
            selected_file = files[file_index]
            plot_script = "plot.py"

            # add .venv for plot.py execution
            venv_python = os.path.join(".venv", "Scripts", "python")

            subprocess.run(
                [venv_python, plot_script, os.path.join("output", selected_file)]
            )

        else:
            print("Invalid selection.")
        return

    log_file += user_input

    # Append timestamp filename
    current_time = datetime.now().strftime("_%Y-%m-%d-%H-%M-%S")

    log_file += current_time + ".csv"
    log_file = os.path.join("output", log_file)

    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting continuous speed tests. Press Ctrl+C to stop.")

    while True:
        result = run_speedtest()
        if result:
            append_to_log(result, log_file)
            print(
                f"Logged result: {result['timestamp']}, Download: {result['download']/1e6:.2f} Mbps, Upload: {result['upload']/1e6:.2f} Mbps, Ping: {result['ping']} ms"
            )
        else:
            print("Retrying in 1 minute due to error.")

            # add 0s to csv so it's clear on the plot when speedtest failed
            current_timestamp = (
                datetime.now(pytz.utc).isoformat(timespec="microseconds") + "Z"
            )
            csv_line = f"{current_timestamp},0,0,0,0"
            with open(log_file, "a") as file:
                file.write(csv_line + "\n")
            time.sleep(60)  # Wait for 1 minute before retrying

        # Wait for a specified interval before the next test
        time.sleep(1)


if __name__ == "__main__":
    main()
