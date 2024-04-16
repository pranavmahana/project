import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib as mlt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from scipy.signal import welch

class GLevelPSDPlotterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("G-Level and PSD Plotter")
        self.geometry("800x600")
        
        self.sensitivity = tk.DoubleVar(value=10.0)
        self.sampling_frequency = tk.DoubleVar(value=25000.0)
        self.time_data = None
        self.g_level_data = None
        self.selected_ranges = [None, None, None]
        self.filename = tk.StringVar()
        self.glevels_fig = plt.figure()  # Store the Figure object

        
        self.setup_tabs()
        self.setup_input_tab()
        self.setup_glevels_tab()
        self.setup_psd_plots_tab()
    
    def setup_tabs(self):
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=1, fill="both")
        
        self.input_tab = ttk.Frame(self.tabControl)
        self.glevels_tab = ttk.Frame(self.tabControl)
        self.psd_plots_tab = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.input_tab, text="Input")
        self.tabControl.add(self.glevels_tab, text="G-Levels")
        self.tabControl.add(self.psd_plots_tab, text="PSD Plots")
        
    def setup_input_tab(self):
        input_frame = ttk.LabelFrame(self.input_tab, text="Input Parameters")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(input_frame, text="Sensitivity:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.sensitivity).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Sampling Frequency:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.sampling_frequency).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Load CSV", command=self.load_csv).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.file_lable = ttk.Label(input_frame, text="Selected file: ",textvariable=self.filename).grid(row=2, column=3, padx=5, pady=5, sticky="e")
        ttk.Button(input_frame, text="Plot G-Levels", command=self.plot_glevels).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
    def setup_glevels_tab(self):
        glevels_frame = ttk.LabelFrame(self.glevels_tab, text="G-Levels")
        glevels_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        ttk.Label(glevels_frame, text="X G-Level Range (s):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.x_range_entry = ttk.Entry(glevels_frame)
        self.x_range_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(glevels_frame, text="Y G-Level Range (s):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.y_range_entry = ttk.Entry(glevels_frame)
        self.y_range_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(glevels_frame, text="Z G-Level Range (s):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.z_range_entry = ttk.Entry(glevels_frame)
        self.z_range_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(glevels_frame, text="Plot PSD", command=self.plot_psd).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
    def setup_psd_plots_tab(self):
        self.psd_fig, self.psd_ax = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
        self.canvas_psd = FigureCanvasTkAgg(self.psd_fig, master=self.psd_plots_tab)
        self.canvas_psd.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                data = pd.read_csv(filename)
                self.time_data = data.iloc[:, 0].values
                self.g_level_data = data.iloc[:, 1:].values
                messagebox.showinfo("Success", "CSV file loaded successfully.")
                self.filename.set(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading CSV file: {e}")
    
    def plot_glevels(self):
        if self.time_data is not None and self.g_level_data is not None:
            glevels_ax = self.glevels_fig.subplots(3, 1, figsize=(8, 6), sharex=True)
            glevels_ax[0].plot(self.time_data, self.g_level_data[:, 0], label='X')
            glevels_ax[1].plot(self.time_data, self.g_level_data[:, 1], label='Y')
            glevels_ax[2].plot(self.time_data, self.g_level_data[:, 2], label='Z')
            for ax in glevels_ax:
                ax.legend()
            self.canvas_glevels.draw()
            self.tabControl.select(self.glevels_tab)
        else:
            messagebox.showwarning("Warning", "Please load CSV file first.")
    
    def plot_psd(self):
        if self.time_data is not None and self.g_level_data is not None:
            fs = self.sampling_frequency.get()
            ranges = [self.parse_range(entry.get()) for entry in [self.x_range_entry, self.y_range_entry, self.z_range_entry]]
            for i, r in enumerate(ranges):
                if r is None:
                    ranges[i] = [self.time_data[0], self.time_data[-1]]
            for i in range(3):
                start, end = ranges[i]
                selected_time = self.time_data[(self.time_data >= start) & (self.time_data <= end)]
                selected_data = self.g_level_data[(self.time_data >= start) & (self.time_data <= end), i]
                f, psd = welch(selected_data, fs=fs)
                self.psd_ax[i].clear()
                self.psd_ax[i].semilogy(f, psd, label='PSD')
                self.psd_ax[i].set_xlabel('Frequency (Hz)')
                self.psd_ax[i].set_ylabel('PSD')
                self.psd_ax[i].legend()
            self.canvas_psd.draw()
            self.tabControl.select(self.psd_plots_tab)
        else:
            messagebox.showwarning("Warning", "Please load CSV file first.")
    
    def parse_range(self, range_str):
        try:
            start, end = map(float, range_str.split(','))
            return [start, end]
        except ValueError:
            return None

if __name__ == "__main__":
    app = GLevelPSDPlotterApp()
    app.mainloop()
