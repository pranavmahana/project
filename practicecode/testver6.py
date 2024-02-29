import tkinter as tk
from tkinter import filedialog, messagebox, Entry, StringVar, OptionMenu, Scrollbar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import EngFormatter
from scipy.signal import welch
from PIL import Image
from docx import Document
from docx.shared import Inches
from io import BytesIO

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")

        # Set custom background color
        self.root.configure(bg="#f0f8ff")  # Light blue background

        self.file_path = None
        self.df = None
        self.selected_range = None
        self.sensitivity_var = tk.IntVar()
        self.sensitivity_var.set(0)  # Default: Sensitivity not provided

        self.window_type_var = tk.StringVar()
        self.window_type_var.set('hann')  # Default window type: Hann

        # Additional parameters for welch function
        self.nperseg_entry = Entry(self.root, width=10)
        self.nperseg_label = tk.Label(self.root, text="nperseg:", bg="#f0f8ff")

        self.noverlap_entry = Entry(self.root, width=10)
        self.noverlap_label = tk.Label(self.root, text="noverlap:", bg="#f0f8ff")

        self.nfft_entry = Entry(self.root, width=10)
        self.nfft_label = tk.Label(self.root, text="nfft:", bg="#f0f8ff")

        # Window type selection
        self.window_type_label = tk.Label(self.root, text="Window Type:", bg="#f0f8ff")
        self.window_type_entry = Entry(self.root, textvariable=self.window_type_var, width=10)
        self.window_type_label.pack()
        self.window_type_entry.pack()

        # Create a Canvas to hold all components
        self.canvas = tk.Canvas(self.root, bg="#f0f8ff")  # Light blue background
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar and attach it to the Canvas
        scrollbar = Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Create a Frame to hold all components within the Canvas
        self.frame = tk.Frame(self.canvas, bg="#f0f8ff")  # Light blue background
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Call the function to create widgets
        self.create_widgets()

        # Configure the Canvas to update the scroll region
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def create_widgets(self):
        # File Selection Button
        self.select_file_button = tk.Button(self.frame, text="Select CSV File", command=self.load_file, bg="#87ceeb")
        self.select_file_button.pack(pady=10)

        # Label to display file information
        self.file_info_label = tk.Label(self.frame, text="Selected File: ", bg="#f0f8ff")  # Light blue background
        self.file_info_label.pack()

        # Checkbox for sensitivity
        self.sensitivity_checkbox = tk.Checkbutton(self.frame, text="Enter Sensor Sensitivity", variable=self.sensitivity_var, command=self.toggle_sensitivity_entry, bg="#f0f8ff")
        self.sensitivity_checkbox.pack()

        # Entry for sensitivity
        self.sensitivity_label = tk.Label(self.frame, text="Enter Sensor Sensitivity (Hz/V): ", bg="#f0f8ff")
        self.sensitivity_label.pack()
        self.sensitivity_entry = Entry(self.frame, state="disabled")
        self.sensitivity_entry.pack()

        # Additional parameters for welch function
        self.nperseg_label.pack()
        self.nperseg_entry.pack()

        self.noverlap_label.pack()
        self.noverlap_entry.pack()

        self.nfft_label.pack()
        self.nfft_entry.pack()

        # Plot Button
        self.plot_button = tk.Button(self.frame, text="Plot PSD", command=self.plot_psd, bg="#87ceeb")
        self.plot_button.pack(pady=10)

        # Export Plot Button
        self.export_button = tk.Button(self.frame, text="Export Plot", command=self.export_plot, bg="#87ceeb")
        self.export_button.pack(pady=10)

        # Matplotlib Figure for G-Levels
        self.fig_glevels, self.ax_glevels = plt.subplots(figsize=(8, 6))
        self.canvas_glevels = FigureCanvasTkAgg(self.fig_glevels, master=self.frame)
        self.canvas_glevels.get_tk_widget().pack()

        # Span Selector for G-Levels
        self.span_selector_glevels = SpanSelector(self.ax_glevels, self.onselect_glevels, 'horizontal', useblit=True)

        # Matplotlib Figure for PSD
        self.fig_psd, self.ax_psd = plt.subplots(figsize=(8, 6))
        self.canvas_psd = FigureCanvasTkAgg(self.fig_psd, master=self.frame)
        self.canvas_psd.get_tk_widget().pack()

        # Span Selector for PSD
        self.span_selector_psd = SpanSelector(self.ax_psd, self.onselect_psd, 'horizontal', useblit=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.file_path = file_path
            self.df = pd.read_csv(file_path)
            self.file_info_label.config(text=f"Selected File: {file_path}")
            tk.messagebox.showinfo("File Loaded", "CSV file loaded successfully.")

    def plot_psd(self):
        if self.df is None:
            tk.messagebox.showerror("Error", "Please select a CSV file first.")
            return

        data = self.df.iloc[:, 1]  # Assuming the data is in the second column, change as needed
        fs = 1.0  # Adjust this value based on your data

        sensitivity = None
        if self.sensitivity_var.get() == 1:
            sensitivity_str = self.sensitivity_entry.get()
            try:
                sensitivity = float(sensitivity_str)
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid numeric value for sensitivity.")
                return

        n = len(data)

        # Get additional parameters for welch function
        try:
            nperseg = int(self.nperseg_entry.get())
            noverlap = int(self.noverlap_entry.get())
            nfft = int(self.nfft_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numeric values for welch parameters.")
            return

        window_type = self.window_type_var.get()

        f, Pxx = self.calculate_psd(data, fs, n, sensitivity, nperseg=nperseg, noverlap=noverlap, nfft=nfft, window_type=window_type)

        # Clear previous plots
        self.ax_psd.cla()

        # Plot PSD
        self.ax_psd.plot(f, Pxx)
        self.ax_psd.set_xlabel('Frequency (Hz)')
        self.ax_psd.set_ylabel('Power/Frequency (dB/Hz)')

        # Set y-axis to display engineering notation
        self.ax_psd.yaxis.set_major_formatter(EngFormatter(unit='dB'))

        # Adjust layout to prevent label cropping
        self.fig_psd.tight_layout()

        self.canvas_psd.draw()

    def calculate_psd(self, data, fs, n, sensitivity=None, nperseg=None, noverlap=None, nfft=None, window_type='hann'):
        f, Pxx = welch(data, fs, nperseg=nperseg, noverlap=noverlap, nfft=nfft, window=window_type)

        if sensitivity is not None:
            # Adjust PSD values based on sensitivity
            Pxx = 10 * np.log10(np.maximum(Pxx, np.finfo(float).tiny) / (sensitivity**2))
        else:
            # If sensitivity is not provided, use the original PSD values
            Pxx = 10 * np.log10(np.maximum(Pxx, np.finfo(float).tiny))

        return f, Pxx

    def onselect_psd(self, xmin, xmax):
        if xmin != xmax:
            self.plot_psd(xmin, xmax)

    def onselect_glevels(self, xmin, xmax):
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

    def toggle_sensitivity_entry(self):
        if self.sensitivity_var.get() == 1:
            self.sensitivity_entry.config(state="normal")
        else:
            self.sensitivity_entry.config(state="disabled")
            self.sensitivity_entry.delete(0, tk.END)  # Clear the entry

    def export_plot(self):
        if self.fig_psd:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg")])
            if file_path:
                self.fig_psd.savefig(file_path, format='jpeg', dpi=300, bbox_inches='tight')  # Adjusted to include tight bounding box
                tk.messagebox.showinfo("Export Successful", "Plot exported successfully.")
        else:
            tk.messagebox.showerror("Error", "Please plot the PSD before exporting.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
