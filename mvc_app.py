from PyQt5.QtWidgets import QApplication
from pandasmodel import PandasModel
from ctrl.main_ctrl import MainController
from ui.mainwindow import MainWindow


class ZaurApp(QApplication):
	def __init__(self, sys_argv):
		super().__init__(sys_argv)
		self.model = PandasModel()
		self.main_ctrl = MainController(self.model)
		self.main_view = MainWindow(self.model, self.main_ctrl)
		self.main_view.show()


if __name__ == '__main__':
	app = ZaurApp(sys.argv)
	sys.exit(app.exec_())



