
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from ui.mainwindow import Ui_MainWindow


class MainView(QMainWindow):
	def __init__(self, model, ctrl):
		super().__init__()
		self._model = model
		self._main_ctrl = ctrl
		self._ui = Ui_MainWindow()
		self._ui.setupUi(self)




