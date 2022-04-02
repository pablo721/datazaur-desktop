from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSlot
from ui.tradewindow import Ui_Form


class Trading(QMainWindow):
	def __init__(self, model, ctrl):
		super().__init__()
		self._model = model
		self._ctrl = ctrl
		self._ui = Ui_Form
		self._ui.setupUi(self)
