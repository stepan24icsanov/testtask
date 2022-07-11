from ui.DialogSignal import Ui_DialogSignal
from ui.DialogSignalSpectrum import Ui_DialogSignalSpectrum
from ui.DialogSignalEnvelope import Ui_DialogSignalEvelope
from ui.DialogSignalEnvelopeSpectrum import Ui_DialogSignalEnvelopeSpectrum
from PyQt5.QtWidgets import QDialog


class DialogSignal(QDialog, Ui_DialogSignal):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Выбор сигнала")


class DialogSignalSpectrum(QDialog, Ui_DialogSignalSpectrum):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Построение спектра сигнала")

class DialogSignalEnvelope(QDialog, Ui_DialogSignalEvelope):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Расчет огибающей сигнала")

class DialogSignalEnvelopeSpectrum(QDialog, Ui_DialogSignalEnvelopeSpectrum):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Спектр огибающей")
