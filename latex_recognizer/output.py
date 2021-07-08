import uuid

from PySide2 import QtWidgets, QtCore


class OutputLabel(QtWidgets.QLabel):
    STYLE_ITEM = ':hover { background-color: rgb(52, 50, 51); }'
    TIMEOUT_TIMER = 1000

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent=parent)
        self.setWordWrap(True)
        self._content = None
        self._title = None
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._end_timer)
        obj_name = uuid.uuid4().hex
        self.setObjectName(obj_name)
        self.setStyleSheet("#{}{}".format(obj_name, self.STYLE_ITEM))

    def set_data(self, title, content):
        self.setText(title)
        self._title = title
        self._content = content

    def mousePressEvent(self, e):
        if self._content is not None:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self._content)
            self._start_timer()

    def _start_timer(self):
        self._timer.start(self.TIMEOUT_TIMER)
        self.setEnabled(False)
        self.setText("Copied!")

    def _end_timer(self):
        self._timer.stop()
        self.setEnabled(True)
        self.setText(self._title)
