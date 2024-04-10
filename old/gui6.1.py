import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import welch

class PSDPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PSD Plotter')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Widgets for parameters
        self.sampling_rate_label = QLabel('Sampling Rate:')
        self.layout.addWidget(self.sampling_rate_label)
        self.sampling_rate_input = QLineEdit()
        self.layout.addWidget(self.sampling_rate_input)

        self.nperseg_label = QLabel('Nperseg:')
        self.layout.addWidget(self.nperseg_label)
        self.nperseg_input = QLineEdit()
        self.layout.addWidget(self.nperseg_input)

        self.window_label = QLabel('Window (e.g., hanning, hamming, blackman):')
        self.layout.addWidget(self.window_label)
        self.window_input = QLineEdit()
        self.layout.addWidget(self.window_input)

        self.load_button = QPushButton('Load CSV File')
        self.load_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.load_button)

        self.plot_button = QPushButton('Plot PSD')
        self.plot_button.clicked.connect(self.plot_psd)
        self.layout.addWidget(self.plot_button)

        # Plot area
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if file_name:
            try:
                self.data = np.loadtxt(file_name, delimiter=',')
            except Exception as e:
                print("Error:", e)

    def compute_psd(self, data, sampling_rate, nperseg, window):
        freq, psd = welch(data, fs=sampling_rate, nperseg=nperseg, window=window, scaling='density')
        return freq, psd

    def plot_psd(self):
        try:
            sampling_rate = float(self.sampling_rate_input.text())
            nperseg = int(self.nperseg_input.text())
            window = self.window_input.text()

            freq, psd = self.compute_psd(self.data, sampling_rate, nperseg, window)
            self.ax.clear()
            self.ax.semilogy(freq, psd)
            self.ax.set_xlabel('Frequency (Hz)')
            self.ax.set_ylabel('PSD')
            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PSDPlotter()
    window.show()
    sys.exit(app.exec_())
