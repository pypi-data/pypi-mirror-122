# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLayout, QPushButton, QVBoxLayout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton("Top"))
    layout.addWidget(QPushButton("Button"))
    window.setLayout(layout)
    window.show()
    app.exec()
