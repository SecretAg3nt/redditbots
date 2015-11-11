import sys
from PyQt4 import QtGui, QtCore
import pelicanbot


class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("PelicanBot")

		extractAction = QtGui.QAction("&Quit", self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip("Quits bot")
		extractAction.triggered.connect(self.close_application)

		startAction = QtGui.QAction("&Start", self)
		startAction.setShortcut("Ctrl+S")
		startAction.setStatusTip("Starts bot")
		startAction.triggered.connect(pelicanbot.run)

		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("&File")
		fileMenu.addAction(startAction)
		fileMenu.addAction(extractAction)




		self.home()

	def home(self):
		startbtn = QtGui.QPushButton("Start", self)
		startbtn.clicked.connect(pelicanbot.run)
		startbtn.resize(startbtn.sizeHint())
		startbtn.move(100, 125)


		quitbtn = QtGui.QPushButton("Quit", self)
		quitbtn.clicked.connect(self.close_application)
		quitbtn.resize(quitbtn.sizeHint())
		quitbtn.move(200, 125)

		self.show()

	def close_application(self):
		sys.exit()


def runGUI():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

runGUI()