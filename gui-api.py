import tkinter as tk
from tkinter import ttk


def start_action():
    print("Start button clicked")
    # Add your start action code here


def stop_action():
    print("Stop button clicked")
    # Add your stop action code here


# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a frame for the CSV filename input
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Add the CSV filename label and text entry field
csv_label = ttk.Label(frame, text=".csv filename")
csv_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

csv_entry = ttk.Entry(frame, width=50)
csv_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

# Add the Start and Stop buttons
start_button = ttk.Button(root, text="Start", command=start_action)
start_button.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_action)
stop_button.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)

# Configure the main window to resize properly
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Start the Tkinter event loop
root.mainloop()
