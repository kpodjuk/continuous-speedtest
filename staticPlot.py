import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse


# Set up argument parser
parser = argparse.ArgumentParser(description="Plot speedtest data from a CSV file.")
parser.add_argument("filename", type=str, help="The CSV file to plot")
args = parser.parse_args()

# Load the CSV file
filename = args.filename
print("Plotting: " + filename)
df = pd.read_csv(filename)

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract test name and timestamp from filename
basename = os.path.basename(filename)
test_name, timestamp_str = basename.split("_")
timestamp = datetime.strptime(timestamp_str.replace(".csv", ""), "%Y-%m-%d-%H-%M-%S")

# Set the Figure size
plt.figure(figsize=(14, 7))

# Plot download, upload, and ping using Seaborn with different line styles
sns.lineplot(
    data=df, x="timestamp", y="download", label="Download", marker="o", linestyle="-"
)  # Solid line
sns.lineplot(
    data=df, x="timestamp", y="upload", label="Upload", marker="o", linestyle="--"
)  # Dotted line
sns.lineplot(
    data=df, x="timestamp", y="ping", label="Ping", marker="o", linestyle="-."
)  # Dash-dot line

# Add titles and labels
plt.title(f"{test_name} - Test conducted at {timestamp}", fontsize=16)
plt.xlabel("Timestamp")
plt.ylabel("Values [Mbs]")
plt.legend()

# Enable zooming with scroll wheel
from matplotlib.widgets import Slider

# Add grid
plt.grid(True, axis="y")

# Show the plot
plt.show()
