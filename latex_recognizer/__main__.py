import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
import qdarkstyle

from latex_recognizer.tray import LatexTray
from latex_recognizer.resources import resource_path


ICON_PATH = "assets/icon.png"


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))
    tray = LatexTray(QIcon(resource_path(ICON_PATH)))
    tray.show()
    return app.exec_()


if __name__ == "__main__":
    main()
