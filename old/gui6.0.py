import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PSDPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PSD Plotter')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.load_button = QPushButton('Load CSV File')
        self.load_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.load_button)

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if file_name:
            try:
                data = np.loadtxt(file_name, delimiter=',')
                freq, psd = self.compute_psd(data)
                self.plot_psd(freq, psd)
            except Exception as e:
                print("Error:", e)

    def compute_psd(self, data):
        fs = 1.0  # Sampling frequency (assuming 1 Hz for simplicity)
        psd, freq = np.histogram(data.flatten(), bins=1024, density=True)
        freq = freq[:-1]  # Remove last element to make freq and psd the same length
        return freq, psd

    def plot_psd(self, freq, psd):
        self.ax.clear()
        self.ax.semilogy(freq, psd)
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('PSD')
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PSDPlotter()
    window.show()
    sys.exit(app.exec_())
