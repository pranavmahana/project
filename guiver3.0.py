import tkinter as tk
from tkinter import filedialog, ttk
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

def plot_glevel(ax, x, sensitivity, title):
    g_levels = x / sensitivity
    ax.plot(g_levels)
    ax.set_xlabel('Time')
    ax.set_ylabel('g-levels')
    ax.set_title(title)

def plot_psd(ax, x, fs, nperseg, noverlap, nfft, title):
    f, Pxx = welch(x, fs=fs, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
    ax.semilogy(f, Pxx)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title(title)

class PSDPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSD Plotter")
        self.root.attributes('-zoomed', True)  # Maximize the window (not fullscreen)

        # Colorful style
        style = ttk.Style()
        style.configure("TFrame", background="#ececec")
        style.configure("TButton", background="#b1d3f3", font=("Arial", 10))
        style.configure("TLabel", background="#ececec", font=("Arial", 10))

        self.file_path_label = ttk.Label(root, text="Select CSV File:")
        self.file_path_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.file_path_entry = ttk.Entry(root, state="disabled", width=40)
        self.file_path_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, pady=5, padx=10, sticky="w")

        self.param_label = ttk.Label(root, text="Enter Welch Parameters:")
        self.param_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        self.fs_label = ttk.Label(root, text="Sampling Frequency (Hz):")
        self.fs_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.fs_entry = ttk.Entry(root)
        self.fs_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        self.nperseg_label = ttk.Label(root, text="Segment Length:")
        self.nperseg_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.nperseg_entry = ttk.Entry(root)
        self.nperseg_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        self.noverlap_label = ttk.Label(root, text="Overlap:")
        self.noverlap_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")
        self.noverlap_entry = ttk.Entry(root)
        self.noverlap_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        self.nfft_label = ttk.Label(root, text="Number of FFT Points:")
        self.nfft_label.grid(row=5, column=0, pady=5, padx=10, sticky="w")
        self.nfft_entry = ttk.Entry(root)
        self.nfft_entry.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        self.sensitivity_label = ttk.Label(root, text="Sensitivity of the Sensor:")
        self.sensitivity_label.grid(row=6, column=0, pady=5, padx=10, sticky="w")
        self.sensitivity_entry = ttk.Entry(root)
        self.sensitivity_entry.grid(row=6, column=1, pady=5, padx=10, sticky="w")

        self.plot_glevel_button = ttk.Button(root, text="Plot G-levels", command=self.plot_glevels)
        self.plot_glevel_button.grid(row=7, column=0, pady=10, padx=10, sticky="w")

        self.plot_psd_button = ttk.Button(root, text="Plot PSD", command=self.plot_psd)
        self.plot_psd_button.grid(row=7, column=1, pady=10, padx=10, sticky="w")

        # Vertical scrollbar for the canvas
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.grid(row=8, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#ececec")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig, self.axs = plt.subplots(2, 3, figsize=(15, 10))
        self.fig.subplots_adjust(wspace=0.5, hspace=0.5)  # Adjust the space between subplots
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path_entry.config(state="normal")
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)
        self.file_path_entry.config(state="disabled")

    def plot_glevels(self):
        file_path = self.file_path_entry.get()
        sensitivity = float(self.sensitivity_entry.get())

        data = read_csv(file_path)

        if data is not None:
            for i in range(3):
                column_index = i + 1
                x = data.iloc[:, column_index].values

                # Plot g-levels
                plot_glevel(self.axs[0, i], x, sensitivity, f'G-levels Plot {i + 1}')

            self.canvas_widget.draw()

    def plot_psd(self):
        file_path = self.file_path_entry.get()
        fs = float(self.fs_entry.get())
        nperseg = int(self.nperseg_entry.get())
        noverlap = int(self.noverlap_entry.get())
        nfft = int(self.nfft_entry.get())

        data = read_csv(file_path)

        if data is not None:
            for i in range(3):
                column_index = i + 1
                x = data.iloc[:, column_index].values

                # Plot PSD
                plot_psd(self.axs[1, i], x, fs, nperseg, noverlap, nfft, f'PSD Plot {i + 1}')

            self.canvas_widget.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PSDPlotterApp(root)
    root.mainloop()
