import tkinter as tk
from tkinter import ttk


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
    filename_entry = ttk.Entry(top_frame, width=50)
    filename_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

    # Create a frame for the buttons
    button_frame = ttk.Frame(root, padding="10 10 10 10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

    # Add the start button
    start_button = ttk.Button(
        button_frame, text="Start", command=lambda: print("Start button clicked")
    )
    start_button.grid(row=0, column=0, padx=5, pady=5)

    # Add the stop button
    stop_button = ttk.Button(
        button_frame, text="Stop", command=lambda: print("Stop button clicked")
    )
    stop_button.grid(row=0, column=1, padx=5, pady=5)

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
