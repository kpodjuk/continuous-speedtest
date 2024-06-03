import speedtest
import time
import json
import signal
import sys

# Define the log file path
LOG_FILE = "speedtest_log.json"


def signal_handler(sig, frame):
    print("Exiting the script.")
    sys.exit(0)


def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    return st.results.dict()


def append_to_log(data):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(data) + "\n")


def main():
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting continuous speed tests. Press Ctrl+C to stop.")

    while True:
        try:
            result = run_speedtest()
            append_to_log(result)
            print(f"Logged result: {result['timestamp']}")
            # Wait for a specified interval before the next test (e.g., 1 hour)
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Retry after 1 minute if an error occurs


if __name__ == "__main__":
    main()
