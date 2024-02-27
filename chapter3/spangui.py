import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")

        self.file_path = None
        self.df = None
        self.selected_range = None

        self.create_widgets()

    def create_widgets(self):
        # File Selection Button
        self.select_file_button = tk.Button(self.root, text="Select CSV File", command=self.load_file)
        self.select_file_button.pack(pady=10)

        # Plot Button
        self.plot_button = tk.Button(self.root, text="Plot PSD", command=self.plot_psd)
        self.plot_button.pack(pady=10)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Span Selector
        self.span_selector = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True,
                                          rectprops=dict(alpha=0.5, facecolor='red'))

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.file_path = file_path
            self.df = pd.read_csv(file_path)
            tk.messagebox.showinfo("File Loaded", "CSV file loaded successfully.")

    def plot_psd(self):
        if self.df is None:
            tk.messagebox.showerror("Error", "Please select a CSV file first.")
            return

        data = self.df.iloc[:, 1]  # Assuming the data is in the second column, change as needed
        fs = 1.0  # Adjust this value based on your data

        n = len(data)
        f, Pxx = self.calculate_psd(data, fs, n)

        self.ax.clear()
        self.ax.semilogy(f, Pxx)
        self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('Power/Frequency [dB/Hz]')
        self.ax.set_title('Power Spectral Density')

        self.canvas.draw()

    def calculate_psd(self, data, fs, n):
        fft_result = np.fft.fft(data)
        freq = np.fft.fftfreq(n, d=1/fs)
        Pxx = np.abs(fft_result)**2 / (fs * n)
        return freq[:n//2], Pxx[:n//2]

    def onselect(self, xmin, xmax):
        self.selected_range = (xmin, xmax)
        if self.selected_range:
            selected_data = self.get_data_within_range(self.selected_range)
            self.analyze_selected_data(selected_data)

    def get_data_within_range(self, selected_range):
        if self.df is not None:
            frequency_column = self.df.columns[0]
            data_column = self.df.columns[1]

            selected_data = self.df[(self.df[frequency_column] >= selected_range[0]) &
                                     (self.df[frequency_column] <= selected_range[1])]
            return selected_data
        else:
            return None

    def analyze_selected_data(self, selected_data):
        if selected_data is not None:
            # Perform further analysis on the selected data
            messagebox.showinfo("Selected Range", f"Selected range: {self.selected_range}\n\n"
                                                   f"Data within the selected range:\n{selected_data}")
        else:
            messagebox.showwarning("No Data", "No data available within the selected range.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
