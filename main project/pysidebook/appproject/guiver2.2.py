import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QTabWidget, QLabel, QLineEdit, QFormLayout
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import welch


class PSDPlotter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.axes = plt.subplots(3, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_psd(self, data, fs, sensitivity):
        for i in range(3):
            f, Pxx = welch(data[:, i], fs=fs)
            self.axes[i].clear()
            self.axes[i].semilogy(f, Pxx / sensitivity**2)
            self.axes[i].set_title(f'PSD - Direction {["X", "Y", "Z"][i]}')
            self.axes[i].set_xlabel('Frequency (Hz)')
            self.axes[i].set_ylabel('PSD')
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

        self.plot_button = QPushButton("Plot PSD")
        self.plot_button.clicked.connect(self.plot_psd)

        self.csv_path_label = QLabel()
        layout.addRow("CSV File:", self.csv_path_label)
        layout.addRow(self.load_button)
        self.fs_input = QLineEdit()
        layout.addRow(QLabel("Sampling Frequency (Hz):"), self.fs_input)
        self.sensitivity_input = QLineEdit()
        layout.addRow(QLabel("Sensitivity:"), self.sensitivity_input)
        layout.addRow(self.plot_button)

        self.input_tab.setLayout(layout)

    def load_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load CSV", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.csv_path_label.setText(file_path)
            self.data = np.loadtxt(file_path, delimiter=',', skiprows=1)

    def plot_psd(self):
        fs = float(self.fs_input.text())
        sensitivity = float(self.sensitivity_input.text())
        self.plot_tab.plot_psd(self.data, fs, sensitivity)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
