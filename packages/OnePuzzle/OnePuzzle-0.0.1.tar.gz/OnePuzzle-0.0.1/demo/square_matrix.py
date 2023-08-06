# -*- coding: utf-8 -*-
from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

win = QWidget()
win.resize(500, 500)

win.move(500, 200)


# widget_count 总方块的个数
# colunm 总列数
# row  总行数


def rectangle_ruler(widget_count, colunm):
    widget_width = win.width() / colunm
    widget_width = 0.95 * widget_width
    colunm_interval = 0.05 * win.width() / (colunm + 1)

    row = (widget_count - 1) // colunm + 1
    widget_height = win.height() / row
    widget_height = 0.95 * widget_height
    row_interval = 0.05 * win.height() / (row + 1)

    for i in range(0, widget_count):
        row_num = i // colunm + 1
        colunm_num = i % colunm + 1
        # row_num    任意方块的行数为：（i）//3  + 1
        # colunm_num         列数为：i%3 + 1

        w = QWidget(win)
        w.setGeometry(colunm_num * colunm_interval + (colunm_num - 1) * widget_width, \
                      row_num * row_interval + (row_num - 1) * widget_height, \
                      widget_width, widget_height)

        w.setStyleSheet('background-color:cyan')


if __name__ == '__main__':
    rectangle_ruler(25, 5)

    win.show()
    sys.exit(app.exec_())
