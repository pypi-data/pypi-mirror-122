# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLayout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = QLabel("hello world")
    label.show()
    app.exec()
