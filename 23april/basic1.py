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
        tk.Label(self.input_frame, text="Sensitivity:").grid(row=0, column=0)
        tk.Entry(self.input_frame, textvariable=self.sensitivity).grid(row=0, column=1)

        # Sampling frequency input
        tk.Label(self.input_frame, text="Sampling Frequency:").grid(row=1, column=0)
        tk.Entry(self.input_frame, textvariable=self.sampling_frequency).grid(row=1, column=1)

        # Load CSV button
        tk.Button(self.input_frame, text="Load CSV", command=self.load_csv).grid(row=2, column=0, columnspan=2)

        # Plot button
        tk.Button(self.input_frame, text="Plot G-levels", command=self.plot_glevels).grid(row=3, column=0, columnspan=2)

        # Plots tab
        self.plots_frame = tk.Frame(self.notebook)
        self.notebook.add(self.plots_frame, text="Plots")

        # Canvas for plotting
        self.fig = plt.Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self.plots_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plots_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
            plt.xlabel("Time")
            plt.ylabel("G-levels")
            plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = VibrationAnalyzer(root)
    root.mainloop()
