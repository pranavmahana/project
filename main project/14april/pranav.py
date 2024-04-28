import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.widgets as widgets
import pandas as pd
from scipy.signal import welch

class GLevelPSDPlotterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("G-Level and PSD Plotter")
        self.geometry("800x600")
        
        self.sensitivity = tk.DoubleVar(value=1.0)
        self.sampling_frequency = tk.DoubleVar(value=100.0)
        self.time_data = None
        self.g_level_data = None
        self.selected_range = None
        
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
        
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def setup_input_tab(self):
        input_frame = ttk.LabelFrame(self.input_tab, text="Input Parameters")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(input_frame, text="Sensitivity:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.sensitivity).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Sampling Frequency:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(input_frame, textvariable=self.sampling_frequency).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Load CSV", command=self.load_csv).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
    def setup_glevels_tab(self):
        self.glevels_fig, self.glevels_ax = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
        self.canvas_glevels = FigureCanvasTkAgg(self.glevels_fig, master=self.glevels_tab)
        self.canvas_glevels.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas_glevels.mpl_connect('button_press_event', self.on_press)
        self.canvas_glevels.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas_glevels.mpl_connect('button_release_event', self.on_release)
        self.canvas_glevels.mpl_connect('scroll_event', self.on_zoom)

        self.toolbar_glevels = NavigationToolbar2Tk(self.canvas_glevels, self.glevels_tab)
        self.toolbar_glevels.update()
        self.toolbar_glevels.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(self.glevels_tab, text="Plot G-Levels", command=self.plot_glevels).pack()
        ttk.Button(self.glevels_tab, text="Plot PSD", command=self.plot_psd).pack()

    def on_press(self, event):
        if event.inaxes != self.glevels_ax[0]:
            return
        self.x0, self.y0 = event.xdata, event.ydata

    def on_motion(self, event):
        if event.inaxes != self.glevels_ax[0]:
            return
        self.x1, self.y1 = event.xdata, event.ydata
        self.glevels_ax[0].set_xlim(self.x0, self.x1)
        self.glevels_ax[0].set_ylim(self.y0, self.y1)
        self.canvas_glevels.draw()

    def on_release(self, event):
        if event.inaxes != self.glevels_ax[0]:
            return
        self.x1, self.y1 = event.xdata, event.ydata
        self.glevels_ax[0].set_xlim(self.x0, self.x1)
        self.glevels_ax[0].set_ylim(self.y0, self.y1)
        self.canvas_glevels.draw()

    def on_zoom(self, event):
        if event.inaxes != self.glevels_ax[0]:
            return
        scale_factor = 1.0 + (event.button == 'up') * 0.1 - (event.button == 'down') * 0.1
        self.glevels_ax[0].set_xlim(self.glevels_ax[0].get_xlim()[0] * scale_factor, self.glevels_ax[0].get_xlim()[1] * scale_factor)
        self.glevels_ax[0].set_ylim(self.glevels_ax[0].get_ylim()[0] * scale_factor, self.glevels_ax[0].get_ylim()[1] * scale_factor)
        self.canvas_glevels.draw()

    def setup_psd_plots_tab(self):
        self.psd_fig, self.psd_ax = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
        self.canvas_psd = FigureCanvasTkAgg(self.psd_fig, master=self.psd_plots_tab)
        self.canvas_psd.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar_psd = NavigationToolbar2Tk(self.canvas_psd, self.psd_plots_tab)
        self.toolbar_psd.update()
        self.toolbar_psd.pack(side=tk.TOP, fill=tk.X)

    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                data = pd.read_csv(filename)
                self.time_data = data.iloc[:, 0].values
                self.g_level_data = data.iloc[:, 1:].values
                messagebox.showinfo("Success", "CSV file loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading CSV file: {e}")

    def plot_glevels(self):
        if self.time_data is not None and self.g_level_data is not None:
            self.glevels_ax[0].clear()
            self.glevels_ax[1].clear()
            self.glevels_ax[2].clear()
            self.glevels_ax[0].plot(self.time_data, self.g_level_data[:, 0], label='X')
            self.glevels_ax[1].plot(self.time_data, self.g_level_data[:, 1], label='Y')
            self.glevels_ax[2].plot(self.time_data, self.g_level_data[:, 2], label='Z')
            for ax in self.glevels_ax:
                ax.legend()
            self.canvas_glevels.draw()
            self.tabControl.select(self.glevels_tab)
        else:
            messagebox.showwarning("Warning", "Please load CSV file first.")

    def plot_psd(self):
        if self.time_data is not None and self.g_level_data is not None:
            fs = self.sampling_frequency.get()
            for i in range(3):
                f, psd = welch(self.g_level_data[:, i], fs=fs)
                self.psd_ax[i].clear()
                self.psd_ax[i].semilogy(f, psd, label='PSD')
                self.psd_ax[i].set_xlabel('Frequency (Hz)')
                self.psd_ax[i].set_ylabel('PSD')
                self.psd_ax[i].legend()
            self.canvas_psd.draw()
            self.tabControl.select(self.psd_plots_tab)

    def on_tab_change(self, event):
        current_tab = event.widget.select()
        tab_text = event.widget.tab(event.widget.index("current"))['text']

        if tab_text == "G-Levels":
            self.plot_glevels()
        elif tab_text == "PSD Plots":
            self.plot_psd()

if __name__ == "__main__":
    app = GLevelPSDPlotterApp()
    app.mainloop()
