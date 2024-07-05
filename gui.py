import tkinter as tk
from tkinter import ttk
import subprocess
import os
import signal
import threading
import sys

# Global variable to keep track of the speedtest subprocess
speedtest_process = None

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.configure(state='normal')  # Enable writing to the Text widget
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.configure(state='disabled')  # Disable writing to the Text widget

    def flush(self):
        pass

def start_speedtest(filename):
    global speedtest_process
    speedtest_process = subprocess.Popen(
        ["python", "speedtest.py", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    threading.Thread(target=monitor_speedtest_output, args=(speedtest_process,)).start()
    print(f"Speed test started with filename: {filename}")

def monitor_speedtest_output(process):
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def stop_speedtest():
    global speedtest_process
    if speedtest_process:
        os.kill(speedtest_process.pid, signal.SIGINT)  # Send a SIGINT to the process
        speedtest_process = None
        print("Speed test stopped")

def update_start_button_state(*args):
    if filename_var.get():
        start_button.state(["!disabled"])
    else:
        start_button.state(["disabled"])

def on_start_pressed(event=None):
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
    root = tk.Tk()
    root.title("Continuous Speedtest")

    top_frame = ttk.Frame(root, padding="10 10 10 10")
    top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    filename_label = ttk.Label(top_frame, text=".csv filename")
    filename_label.grid(row=0, column=0, sticky=tk.W)

    global filename_var, filename_entry
    filename_var = tk.StringVar()
    filename_entry = ttk.Entry(top_frame, width=50, textvariable=filename_var)
    filename_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
    filename_var.trace_add("write", update_start_button_state)

    filename_entry.bind("<Return>", on_start_pressed)

    button_frame = ttk.Frame(root, padding="10 10 10 10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

    global start_button
    start_button = ttk.Button(button_frame, text="Start", command=on_start_pressed)
    start_button.grid(row=0, column=0, padx=5, pady=5)
    start_button.state(["disabled"])

    global stop_button
    stop_button = ttk.Button(button_frame, text="Stop", command=on_stop_pressed)
    stop_button.grid(row=0, column=1, padx=5, pady=5)
    stop_button.state(["disabled"])

    for child in top_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in button_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    output_frame = ttk.Frame(root, padding="10 10 10 10")
    output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    global output_text
    output_text = tk.Text(output_frame, wrap="word", height=15, width=80, state='disabled')
    output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    output_text['yscrollcommand'] = scrollbar.set

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    top_frame.columnconfigure(1, weight=1)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)

    # Redirect stdout to the Text widget
    sys.stdout = ConsoleRedirector(output_text)
    sys.stderr = ConsoleRedirector(output_text)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
