import sys
from pathlib import Path

from numpy import hamming
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from ui.dialogs import *
from models import *
from tools import *
from ui.testtask import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_name = ""
        self.plt = self.ui.graph_widget.getPlotItem()
        self.plt.axes['left']['item'].setLabel(text='Виброускорение, м/с²')
        self.curve = self.plt.plot()
        self.curve.opts["pen"] = pg.mkPen((45, 112, 149), width=1)
        self.ui.open_file.triggered.connect(self.open_file)
        self.ui.signal.triggered.connect(self.plot_signal)
        self.ui.signal_button.clicked.connect(self.plot_signal)
        self.ui.signal_spectrum.triggered.connect(self.plot_signal_spectrum)
        self.ui.spectrum_button.clicked.connect(self.plot_signal_spectrum)
        self.ui.signal_envelope.triggered.connect(self.plot_envelope_signal)
        self.ui.envelope_button.clicked.connect(self.plot_envelope_signal)
        self.ui.envelope_spectrum.triggered.connect(self.plot_spectrum_envelope)
        self.ui.envelope_spectrum_button.clicked.connect(self.plot_spectrum_envelope)

        self.current_signal_data_x = np.array([])
        self.current_signal_data_y = np.array([])

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            caption="Open File",
            filter="Signal Files (*.dd *.d2 *.d3 *.udd)"
        )[0]
        if file_path:
            self.ui.menu_tools.setEnabled(False)
            self.ui.signal.setEnabled(False)
            self.ui.signal_button.setEnabled(False)
            self.ui.spectrum_button.setEnabled(False)
            self.ui.signal_spectrum.setEnabled(False)
            self.ui.envelope_button.setEnabled(False)
            self.ui.signal_envelope.setEnabled(False)
            self.file_name = Path(file_path).name

            file_suffix = Path(file_path).suffix

            if ".dd" == file_suffix:
                self.file = dd_file(file_path)
            elif ".d2" == file_suffix:
                self.file = d2_file(file_path)
            elif ".d3" == file_suffix:
                self.file = d3_file(file_path)
            elif ".udd" == file_suffix:
                self.file = udd_file(file_path)
            else:
                return 0
            self.setWindowTitle(file_path)
            self.ui.menu_tools.setEnabled(True)
            self.ui.signal.setEnabled(True)
            self.ui.signal_button.setEnabled(True)

    def plot_signal(self):
        dialog = DialogSignal()
        count_channels = self.file.get_count_channels()

        if hasattr(self.file, "version_file0") and hasattr(self.file, "version_file1"):
            if self.file.version_file0:
                channel_with_index_0 = 0
            if self.file.version_file1:
                channel_with_index_0 = 1
        else:
            channel_with_index_0 = 0

        start_index = 1 - channel_with_index_0  # если есть канал с индексом 0, то начало цикла с нуля
        stop_index = count_channels + 1 - channel_with_index_0
        for i in range(start_index, stop_index):
            dialog.list_channels.addItem(f"{i}. {self.file.get_channel_name(i)}")
        if dialog.exec():
            self.selected_channel = dialog.list_channels.currentIndex() + 1 - channel_with_index_0
            signal = self.file.get_signal(self.selected_channel)
            signal_time = self.file.get_signal_time(self.selected_channel)
            self.current_signal_data_y = signal
            self.current_signal_data_x = signal_time
            self.curve.setData(signal_time, signal)
            self.plt.enableAutoRange(True, x=True, y=True)
            self.plt.axes['bottom']['item'].setLabel(text='Время, с')
            self.ui.spectrum_button.setEnabled(True)
            self.ui.signal_spectrum.setEnabled(True)
            self.ui.envelope_button.setEnabled(True)
            self.ui.signal_envelope.setEnabled(True)

    def plot_signal_spectrum(self):
        dialog = DialogSignalSpectrum()
        if dialog.exec():
            count_samples = self.file.get_number_of_samples(self.selected_channel)
            sampling_frequency = self.file.get_sampling_frequency(self.selected_channel)
            window = hamming(count_samples)
            yf, xf = fft_normalized(self.current_signal_data_y * window, count_samples, sampling_frequency)
            self.curve.setData(xf, yf)
            if dialog.min_spectrum_f.text() and dialog.max_spectrum_f.text():
                min_freq = int(dialog.min_spectrum_f.text())
                max_freq = int(dialog.max_spectrum_f.text())
                self.plt.setXRange(min_freq, max_freq)
            else:
                self.plt.enableAutoRange(True, x=True, y=True)
            self.plt.axes['bottom']['item'].setLabel(text='Частота, Гц')

    def plot_envelope_signal(self):
        dialog = DialogSignalEnvelope()
        if dialog.exec():
            count_samples = self.file.get_number_of_samples(self.selected_channel)
            sampling_frequency = self.file.get_sampling_frequency(self.selected_channel)
            f_min = float(dialog.frequency_min.text())
            f_max = float(dialog.frequency_max.text())
            band = [f_min, f_max]
            self.current_signal_envelope = envelope_signal(self.current_signal_data_y, band, sampling_frequency,
                                                           count_samples)
            self.curve.setData(self.current_signal_data_x, self.current_signal_envelope)
            self.ui.envelope_spectrum.setEnabled(True)
            self.ui.envelope_spectrum_button.setEnabled(True)
            self.plt.enableAutoRange(True, x=True, y=True)

        self.plt.axes['bottom']['item'].setLabel(text='Время, с')

    def plot_spectrum_envelope(self):
        dialog = DialogSignalEnvelopeSpectrum()
        if dialog.exec():
            count_samples = self.file.get_number_of_samples(self.selected_channel)
            sampling_frequency = self.file.get_sampling_frequency(self.selected_channel)
            yf, xf = fft_normalized(self.current_signal_envelope, count_samples, sampling_frequency)
            yf[0] = 0 # убирается составляющая на частоте 0
            self.curve.setData(xf, yf)
            if dialog.min_spectrum_f.text() and dialog.max_spectrum_f.text():
                min_freq = int(dialog.min_spectrum_f.text())
                max_freq = int(dialog.max_spectrum_f.text())
                self.plt.setXRange(min_freq, max_freq)
            else:
                self.plt.enableAutoRange(True, x=True, y=True)
        self.plt.axes['bottom']['item'].setLabel(text='Частота, Гц')


if __name__ == "__main__":
    pg.setConfigOption('background', 'w')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
