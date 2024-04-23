import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.signal import welch

class GLevelAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("G-Level Analyzer")

        self.tab_control = ttk.Notebook(self.root)
        self.tab_input = ttk.Frame(self.tab_control)
        self.tab_plot = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_input, text="Input")
        self.tab_control.add(self.tab_plot, text="Plot")

        self.tab_control.pack(expand=1, fill="both")

        self.create_input_tab()
        self.create_plot_tab()

    def create_input_tab(self):
        self.lbl_sampling_freq = tk.Label(self.tab_input, text="Sampling Frequency:")
        self.lbl_sampling_freq.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_sampling_freq = tk.Entry(self.tab_input)
        self.entry_sampling_freq.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_sensitivity = tk.Label(self.tab_input, text="Sensitivity:")
        self.lbl_sensitivity.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_sensitivity = tk.Entry(self.tab_input)
        self.entry_sensitivity.grid(row=1, column=1, padx=5, pady=5)

        self.btn_load_csv = tk.Button(self.tab_input, text="Load CSV", command=self.load_csv)
        self.btn_load_csv.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.btn_plot_glevel = tk.Button(self.tab_input, text="Plot G-Level", command=self.plot_glevel)
        self.btn_plot_glevel.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_plot_tab(self):
        self.fig, self.ax = plt.subplots(3, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_plot)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tab_plot)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH)
    
        self.time_ranges = [(None, None) for _ in range(3)]  # Initialize time ranges for each axis
    
        for i, axis in enumerate(['X', 'Y', 'Z']):
            frame = ttk.Frame(self.tab_plot)
            frame.pack(fill=tk.BOTH, expand=True)
    
            lbl = tk.Label(frame, text=f"Time Range for {axis}-Axis:")
            lbl.pack(side=tk.LEFT, padx=5, pady=5)
    
            self.time_range_entries = (
                tk.Entry(frame, width=10),
                tk.Entry(frame, width=10)
            )
            self.time_range_entries[0].pack(side=tk.LEFT, padx=5, pady=5)
            self.time_range_entries[1].pack(side=tk.LEFT, padx=5, pady=5)
    
        plot_glevel_btn = tk.Button(frame, text=f"Plot PSD for {axis}-Axis", command=lambda idx=i: self.plot_psd(idx))
        plot_glevel_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)

    def plot_glevel(self):
        if hasattr(self, 'df'):
            try:
                sampling_freq = float(self.entry_sampling_freq.get())
                sensitivity = float(self.entry_sensitivity.get())

                time = self.df.iloc[:, 0]
                x_glevel = self.df.iloc[:, 1] * sensitivity
                y_glevel = self.df.iloc[:, 2] * sensitivity
                z_glevel = self.df.iloc[:, 3] * sensitivity

                for i, axis_data in enumerate([(x_glevel, 'X'), (y_glevel, 'Y'), (z_glevel, 'Z')]):
                    ax = self.ax[i]
                    ax.clear()
                    ax.plot(time, axis_data[0], color='b', linestyle='-', label=f'{axis_data[1]}-Axis')
                    ax.set_title(f"{axis_data[1]}-Axis G-Level")
                    ax.set_xlabel("Time")
                    ax.set_ylabel("G-Level")
                    ax.set_yscale('log')

                    # Set time range if provided
                    start_time, end_time = self.time_ranges[i]
                    if start_time is not None and end_time is not None:
                        ax.set_xlim(start_time, end_time)

                    ax.legend()

                self.fig.tight_layout()
                self.canvas.draw()

            except ValueError:
                messagebox.showerror("Error", "Invalid input for sampling frequency or sensitivity.")

        else:
            messagebox.showerror("Error", "Please load a CSV file first.")

    def plot_psd(self, axis_idx):
        if hasattr(self, 'df'):
            try:
                sampling_freq = float(self.entry_sampling_freq.get())
                sensitivity = float(self.entry_sensitivity.get())
                axis_names = ['X', 'Y', 'Z']

                time = self.df.iloc[:, 0]
                axis_data = self.df.iloc[:, axis_idx + 1] * sensitivity

                # Get time range for selected axis
                start_time, end_time = self.time_ranges[axis_idx]
                if start_time is None or end_time is None:
                    messagebox.showerror("Error", f"Please specify time range for {axis_names[axis_idx]}-Axis plot.")
                    return

                # Select data within the specified time range
                mask = (time >= start_time) & (time <= end_time)
                selected_data = axis_data[mask]

                # Compute PSD using Welch's method
                f, Pxx = welch(selected_data, fs=sampling_freq)

                # Plot PSD
                plt.figure()
                plt.plot(f, Pxx, color='b', linestyle='-')
                plt.title(f"PSD for {axis_names[axis_idx]}-Axis")
                plt.xlabel("Frequency (Hz)")
                plt.ylabel("Power/Frequency")
                plt.grid(True)
                plt.show()

            except ValueError:
                messagebox.showerror("Error", "Invalid input for sampling frequency or sensitivity.")

        else:
            messagebox.showerror("Error", "Please load a CSV file first.")

def main():
    root = tk.Tk()
    app = GLevelAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
