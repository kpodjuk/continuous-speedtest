import subprocess
import time
import csv
import signal
import sys
import json
from datetime import datetime


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


def main():
    # Ask the user for the desired CSV filename
    log_file = input(
        "Enter the desired filename for the CSV log (without .csv extension): "
    )

    # Append some identification info to filename
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    log_file += "-speedTest-" + current_time + ".csv"

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
            time.sleep(60)  # Wait for 1 minute before retrying

        # Wait for a specified interval before the next test
        time.sleep(1)


if __name__ == "__main__":
    main()
