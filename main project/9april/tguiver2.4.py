import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import welch


class PSDPlotter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PSD Plotter")

        self.tab_control = ttk.Notebook(self)

        self.input_tab = ttk.Frame(self.tab_control)
        self.plot_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.input_tab, text="Input")
        self.tab_control.add(self.plot_tab, text="Plots")

        self.tab_control.pack(expand=1, fill="both")

        self.setup_input_tab()

    def setup_input_tab(self):
        self.input_frame = ttk.Frame(self.input_tab)

        self.load_button = ttk.Button(self.input_frame, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.plot_button = ttk.Button(self.input_frame, text="Plot PSD", command=self.plot_psd)
        self.plot_button.grid(row=1, column=0, padx=5, pady=5)

        self.csv_path_label = ttk.Label(self.input_frame, text="")
        self.csv_path_label.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.input_frame, text="Sampling Frequency (Hz):").grid(row=1, column=1, padx=5, pady=5)
        self.fs_input = ttk.Entry(self.input_frame)
        self.fs_input.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Sensitivity:").grid(row=2, column=1, padx=5, pady=5)
        self.sensitivity_input = ttk.Entry(self.input_frame)
        self.sensitivity_input.grid(row=2, column=2, padx=5, pady=5)

        self.input_frame.pack(padx=10, pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(title="Load CSV", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path_label.config(text=file_path)
            self.data = np.loadtxt(file_path, delimiter=',', skiprows=1)

    def plot_psd(self):
        try:
            fs = float(self.fs_input.get())
            sensitivity = float(self.sensitivity_input.get())

            fig, axes = plt.subplots(3, 1, figsize=(8, 6))

            for i in range(3):
                f, Pxx = welch(self.data[:, i], fs=fs)
                g_level = np.sqrt(np.trapz(Pxx, f)) / sensitivity
                axes[i].semilogy(f, Pxx / sensitivity**2, label='PSD')
                axes[i].axhline(y=g_level, color='r', linestyle='--', label='G-Level')
                axes[i].set_title(f'PSD - Direction {["X", "Y", "Z"][i]}')
                axes[i].set_xlabel('Frequency (Hz)')
                axes[i].set_ylabel('PSD')
                axes[i].legend()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_tab)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = PSDPlotter()
    app.geometry("800x600")
    app.mainloop()
