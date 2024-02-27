import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import welch

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")

        self.file_path = None
        self.df = None

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

        f, Pxx = welch(data, fs, nperseg=1024)
        
        self.ax.clear()
        self.ax.semilogy(f, Pxx)
        self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('Power/Frequency [dB/Hz]')
        self.ax.set_title('Power Spectral Density')

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
