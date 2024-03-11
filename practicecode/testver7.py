import tkinter as tk
from tkinter import filedialog
import pandas as pd
from scipy.signal import welch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def plot_psd(ax, x, fs, nperseg, noverlap, nfft):
    f, Pxx = welch(x, fs=fs, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
    ax.semilogy(f, Pxx)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title('Power Spectral Density')

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")

        self.file_path_label = tk.Label(root, text="Select CSV File:")
        self.file_path_label.pack()

        self.file_path_entry = tk.Entry(root, state="disabled", width=40)
        self.file_path_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.param_label = tk.Label(root, text="Enter Welch Parameters:")
        self.param_label.pack()

        self.fs_label = tk.Label(root, text="Sampling Frequency (Hz):")
        self.fs_label.pack()
        self.fs_entry = tk.Entry(root)
        self.fs_entry.pack()

        self.nperseg_label = tk.Label(root, text="Segment Length:")
        self.nperseg_label.pack()
        self.nperseg_entry = tk.Entry(root)
        self.nperseg_entry.pack()

        self.noverlap_label = tk.Label(root, text="Overlap:")
        self.noverlap_label.pack()
        self.noverlap_entry = tk.Entry(root)
        self.noverlap_entry.pack()

        self.nfft_label = tk.Label(root, text="Number of FFT Points:")
        self.nfft_label.pack()
        self.nfft_entry = tk.Entry(root)
        self.nfft_entry.pack()

        self.plot_button = tk.Button(root, text="Plot PSD", command=self.plot_psd)
        self.plot_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path_entry.config(state="normal")
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)
        self.file_path_entry.config(state="disabled")

    def plot_psd(self):
        file_path = self.file_path_entry.get()
        fs = float(self.fs_entry.get())
        nperseg = int(self.nperseg_entry.get())
        noverlap = int(self.noverlap_entry.get())
        nfft = int(self.nfft_entry.get())

        data = read_csv(file_path)

        if data is not None:
            fig, axs = plt.subplots(3, 1, figsize=(10, 12))

            for i in range(3):
                column_index = i + 1
                x = data.iloc[:, column_index].values
                plot_psd(axs[i], x, fs, nperseg, noverlap, nfft)

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
