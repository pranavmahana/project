import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QFileDialog, QComboBox
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Create a combo box for theme selection
        self.theme_combo = QComboBox(self)
        self.theme_combo.addItem('Default')
        self.theme_combo.addItem('Dark')
        layout.addWidget(self.theme_combo)

        # Create a label for the x-axis selection
        self.x_axis_label = QLabel('X-axis:', self)
        layout.addWidget(self.x_axis_label)

        # Create a line edit for x-axis selection
        self.x_axis_lineedit = QLineEdit(self)
        layout.addWidget(self.x_axis_lineedit)

        # Create a label for the y-axis selection
        self.y_axis_label = QLabel('Y-axis:', self)
        layout.addWidget(self.y_axis_label)

        # Create a line edit for y-axis selection
        self.y_axis_lineedit = QLineEdit(self)
        layout.addWidget(self.y_axis_lineedit)

        # Create a radio button for versus all option
        self.vs_all_radio = QRadioButton('Versus all', self)
        layout.addWidget(self.vs_all_radio)

        # Create a push button for file selection
        self.file_button = QPushButton('Select file', self)
        layout.addWidget(self.file_button)

        # Create a figure for the plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Connect the signals to the slots
        self.theme_combo.currentIndexChanged.connect(self.update_plot)
        self.x_axis_lineedit.editingFinished.connect(self.update_plot)
        self.y_axis_lineedit.editingFinished.connect(self.update_plot)
        self.vs_all_radio.toggled.connect(self.update_plot)
        self.file_button.clicked.connect(self.open_file_dialog)

        # Initialize the updating_plot flag
        self.updating_plot = False

    # def open_file_dialog(self):
    #     file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'CSV files (*.csv)')
    #     if file_name:
    #         self.data = pd.read_csv(file_name)
    #         self.x_axis_lineedit.clear()
    #         self.y_axis_lineedit.clear()
    #         if not self.data.empty:
    #             self.x_axis_lineedit.setText(str(self.data.columns[0]))
    #             self.y_axis_lineedit.setText(str(self.data.columns[1]))

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'CSV files (*.csv)')
        if file_name:
            self.data = pd.read_csv(file_name)
            self.x_axis_lineedit.clear()
            self.y_axis_lineedit.clear()
        if not self.data.empty:
            self.x_axis_lineedit.setText(str(self.data.columns[0]))
            self.y_axis_lineedit.setText(str(self.data.columns[1]))
            self.update_plot()
              # Manually call the update_plot function
    def update_plot(self):
        # Use a flag to determine whether to disconnect and reconnect the editingFinished signal
        if not self.updating_plot:
            self.updating_plot = True

            # Disconnect the editingFinished signal temporarily
            self.x_axis_lineedit.editingFinished.disconnect(self.update_plot)
            self.y_axis_lineedit.editingFinished.disconnect(self.update_plot)

            # Clear the current plot
            self.ax.clear()

            # Check if the "versus all" option is selected
            if self.vs_all_radio.isChecked() and hasattr(self, 'data'):
                for col in self.data.columns:
                    if col != self.x_axis_lineedit.text():
                        self.ax.plot(self.data[self.x_axis_lineedit.text()], self.data[col], label=col)
                self.ax.legend()
            elif hasattr(self, 'data'):
                self.ax.plot(self.data[self.x_axis_lineedit.text()], self.data[self.y_axis_lineedit.text()])

            self.ax.set_xlabel(self.x_axis_lineedit.text())
            self.ax.set_ylabel(self.y_axis_lineedit.text())
            self.ax.set_title('CSV Data Plot')

            # Reconnect the editingFinished signal
            self.x_axis_lineedit.editingFinished.connect(self.update_plot)
            self.y_axis_lineedit.editingFinished.connect(self.update_plot)

            self.canvas.draw()

            # Reset the flag
            self.updating_plot = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
