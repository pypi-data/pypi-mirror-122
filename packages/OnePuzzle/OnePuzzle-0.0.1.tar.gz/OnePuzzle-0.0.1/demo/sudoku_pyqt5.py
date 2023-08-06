# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication, QWidget


def rectangle_ruler(win, widget_count, column):
    widget_width = 0.95 * (win.width() / column)
    column_interval = 0.05 * win.width() / (column + 1)

    row = (widget_count - 1) // column + 1
    widget_height = win.height() / row
    widget_height *= 0.95
    row_interval = 0.05 * win.height() / (row + 1)

    for i in range(0, widget_count):
        row_num = i // column + 1
        column_num = i % column + 1
        # row_num    任意方块的行数为：（i）//3  + 1
        # column_num         列数为：i%3 + 1

        w = QWidget(win)
        w.setGeometry(int(column_num * column_interval + (column_num - 1) * widget_width),
                      int(row_num * row_interval + (row_num - 1) * widget_height),
                      int(widget_width), int(widget_height))

        w.setStyleSheet('background-color:cyan')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QWidget()
    widget.resize(600, 600)
    widget.move(500, 200)

    rectangle_ruler(widget, 49, 7)
    widget.show()
    app.exec()
