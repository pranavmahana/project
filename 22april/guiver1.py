import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


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
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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
    
                self.ax[0].clear()
                self.ax[0].plot(time, x_glevel, color='b', linestyle='-', label='X-Axis')
                self.ax[0].set_title("X-Axis G-Level")
                self.ax[0].set_xlabel("Time")
                self.ax[0].set_ylabel("Log(G-Level)")
                self.ax[0].set_yscale('log')
    
                self.ax[1].clear()
                self.ax[1].plot(time, y_glevel, color='r', linestyle='--', label='Y-Axis')
                self.ax[1].set_title("Y-Axis G-Level")
                self.ax[1].set_xlabel("Time")
                self.ax[1].set_ylabel("Log(G-Level)")
                self.ax[1].set_yscale('log')
    
                self.ax[2].clear()
                self.ax[2].plot(time, z_glevel, color='g', linestyle='-.', label='Z-Axis')
                self.ax[2].set_title("Z-Axis G-Level")
                self.ax[2].set_xlabel("Time")
                self.ax[2].set_ylabel("Log(G-Level)")
                self.ax[2].set_yscale('log')
    
                for ax in self.ax:
                    ax.legend()
    
                self.fig.tight_layout()
                self.canvas.draw()
    
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid input for sampling frequency or sensitivity.")
    
        else:
            tk.messagebox.showerror("Error", "Please load a CSV file first.")


def main():
    root = tk.Tk()
    app = GLevelAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
