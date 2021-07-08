import json
from collections import namedtuple

import cv2
import numpy as np
from PySide2 import QtWidgets
from tensorflow.keras.models import load_model

from latex_recognizer.canvas import Canvas
from latex_recognizer.output import OutputLabel
from latex_recognizer.resources import resource_path


def get_model(path_model, path_meta):
    Rect = namedtuple("Rect", "x y w h")
    model = load_model(path_model)
    with open(path_meta) as file:
        rel = json.load(file)

    def union(a, b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0] + a[2], b[0] + b[2]) - x
        h = max(a[1] + a[3], b[1] + b[3]) - y
        return x, y, w, h

    def find_symbol(img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.medianBlur(image, 1)
        _, thresh = cv2.threshold(image,
                                  230, 255,
                                  cv2.THRESH_BINARY_INV)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                           (4, 4))
        dilated = cv2.dilate(thresh, kernel, iterations=5)
        cnts = cv2.findContours(dilated,
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_NONE)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        rect = cv2.boundingRect(cnts[0])
        for c in cnts[1:]:
            rect = union(rect, cv2.boundingRect(c))

        return Rect(*rect)

    def recognize(img):
        x, y, w, h = find_symbol(img)
        img = img[y:y + h, x:x + w]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_NEAREST)
        _, resized = cv2.threshold(resized, 165, 255, cv2.THRESH_BINARY)

        input_arr = np.array([np.reshape(resized / 255, (32, 32, 1))])
        pred = model.predict(input_arr)
        idx = np.argmax(pred)

        return rel[str(idx)], pred[0][idx]

    return recognize


class Recognizer(QtWidgets.QWidget):
    PATH_MODEL = resource_path("models/model_recognizer.h5")
    PATH_REL = resource_path("models/classes.json")
    RECOGNIZER_WINDOW_SIZE = (300, 375)
    CANVAS_SIZE = (250, 300)
    BOTTOM_PANEL_HEIGHT = 75

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.model = get_model(self.PATH_MODEL, self.PATH_REL)

        self.setFixedSize(*self.RECOGNIZER_WINDOW_SIZE)
        layout = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()

        self.canvas = Canvas(self.CANVAS_SIZE)
        top_layout.addWidget(self.canvas)
        layout.addLayout(top_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_widget.setFixedHeight(self.BOTTOM_PANEL_HEIGHT)
        layout.addWidget(bottom_widget)

        panel_layout = QtWidgets.QHBoxLayout()
        recognize_button = QtWidgets.QPushButton("Recognize")
        recognize_button.clicked.connect(self.recognize)
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(self.clear)
        self.output = OutputLabel()
        self.output.hide()

        panel_layout.addWidget(self.output)
        panel_layout.addStretch(1)
        panel_layout.addWidget(recognize_button)
        panel_layout.addWidget(clear_button)

        bottom_widget.setLayout(panel_layout)
        self.setLayout(layout)

    def clear(self):
        self.canvas.clear()
        self.output.clear()
        self.output.hide()

    def recognize(self):
        image = self.canvas.to_cv()
        pred = self.model(image)

        self.output.clear()

        title = "{}\n" \
                "Score: {}".format(pred[0],
                                   str(np.round(pred[1], 4)))
        self.output.set_data(title, pred[0])
        self.output.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

