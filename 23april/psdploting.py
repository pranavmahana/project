import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy.signal import welch


class VibrationAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Vibration Analyzer")

        # Variables to store user input
        self.sensitivity = tk.DoubleVar(value=10)
        self.sampling_frequency = tk.DoubleVar(value=25000)

        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Input tab
        self.input_frame = tk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="Input")

        # Sensitivity input
        tk.Label(self.input_frame, text="Sensitivity:").pack(side="left")
        tk.Entry(self.input_frame, textvariable=self.sensitivity).pack(side="left")

        # Sampling frequency input
        tk.Label(self.input_frame, text="Sampling Frequency:").pack(side="left")
        tk.Entry(self.input_frame, textvariable=self.sampling_frequency).pack(side="left")

        # Load CSV button
        tk.Button(self.input_frame, text="Load CSV", command=self.load_csv).pack(side="left")

        # Plot G-levels button
        tk.Button(self.input_frame, text="Plot G-levels", command=self.plot_glevels).pack(side="left")

        # G-level plots tab
        self.glevel_plots_frame = tk.Frame(self.notebook)
        self.notebook.add(self.glevel_plots_frame, text="G-level Plots")

        # Plot PSD button
        tk.Button(self.glevel_plots_frame, text="Plot PSD", command=self.plot_psd).pack(side="top")

        # Canvas for plotting G-levels
        self.glevel_fig = plt.Figure(figsize=(14, 10))
        self.glevel_canvas = FigureCanvasTkAgg(self.glevel_fig, self.glevel_plots_frame)
        self.glevel_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Toolbar for G-level plots
        self.glevel_toolbar = NavigationToolbar2Tk(self.glevel_canvas, self.glevel_plots_frame)
        self.glevel_toolbar.update()
        self.glevel_toolbar.pack(side="bottom", fill="x")

        # Plot click event for G-level plots
        self.glevel_fig.canvas.mpl_connect('button_press_event', self.on_glevel_plot_click)

        # Store plot index for zooming G-level plots
        self.glevel_plot_index = None

        # PSD plots tab
        self.psd_plots_frame = tk.Frame(self.notebook)
        self.notebook.add(self.psd_plots_frame, text="PSD Plots")

        # Canvas for plotting PSD
        self.psd_fig = plt.Figure(figsize=(14, 10))
        self.psd_canvas = FigureCanvasTkAgg(self.psd_fig, self.psd_plots_frame)
        self.psd_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Toolbar for PSD plots
        self.psd_toolbar = NavigationToolbar2Tk(self.psd_canvas, self.psd_plots_frame)
        self.psd_toolbar.update()
        self.psd_toolbar.pack(side="bottom", fill="x")

        # Plot click event for PSD plots
        self.psd_fig.canvas.mpl_connect('button_press_event', self.on_psd_plot_click)

        # Store plot index for zooming PSD plots
        self.psd_plot_index = None

        # G-levels DataFrame
        self.data = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

    def plot_glevels(self):
        if self.data is not None:
            num_channels = len(self.data.columns) - 1  # Exclude time column
            num_plots = min(num_channels, 24)

            # Calculate number of rows and columns
            num_rows = (num_plots - 1) // 6 + 1
            num_cols = min(num_plots, 6)

            # Clear previous plots
            self.glevel_fig.clf()

            # Plot small images of G-levels
            for i in range(num_plots):
                channel = self.data.columns[i + 1]  # Exclude time column
                ax = self.glevel_fig.add_subplot(num_rows, num_cols, i + 1)
                ax.plot(self.data.iloc[:, 0], self.data.iloc[:, i + 1] / self.sensitivity.get())
                ax.set_title(channel, fontsize=8)

                # Calculate y-axis limit dynamically based on the maximum value of G-levels
                max_glevel = max(self.data.iloc[:, i + 1] / self.sensitivity.get())
                ax.set_ylim(0, max_glevel * 1.2)  # Add 20% padding

                ax.set_xlabel("Time (s)", fontsize=10)  # Label x-axis with larger font size
                ax.set_ylabel("G-levels", fontsize=8)  # Label y-axis
                ax.tick_params(axis='x', rotation=45, labelsize=8)  # Rotate x-axis labels for better readability
                ax.tick_params(axis='both', which='major', pad=2)  # Increase padding between ticks

            # Adjust spacing between plot frames
            self.glevel_fig.subplots_adjust(hspace=1, wspace=0.5, top=0.95)

            self.glevel_canvas.draw()

            # Switch to the G-level Plots tab
            self.notebook.select(self.glevel_plots_frame)

    def on_glevel_plot_click(self, event):
        if event.inaxes:
            for i, ax in enumerate(self.glevel_fig.axes):
                if ax == event.inaxes:
                    self.glevel_plot_index = i
                    break

            if self.glevel_plot_index is not None:
                self.zoom_glevel_plot()

    def zoom_glevel_plot(self):
        if self.glevel_plot_index is not None:
            plt.figure()
            channel = self.data.columns[self.glevel_plot_index + 1]  # Exclude time column
            plt.plot(self.data.iloc[:, 0], self.data.iloc[:, self.glevel_plot_index + 1] / self.sensitivity.get())
            plt.title(channel)
            plt.xlabel("Time (s)")
            plt.ylabel("G-levels")
            plt.show()

    def plot_psd(self):
        if self.data is not None:
            num_channels = len(self.data.columns) - 1  # Exclude time column
            num_plots = min(num_channels, 24)

            # Calculate number of rows and columns
            num_rows = (num_plots - 1) // 6 + 1
            num_cols = min(num_plots, 6)

            # Clear previous plots
            self.psd_fig.clf()

            # Plot small images of PSD
            for i in range(num_plots):
                channel = self.data.columns[i + 1]  # Exclude time column
                ax = self.psd_fig.add_subplot(num_rows, num_cols, i + 1)

                # Calculate PSD using Welch method
                f, Pxx = welch(self.data.iloc[:, i + 1], fs=self.sampling_frequency.get())

                ax.semilogy(f, Pxx)
                ax.set_title(channel, fontsize=8)
                ax.set_xlabel("Frequency (Hz)", fontsize=8)
                ax.set_ylabel("PSD", fontsize=8)

            # Adjust spacing between plot frames
            self.psd_fig.subplots_adjust(hspace=1, wspace=0.5, top=0.95)

            self.psd_canvas.draw()

            # Switch to the PSD Plots tab
            self.notebook.select(self.psd_plots_frame)

    def on_psd_plot_click(self, event):
        if event.inaxes:
            for i, ax in enumerate(self.psd_fig.axes):
                if ax == event.inaxes:
                    self.psd_plot_index = i
                    break

            if self.psd_plot_index is not None:
                self.zoom_psd_plot()

    def zoom_psd_plot(self):
        if self.psd_plot_index is not None:
            plt.figure()
            channel = self.data.columns[self.psd_plot_index + 1]  # Exclude time column

            # Calculate PSD using Welch method
            f, Pxx = welch(self.data.iloc[:, self.psd_plot_index + 1], fs=self.sampling_frequency.get())

            plt.semilogy(f, Pxx)
            plt.title(channel)
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("PSD")
            plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = VibrationAnalyzer(root)
    root.mainloop()
