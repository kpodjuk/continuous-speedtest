import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import argparse


# Function to read the CSV file and return a DataFrame
def read_csv(file_path):
    return pd.read_csv(file_path, parse_dates=["timestamp"])


# Function to create and update the plot
def update_plot(df):
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Download Speed", "Upload Speed", "Ping"),
    )

    # Plot Download Speed
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["download"],
            mode="lines+markers",
            name="Download Speed",
        ),
        row=1,
        col=1,
    )

    # Plot Upload Speed
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["upload"], mode="lines+markers", name="Upload Speed"
        ),
        row=2,
        col=1,
    )

    # Plot Ping
    fig.add_trace(
        go.Scatter(x=df["timestamp"], y=df["ping"], mode="lines+markers", name="Ping"),
        row=3,
        col=1,
    )

    # Update layout
    fig.update_layout(title="Internet Speed Test Results", height=800, showlegend=True)
    fig.update_xaxes(title_text="Timestamp", row=3, col=1)
    fig.update_yaxes(title_text="Download Speed (Mbps)", row=1, col=1)
    fig.update_yaxes(title_text="Upload Speed (Mbps)", row=2, col=1)
    fig.update_yaxes(title_text="Ping (ms)", row=3, col=1)

    fig.show()


# Main function to monitor the CSV file for updates and refresh the plot
def main(file_path):
    # Read the initial data
    df = read_csv(file_path)
    update_plot(df)

    # Monitor the CSV file for updates
    while True:
        time.sleep(10)  # Check for updates every 10 seconds
        new_df = read_csv(file_path)
        if not new_df.equals(df):
            df = new_df
            update_plot(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CSV data dynamically.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    main(args.file_path)
