import tkinter as tk
from tkinter import filedialog
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_psd():
   csv_file = file_path.get()
   fs = int(fs_entry.get())
   nperseg = int(nperseg_entry.get())
   noverlap = int(noverlap_entry.get())

   try:
       data = pd.read_csv(csv_file, header=None)[0].values  # Assuming voltages in first column
       f, Pxx = signal.welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap)

       fig, ax = plt.subplots()
       ax.plot(f, Pxx)
       ax.set_xlabel('Frequency (Hz)')
       ax.set_ylabel('Power Spectral Density (V^2/Hz)')
       ax.set_title('PSD from CSV Data')

       canvas.draw()

   except FileNotFoundError:
       error_label.config(text="File not found. Please select a valid CSV file.")
   except ValueError:
       error_label.config(text="Invalid input for arguments. Please enter integers.")
   except Exception as e:
       error_label.config(text=f"An error occurred: {e}")

root = tk.Tk()
root.title("PSD Plotter")

# Input fields for arguments
fs_label = tk.Label(root, text="Sampling Frequency (Hz):")
fs_label.grid(row=0, column=0)
fs_entry = tk.Entry(root)
fs_entry.grid(row=0, column=1)

nperseg_label = tk.Label(root, text="Number of Points per Segment:")
nperseg_label.grid(row=1, column=0)
nperseg_entry = tk.Entry(root)
nperseg_entry.grid(row=1, column=1)

noverlap_label = tk.Label(root, text="Number of Overlapping Points:")
noverlap_label.grid(row=2, column=0)
noverlap_entry = tk.Entry(root)
noverlap_entry.grid(row=2, column=1)

# File selection button
file_button = tk.Button(root, text="Select CSV File", command=lambda: file_path.set(filedialog.askopenfilename()))
file_button.grid(row=3, column=0, columnspan=2)
file_path = tk.StringVar()

# Error message label
error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=4, column=0, columnspan=2)

# Plot button
plot_button = tk.Button(root, text="Plot PSD", command=plot_psd)
plot_button.grid(row=5, column=0, columnspan=2)

# Figure and canvas for plotting
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)

root.mainloop()
