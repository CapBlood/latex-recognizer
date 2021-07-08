from PySide2 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2


class MixinCvFormat:
    CV_FORMAT = "PNG"

    def to_cv(self):
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly)
        self.pixmap().save(buff, self.CV_FORMAT)
        pic_bytes = ba.data()
        x = np.fromstring(pic_bytes, dtype='uint8')
        image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
        return image


class Canvas(QtWidgets.QLabel, MixinCvFormat):
    FILL_COLOR = '#ffffff'
    PEN_COLOR = '#000000'
    PEN_WIDTH = 4

    def __init__(self, size):
        super().__init__()
        pixmap = QtGui.QPixmap(*size)
        self.setPixmap(pixmap)
        self.clear()

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(self.PEN_COLOR)

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def clear(self):
        self.pixmap().fill(QtGui.QColor(self.FILL_COLOR))
        self.update()

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return
        # https://stackoverflow.com/questions/59047167/mouse-position-on-mouse-move-event-is-set-on-parent-instead-of-child
        rect = self.contentsRect()
        pmRect = self.pixmap().rect()
        if rect != pmRect:
            # the pixmap rect is different from that available to the label
            align = self.alignment()
            if align & QtCore.Qt.AlignHCenter:
                # horizontally align the rectangle
                pmRect.moveLeft((rect.width() - pmRect.width()) / 2)
            elif align & QtCore.Qt.AlignRight:
                # align to bottom
                pmRect.moveRight(rect.right())
            if align & QtCore.Qt.AlignVCenter:
                # vertically align the rectangle
                pmRect.moveTop((rect.height() - pmRect.height()) / 2)
            elif align & QtCore.Qt.AlignBottom:
                # align right
                pmRect.moveBottom(rect.bottom())

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.PEN_WIDTH)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.translate(-pmRect.topLeft())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
