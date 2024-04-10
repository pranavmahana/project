import tkinter as tk
from tkinter import filedialog, messagebox, Entry
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import EngFormatter
from scipy.signal import welch
from PIL import Image

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")

        # Set custom background color
        self.root.configure(bg="#f0f8ff")  # Light blue background

        self.file_path = None
        self.df = None
        self.selected_range = None
        self.sensitivity = 24e3  # Default sensitivity in Hz/V

        self.create_widgets()

    def create_widgets(self):
        # File Selection Button
        self.select_file_button = tk.Button(self.root, text="Select CSV File", command=self.load_file, bg="#87ceeb")
        self.select_file_button.pack(pady=10)

        # Label to display file information
        self.file_info_label = tk.Label(self.root, text="Selected File: ", bg="#f0f8ff")  # Light blue background
        self.file_info_label.pack()

        # Entry for sensitivity
        self.sensitivity_label = tk.Label(self.root, text="Enter Sensor Sensitivity (Hz/V): ", bg="#f0f8ff")
        self.sensitivity_label.pack()
        self.sensitivity_entry = Entry(self.root)
        self.sensitivity_entry.insert(0, str(self.sensitivity))
        self.sensitivity_entry.pack()

        # Plot Button
        self.plot_button = tk.Button(self.root, text="Plot PSD", command=self.plot_psd, bg="#87ceeb")
        self.plot_button.pack(pady=10)

        # Export Plot Button
        self.export_button = tk.Button(self.root, text="Export Plot", command=self.export_plot, bg="#87ceeb")
        self.export_button.pack(pady=10)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Span Selector
        self.span_selector = SpanSelector(self.ax, self.onselect, 'horizontal', useblit=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.file_path = file_path
            self.df = pd.read_csv(file_path)
            self.file_info_label.config(text=f"Selected File: {file_path}")
            tk.messagebox.showinfo("File Loaded", "CSV file loaded successfully.")

    def plot_psd(self):
        sensitivity_str = self.sensitivity_entry.get()
        try:
            self.sensitivity = float(sensitivity_str)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid numeric value for sensitivity.")
            return

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

        # Set the formatter for the y-axis to display engineering notation
        self.ax.yaxis.set_major_formatter(EngFormatter(unit='dB'))

        self.canvas.draw()

    def calculate_psd(self, data, fs, n):
        f, Pxx = welch(data, fs, nperseg=1024)
        Pxx = 10 * np.log10(Pxx / (self.sensitivity**2))  # Convert to dB re: (Hz/V)^2
        return f, Pxx

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

    def export_plot(self):
        if self.fig:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg")])
            if file_path:
                self.fig.savefig(file_path, format='jpeg', dpi=300)
                tk.messagebox.showinfo("Export Successful", "Plot exported successfully.")
        else:
            tk.messagebox.showerror("Error", "Please plot the PSD before exporting.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
