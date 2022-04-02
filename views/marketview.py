from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from ui.marketswindow import Ui_Form
from ctrl.markets_ctrl import MarketsController


class MarketsView(QMainWindow):
	def __init__(self, model, ctrl):
		super().__init__()
		self._model = model
		self._ctrl = ctrl
		self._ui = Ui_Form()
		self._ui.setupUi(self)




