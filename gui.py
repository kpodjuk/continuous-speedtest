import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys

# Global variable to keep track of the speedtest subprocess
speedtest_process = None


def start_speedtest(filename):
    global speedtest_process
    # Get the path to the current Python executable (which should be from the virtual environment)
    python_executable = sys.executable
    speedtest_process = subprocess.Popen([python_executable, "speedtest.py", filename])
    print(f"Speed test started with filename: {filename}")


def stop_speedtest():
    global speedtest_process
    if speedtest_process:
        speedtest_process.terminate()
        speedtest_process = None
        print("Speed test stopped")


def update_start_button_state(*args):
    # Enable the start button only if the filename entry is not empty
    if filename_var.get():
        start_button.state(["!disabled"])
    else:
        start_button.state(["disabled"])


def on_start_pressed():
    filename = filename_var.get()
    start_speedtest(filename)
    stop_button.state(["!disabled"])
    start_button.state(["disabled"])
    filename_entry.state(["disabled"])


def on_stop_pressed():
    stop_speedtest()
    stop_button.state(["disabled"])
    filename_entry.state(["!disabled"])
    update_start_button_state()


def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Simple GUI")

    # Create a frame for the top section
    top_frame = ttk.Frame(root, padding="10 10 10 10")
    top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Add a label for the text field
    filename_label = ttk.Label(top_frame, text=".csv filename")
    filename_label.grid(row=0, column=0, sticky=tk.W)

    # Add the text field
    global filename_var, filename_entry
    filename_var = tk.StringVar()
    filename_entry = ttk.Entry(top_frame, width=50, textvariable=filename_var)
    filename_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
    filename_var.trace_add("write", update_start_button_state)

    # Create a frame for the buttons
    button_frame = ttk.Frame(root, padding="10 10 10 10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

    # Add the start button
    global start_button
    start_button = ttk.Button(button_frame, text="Start", command=on_start_pressed)
    start_button.grid(row=0, column=0, padx=5, pady=5)
    start_button.state(["disabled"])

    # Add the stop button
    global stop_button
    stop_button = ttk.Button(button_frame, text="Stop", command=on_stop_pressed)
    stop_button.grid(row=0, column=1, padx=5, pady=5)
    stop_button.state(["disabled"])

    # Add padding around all the widgets
    for child in top_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in button_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Make the main window resizeable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    top_frame.columnconfigure(1, weight=1)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    create_gui()
