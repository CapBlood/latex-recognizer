from PySide2 import QtWidgets

from latex_recognizer.recognize_window import Recognizer


class LatexTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.__configure()

    def __configure(self):
        self._recognizer = Recognizer()

        menu = QtWidgets.QMenu(self.parent())
        recognize_action = menu.addAction("Recognize")
        exit_action = menu.addAction("Exit")
        recognize_action.triggered.connect(self.show_recognize)
        exit_action.triggered.connect(
            QtWidgets.QApplication.instance().quit)
        self.setContextMenu(menu)

    def show_recognize(self):
        self._recognizer.show()
        self._recognizer.setFocus()
