import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import numpy as np
from scipy.signal import welch
from mplwidget import MplWidget

class RadarGUI(QMainWindow):
    def __init__(self):
        super(RadarGUI, self).__init__()
        loadUi('radar_gui.ui', self)
        self.setWindowTitle('Radar PSD Viewer')
        
        self.plot_button.clicked.connect(self.plot_psd)
        self.plot_widget = MplWidget(self.centralwidget)

    def plot_psd(self):
        # Sample radar data (replace this with your own data)
        fs = 1000  # Sample rate (Hz)
        t = np.arange(0, 10, 1/fs)  # 10 seconds
        radar_data = np.sin(2 * np.pi * 50 * t) + 0.5 * np.random.randn(len(t))
        
        f, psd = welch(radar_data, fs=fs, nperseg=1024)
        
        # Clear previous plot
        self.plot_widget.ax.clear()
        
        # Plot PSD
        self.plot_widget.ax.semilogy(f, psd)
        self.plot_widget.ax.set_xlabel('Frequency (Hz)')
        self.plot_widget.ax.set_ylabel('PSD (dB/Hz)')
        self.plot_widget.ax.set_title('Power Spectral Density')
        self.plot_widget.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = RadarGUI()
    mainWindow.show()
    sys.exit(app.exec_())

