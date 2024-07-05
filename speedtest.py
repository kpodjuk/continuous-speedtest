import os
import subprocess
import time
import csv
import signal
import sys
import json
from datetime import datetime
import argparse

venv_python = os.path.join(
    ".venv", "bin", "python" if os.name != "nt" else "Scripts\\python"
)

parser = argparse.ArgumentParser(
    description="Perform speedtests and save result in .csv"
)
parser.add_argument("filename", type=str, help="The CSV file to output to")
args = parser.parse_args()

def signal_handler(sig, frame):
    print("Exiting the script.")
    sys.exit(0)

def run_speedtest():
    try:
        if os.name == "nt":
            venv_path = os.path.join(".venv", "Scripts", "speedtest-cli.exe")
        else:
            venv_path = os.path.join(".venv", "bin", "speedtest-cli")

        result = subprocess.run(
            [venv_path, "--json"], capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running speedtest-cli: {e}")
        return None

def append_to_log(data, log_file):
    if data:
        fieldnames = [
            "timestamp",
            "download",
            "upload",
            "ping",
            "server",
            "ssid",
            "signalStrength",
        ]
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(
                {
                    "timestamp": data["timestamp"],
                    "download": data["download"] / 1e6,
                    "upload": data["upload"] / 1e6,
                    "ping": data["ping"],
                    "server": data["server"]["host"],
                    "ssid": data["ssid"],
                    "signalStrength": data["signalStrength"],
                }
            )

def get_wifi_ssid():
    netsh_output = subprocess.check_output(
        "netsh wlan show interfaces", shell=True
    ).decode("utf-8", errors="ignore")
    for line in netsh_output.split("\n"):
        if "SSID" in line and "BSSID" not in line:
            ssid = line.split(":")[1].strip()
            return ssid
    return "0"

def get_wifi_signal_strength():
    netsh_output = subprocess.check_output(
        "netsh wlan show interfaces", shell=True
    ).decode("utf-8", errors="ignore")
    for line in netsh_output.split("\n"):
        if "Signal" in line:
            signal_strength = line.split(":")[1].strip().replace("%", "")
            return signal_strength
    return "0"

def main():
    os.makedirs("output", exist_ok=True)
    log_file = args.filename
    log_file += datetime.now().strftime("_%Y-%m-%d-%H-%M-%S") + ".csv"
    log_file = os.path.join("output", log_file)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting continuous speed tests. Press Ctrl+C to stop.")

    while True:
        result = run_speedtest()
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

        if result:
            result["timestamp"] = current_timestamp
            result["ssid"] = get_wifi_ssid()
            result["signalStrength"] = get_wifi_signal_strength()
            append_to_log(result, log_file)
            print(
                f"Logged result: {current_timestamp}, Download: {result['download']/1e6:.2f} Mbps, Upload: {result['upload']/1e6:.2f} Mbps, Ping: {result['ping']} ms, SSID: {result['ssid']}, signalStrength: {result['signalStrength']}"
            )
        else:
            print("Retrying in 1 minute due to error.")
            data = {
                "timestamp": current_timestamp,
                "download": 0,
                "upload": 0,
                "ping": 0,
                "server": {"host": 0},
                "ssid": 0,
                "signalStrength": 0,
            }
            append_to_log(data, log_file)
            time.sleep(60)
        time.sleep(1)

if __name__ == "__main__":
    main()
