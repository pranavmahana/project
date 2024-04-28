import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


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

        # Plot button
        tk.Button(self.input_frame, text="Plot G-levels", command=self.plot_glevels).pack(side="left")

        # Plots tab
        self.plots_frame = tk.Frame(self.notebook)
        self.notebook.add(self.plots_frame, text="Plots")

        # Canvas for plotting
        self.fig = plt.Figure(figsize=(12, 12))
        self.canvas = FigureCanvasTkAgg(self.fig, self.plots_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plots_frame)
        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")

        # Plot click event
        self.fig.canvas.mpl_connect('button_press_event', self.on_plot_click)

        # Store plot index for zooming
        self.plot_index = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

    def plot_glevels(self):
        if hasattr(self, 'data'):
            num_channels = len(self.data.columns) - 1  # Exclude time column
            num_plots = min(num_channels, 24)

            # Clear previous plots
            self.fig.clf()

            # Plot small images of G-levels
            for i in range(num_plots):
                channel = self.data.columns[i + 1]  # Exclude time column
                ax = self.fig.add_subplot(4, 6, i + 1)
                ax.plot(self.data.iloc[:, 0], self.data.iloc[:, i + 1] / self.sensitivity.get())
                ax.set_title(channel)
                ax.set_ylim(bottom=0)  # Ensure non-negative values
                ax.set_xlabel("Time (s)")  # Label x-axis
                ax.set_ylabel("G-levels")  # Label y-axis
                ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
                ax.tick_params(axis='both', which='major', pad=5)  # Increase padding between ticks

            self.canvas.draw()

            # Switch to the Plots tab
            self.notebook.select(self.plots_frame)

    def on_plot_click(self, event):
        if event.inaxes:
            for i, ax in enumerate(self.fig.axes):
                if ax == event.inaxes:
                    self.plot_index = i
                    break

            if self.plot_index is not None:
                self.zoom_plot()

    def zoom_plot(self):
        if self.plot_index is not None:
            plt.figure()
            channel = self.data.columns[self.plot_index + 1]  # Exclude time column
            plt.plot(self.data.iloc[:, 0], self.data.iloc[:, self.plot_index + 1] / self.sensitivity.get())
            plt.title(channel)
            plt.xlabel("Time (s)")
            plt.ylabel("G-levels")
            plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = VibrationAnalyzer(root)
    root.mainloop()
