
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os

class DynamicPlot:

    def __init__(self):
        self.fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=("Download Speed", "Upload Speed", "Ping"),
        )
        self.trace_download = go.Scatter(x=[], y=[], mode="lines+markers", name="Download Speed")
        self.trace_upload = go.Scatter(x=[], y=[], mode="lines+markers", name="Upload Speed")
        self.trace_ping = go.Scatter(x=[], y=[], mode="lines+markers", name="Ping")
        
        self.fig.add_trace(self.trace_download, row=1, col=1)
        self.fig.add_trace(self.trace_upload, row=2, col=1)
        self.fig.add_trace(self.trace_ping, row=3, col=1)
        
        self.fig.update_layout(title="Internet Speed Test Results", height=800, showlegend=True)
        self.fig.update_xaxes(title_text="Timestamp", row=3, col=1)
        self.fig.update_yaxes(title_text="Download Speed (Mbps)", row=1, col=1)
        self.fig.update_yaxes(title_text="Upload Speed (Mbps)", row=2, col=1)
        self.fig.update_yaxes(title_text="Ping (ms)", row=3, col=1)
        
        self.df = pd.DataFrame()

    def read_csv(self, file_path):
        try:
            return pd.read_csv(file_path, parse_dates=["timestamp"])
        except Exception as e:
            print(f"Error reading the file: {e}")
            return pd.DataFrame()

    def update_plot(self, new_data):
        self.df = pd.concat([self.df, new_data]).drop_duplicates().reset_index(drop=True)

        self.fig.data[0].x = self.df["timestamp"]
        self.fig.data[0].y = self.df["download"]
        
        self.fig.data[1].x = self.df["timestamp"]
        self.fig.data[1].y = self.df["upload"]
        
        self.fig.data[2].x = self.df["timestamp"]
        self.fig.data[2].y = self.df["ping"]
        
        self.fig.show()

    def main(self, file_path):
        self.df = self.read_csv(file_path)
        self.update_plot(self.df)

        # Monitor the CSV file for updates
        while True:
            time.sleep(10)  # Check for updates every 10 seconds
            new_df = self.read_csv(file_path)
            if not new_df.equals(self.df) and not new_df.empty:
                new_data = new_df[~new_df.isin(self.df.to_dict('l')).all(1)]
                self.update_plot(new_data)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Plot CSV data dynamically.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print(f"File {args.file_path} does not exist.")
    else:
        dp = DynamicPlot()
        dp.main(args.file_path)
