import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTabWidget, QLabel, QLineEdit, QFormLayout, QComboBox, QSizePolicy
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import welch


class PSDPlotter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.axes = plt.subplots(4, 1, figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.selected_frame = None
        self.g_levels = None
        self.fs = None
        self.sensitivity = None

    def plot_g_levels(self, data, fs, sensitivity):
        self.fs = fs
        self.sensitivity = sensitivity

        # Compute g-levels
        self.g_levels = np.sqrt(np.sum(data**2, axis=1)) / sensitivity

        # Plot g-levels
        self.axes[0].clear()
        self.axes[0].plot(np.arange(len(self.g_levels)) / fs, self.g_levels, color='blue')
        self.axes[0].set_title('G-Levels')
        self.axes[0].set_xlabel('Time (s)')
        self.axes[0].set_ylabel('G-Levels')

        self.canvas.draw()

    def plot_psd(self, data, start_time, end_time):
        if self.g_levels is None or self.fs is None or self.sensitivity is None:
            return

        start_index = int(start_time * self.fs)
        end_index = int(end_time * self.fs)

        selected_data = data[start_index:end_index, :]

        for i in range(3):
            f, Pxx = welch(selected_data[:, i], fs=self.fs)
            self.axes[i+1].clear()
            self.axes[i+1].semilogy(f, Pxx / self.sensitivity**2)
            self.axes[i+1].set_title(f'PSD - Direction {["X", "Y", "Z"][i]}')
            self.axes[i+1].set_xlabel('Frequency (Hz)')
            self.axes[i+1].set_ylabel('PSD')

        self.canvas.draw()

    def clear_plots(self):
        for ax in self.axes:
            ax.clear()
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PSD Plotter")

        self.tab_widget = QTabWidget()

        self.input_tab = QWidget()
        self.plot_tab = PSDPlotter()

        self.tab_widget.addTab(self.input_tab, "Input")
        self.tab_widget.addTab(self.plot_tab, "Plots")

        self.setCentralWidget(self.tab_widget)

        self.setup_input_tab()

    def setup_input_tab(self):
        layout = QFormLayout()

        self.load_button = QPushButton("Load CSV")
        self.load_button.clicked.connect(self.load_csv)

        self.plot_g_button = QPushButton("Plot G-Levels")
        self.plot_g_button.clicked.connect(self.plot_g_levels)

        self.start_time_input = QLineEdit()
        self.end_time_input = QLineEdit()
        layout.addRow(QLabel("Start Time (s):"), self.start_time_input)
        layout.addRow(QLabel("End Time (s):"), self.end_time_input)
        self.plot_psd_button = QPushButton("Plot PSD")
        self.plot_psd_button.clicked.connect(self.plot_psd)

        self.csv_path_label = QLabel()
        layout.addRow("CSV File:", self.csv_path_label)
        layout.addRow(self.load_button)
        layout.addRow(self.plot_g_button)
        layout.addRow(self.plot_psd_button)

        self.input_tab.setLayout(layout)

    def load_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load CSV", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.csv_path_label.setText(file_path)
            self.data = np.loadtxt(file_path, delimiter=',', skiprows=1)

    def plot_g_levels(self):
        fs = float(self.get_field_value(self.plot_tab.fs_input))
        sensitivity = float(self.get_field_value(self.plot_tab.sensitivity_input))
        self.plot_tab.clear_plots()
        self.plot_tab.plot_g_levels(self.data, fs, sensitivity)

    def plot_psd(self):
        start_time = float(self.get_field_value(self.start_time_input))
        end_time = float(self.get_field_value(self.end_time_input))
        self.plot_tab.plot_psd(self.data, start_time, end_time)

    def get_field_value(self, field):
        return field.text().strip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
