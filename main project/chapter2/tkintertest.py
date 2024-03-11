import tkinter as tk
import tkinter.filedialog as filedialog
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt

root = tk.Tk()

# Function to load CSV data
def load_data():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    data = np.loadtxt(filename, delimiter=",")
    return data

# Function to plot PSD
def plot_psd():
    global fs  # Declare fs as global to access its value

    nperseg = int(nperseg_entry.get())
    noverlap = int(noverlap_entry.get())
    window = window_entry.get()

    data = load_data()
    f, Pxx = welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap, window=window)

    plt.figure(figsize=(8, 5))
    plt.plot(f, Pxx)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSD (dB/Hz)")
    plt.title("Power Spectral Density (Welch's Method)")
    plt.grid(True)
    plt.show()

# Initial sampling rate (modify as needed)
fs = 1000  # Example value, replace with user input or default

# GUI elements
fs_label = tk.Label(root, text="Sampling Frequency (Hz):")
fs_entry = tk.Entry(root)  # Commented out as fs is set initially
nperseg_label = tk.Label(root, text="Number of Points per Segment:")
nperseg_entry = tk.Entry(root)
noverlap_label = tk.Label(root, text="Number of Overlapping Points:")
noverlap_entry = tk.Entry(root)
window_label = tk.Label(root, text="Window Function:")
window_entry = tk.Entry(root)
plot_button = tk.Button(root, text="Plot PSD", command=plot_psd)

# Arrange elements
fs_label.pack()
# fs_entry.pack()  # Commented out as fs is set initially
nperseg_label.pack()
nperseg_entry.pack()
noverlap_label.pack()
noverlap_entry.pack()
window_label.pack()
window_entry.pack()
plot_button.pack()

root.mainloop()
