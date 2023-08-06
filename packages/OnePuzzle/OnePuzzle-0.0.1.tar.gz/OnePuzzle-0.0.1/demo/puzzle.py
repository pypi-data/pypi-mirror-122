# -*- coding: utf-8 -*-
import sys
from operator import add, sub
from queue import Queue

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

MONTH_COLOR = "#c1c1c1"
DAY_COLOR = "#c6c6c6"
TARGET_COLOR = "#212121"


class Block(object):
    row = 1
    col = 1

    def __init__(self, row=None, col=None):
        if row:
            self.row = row

        if col:
            self.col = col

    def __repr__(self):
        return "<Block/{}-{}>".format(self.row, self.col)

    __str__ = __repr__

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return int("{}{}".format(int(self.row), int(self.col)))


class JAN(Block):
    row = 1
    col = 1


class FEB(Block):
    row = 1
    col = 2


class MAR(Block):
    row = 1
    col = 3


class APR(Block):
    row = 1
    col = 4


class MAY(Block):
    row = 1
    col = 5


class JUN(Block):
    row = 1
    col = 6


class JUL(Block):
    row = 2
    col = 1


class AUG(Block):
    row = 2
    col = 2


class SEP(Block):
    row = 2
    col = 3


class OCT(Block):
    row = 2
    col = 4


class NOV(Block):
    row = 2
    col = 5


class DEC(Block):
    row = 2
    col = 6


# 每个图案有八种形态，上下左右
# 倾斜90度之后，上下左右
class Pattern(object):
    color = "#d7ccc8"
    blocks = []

    col_offset = row_offset = 0

    def __init__(self, col_offset=0, row_offset=0):
        self.col_offset = col_offset
        self.row_offset = row_offset
        for block in self.blocks:
            block.col += col_offset
            block.row += row_offset


class BigL(Pattern):
    color = "#b2dfdb"
    blocks = [Block(1, 1), Block(2, 1), Block(3, 1), Block(4, 1), Block(4, 2)]

    def rotate(self):
        self.blocks = [Block(2, 1), Block(2, 2), Block(2, 3), Block(2, 4), Block(1, 4)]
        return self


class FullSmash(Pattern):
    color = "#c8e6c9"
    blocks = [Block(1, 1), Block(1, 2), Block(1, 3), Block(2, 1), Block(2, 2), Block(2, 3)]


class LackSmash(Pattern):
    color = "#e1bee7"
    blocks = [Block(1, 1), Block(1, 2), Block(1, 3), Block(2, 1), Block(2, 2)]


class BigZ(Pattern):
    color = "#d1c4e9"
    blocks = [Block(1, 1), Block(1, 2), Block(2, 2), Block(3, 2), Block(3, 3)]


class Sunken(Pattern):
    color = "#c5cae9"
    blocks = [Block(1, 1), Block(2, 1), Block(2, 2), Block(2, 3), Block(1, 3)]


class Convex(Pattern):
    color = "#bbdefb"
    blocks = [Block(1, 2), Block(2, 1), Block(2, 2), Block(2, 3), Block(2, 4)]


class EquilateralL(Pattern):
    color = "#b3e5fc"
    blocks = [Block(1, 1), Block(2, 1), Block(3, 1), Block(3, 2), Block(3, 3)]


class Stiletto(Pattern):
    color = "#b2ebf2"
    blocks = [Block(1, 1), Block(2, 1), Block(2, 2), Block(3, 2), Block(4, 2)]


class Board(object):
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.column = 7
        self.app = QApplication(sys.argv)
        self.widget = QWidget()
        self.widget.setWindowTitle('A Puzzle A Day')
        self.widget.resize(width, height)

        self.block_width = 0.95 * (width / self.column)
        self.block_interval = 0.05 * width / (self.column + 1)

        self.months = [JAN(), FEB(), MAR(), APR(), MAY(), JUN(), JUL(), AUG(), SEP(), OCT(), NOV(), DEC()]
        self.days = [Block(3 + i // self.column, 1 + i % self.column) for i in range(31)]
        self.entities = []

    def draw_block(self, column_num, row_num, color="cyan", text=None):
        w = QWidget(self.widget)
        w.setGeometry(
            int(column_num * self.block_interval + (column_num - 1) * self.block_width),
            int(row_num * self.block_interval + (row_num - 1) * self.block_width),
            int(self.block_width),
            int(self.block_width),
        )

        w.setStyleSheet('background-color:{}'.format(color))
        if text:
            text_label = QLabel(w)
            text_label.setStyleSheet('color:#ffffff')
            text_label.setText(text)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont('', 24))
            text_label.resize(self.block_width, self.block_width)

    def draw_months(self):
        for month in self.months:  # type: Block
            self.draw_block(month.col, month.row, MONTH_COLOR)

    def draw_days(self):
        for day in self.days:  # type: Block
            self.draw_block(day.col, day.row, DAY_COLOR)

    def draw_pattern(self, pattern):
        # type: (Pattern) -> ()
        for block in pattern.blocks:
            self.draw_block(block.col, block.row, pattern.color)

    def show(self, pattern=None):
        self.draw_months()
        self.draw_days()
        if pattern:
            self.draw_pattern(pattern)

        for entity in self.entities:
            self.draw_pattern(entity)

        self.widget.show()
        self.app.exec()

    def add_entity(self, entity):
        # type: (OperateEntity)->()
        self.entities.append(entity)


class OperateEntity(object):
    color = "#ffecb3"
    # 水平线
    horizontal_line = 0.5
    # 垂直线
    vertical_line = 2.5
    operates = []
    vertical_transfer = False
    horizontal_transfer = False
    rotate_transfer = False

    vertical_add = add
    horizontal_add = add
    vertical_sub = sub
    horizontal_sub = sub

    def __init__(self, col_offset=0, row_offset=0):
        self.col_offset = col_offset
        self.row_offset = row_offset
        self.horizontal_line += col_offset
        self.vertical_line += row_offset

    def vertical(self):
        self.vertical_transfer = not self.vertical_transfer
        self.vertical_sub, self.vertical_add = self.vertical_add, self.vertical_sub
        return self

    def horizontal(self):
        self.horizontal_transfer = not self.horizontal_transfer
        self.horizontal_sub, self.horizontal_add = self.horizontal_add, self.horizontal_sub
        return self

    @property
    def blocks(self):
        return [Block(x(self.horizontal_line), y(self.vertical_line)) for x, y in self.operates]

    def __repr__(self):
        # return "OperateEntity[{}]".format(",".join(map(repr, self.blocks)))
        base = "{}({}, {})".format(self.__class__.__name__, self.col_offset, self.row_offset)
        if self.horizontal_transfer:
            base += ".horizontal()"
        if self.vertical_transfer:
            base += ".vertical()"
        if self.rotate_transfer:
            base += ".rotate()"
        return base

    def rotate(self):
        self.rotate_transfer = not self.rotate_transfer
        self.horizontal_line, self.vertical_line = self.vertical_line, self.horizontal_line
        for operate in self.operates:
            operate[0], operate[1] = operate[1], operate[0]
        return self


class BigLEntity(OperateEntity):
    # 水平线
    horizontal_line = 2.5
    # 垂直线
    vertical_line = 1.5
    color = "#d50000"

    def __init__(self, *args, **kwargs):
        super(BigLEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_add(y, 0.5)],
        ]


class FullSmashEntity(OperateEntity):
    color = "#e65100"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(FullSmashEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1)],
        ]


class LackSmashEntity(FullSmashEntity):
    color = "#2e7d32"

    def __init__(self, *args, **kwargs):
        super(LackSmashEntity, self).__init__(*args, **kwargs)
        self.operates.pop()


class BigZEntity(OperateEntity):
    color = "#c94ed1"
    # 水平线
    horizontal_line = 2
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(BigZEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 0)],
            [lambda x: self.horizontal_add(x, 0), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 1)],
        ]


# 凹
class SunkenEntity(OperateEntity):
    color = "#536dfe"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(SunkenEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1)],
        ]


# 凸
class ConvexEntity(OperateEntity):
    color = "#00897b"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2.5

    def __init__(self, *args, **kwargs):
        super(ConvexEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1.5)],
        ]


# 等边L
class EquilateralLEntity(OperateEntity):
    color = "#1976d2"
    # 水平线
    horizontal_line = 2
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(EquilateralLEntity, self).__init__(*args, **kwargs)
        self.operates = [
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 0), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 1)],
        ]


# 剑
class StilettoEntity(OperateEntity):
    color = "#6200ea"
    # 水平线
    horizontal_line = 2.5
    # 垂直线
    vertical_line = 1.5

    def __init__(self, *args, **kwargs):
        super(StilettoEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_add(y, 0.5)],
        ]


class Solution(object):
    def __init__(self, month=1, day=1):
        self.month = month
        self.day = day
        self.entity_classes = [
            BigLEntity,
            BigZEntity,
            LackSmashEntity,
            FullSmashEntity,
            EquilateralLEntity,
            StilettoEntity,
            ConvexEntity,
            SunkenEntity,
        ]

    def solve(self):
        board = Board()
        board.months.pop(self.month - 1)
        board.days.pop(self.day - 1)
        totals = set(board.months + board.days)

        result = []
        calculated = 0

        def traceback(left_classes, entities, entity_filled):
            nonlocal calculated
            if calculated % 10000000 == 0 or len(entities) > 6:
                print("{}:{}".format(calculated, entities))
            # print([entity for entity in entities])
            # print(entities)
            for index in range(len(left_classes)):
                classes = left_classes.copy()
                entity_class = classes.pop(index)
                # entity_class = left_classes[i]
                for i in range(7):
                    for j in range(7):

                        for m in [lambda x: x, lambda x: x.rotate()]:
                            for n in [lambda x: x, lambda x: x.horizontal()]:
                                for p in [lambda x: x, lambda x: x.vertical()]:
                                    calculated += 1
                                    entity = entity_class(i, j)
                                    entity = m(n(p(entity)))

                                    # entities = entities.copy()
                                    entities.append(entity)

                                    # entity_filled = entity_filled.copy()
                                    entity_filled.extend(entity.blocks)

                                    # 有超出的
                                    if set(entity_filled) - totals:
                                        # print("overflow")
                                        entities.remove(entity)
                                        for block in entity.blocks:
                                            entity_filled.remove(block)
                                        continue

                                    # 有重复的
                                    if len(entity_filled) != len(set(entity_filled)):
                                        # print("duplicate")
                                        entities.remove(entity)
                                        for block in entity.blocks:
                                            entity_filled.remove(block)
                                        continue

                                    # 有成功
                                    if not totals - set(entity_filled):
                                        # print("success")
                                        # print(entities)
                                        result.append(entities)
                                        return entities

                                    # 有空洞
                                    if not self.validate_trap(totals - set(entity_filled)):
                                        # print("trap")
                                        entities.remove(entity)
                                        for block in entity.blocks:
                                            entity_filled.remove(block)
                                        continue

                                    # 成功则无需再清空
                                    success_result = traceback(classes, entities, entity_filled)
                                    if success_result:
                                        return success_result

                                    # 清空再继续努力
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)

        success_entities = traceback(self.entity_classes, [], [])
        print(calculated)
        print(success_entities)
        # print(len(result))
        for success in success_entities:
            board.add_entity(success)
        board.show()

    def solute(self, entities=None):
        board = Board()
        board.months.pop(self.month - 1)
        board.days.pop(self.day - 1)
        totals = set(board.months + board.days)
        # board.show(FullSmashEntity().rotate().rotate().horizontal())
        # board.show(BigLEntity().rotate().horizontal().vertical().rotate())
        # board.show(LackSmashEntity().rotate().horizontal().vertical().horizontal())
        # board.show(BigZEntity().rotate().horizontal().vertical())
        # board.show(SunkenEntity().rotate().horizontal().vertical())
        # board.show(ConvexEntity().rotate().horizontal().vertical())
        # board.show(EquilateralLEntity().rotate().horizontal().vertical())
        # board.show(StilettoEntity().rotate().horizontal().vertical())
        # Board().show(EquilateralL(2, 3))
        # self.app.exec()

        # entities = BigLEntity().blocks + LackSmashEntity(2, 3).blocks + EquilateralL(2, 3).blocks

        # entities = [FullSmashEntity(0, 3), BigLEntity(), LackSmashEntity(2, 2)]
        # entities = [FullSmashEntity(0, 2)]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 3)]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 3), LackSmashEntity(0, 4)]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 3), LackSmashEntity(0, 4), ConvexEntity(4, 3)]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 3).rotate(), LackSmashEntity(0, 4).rotate(),
        #             SunkenEntity(4, 4).vertical(), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 3).rotate(), LackSmashEntity(4, 3).horizontal().vertical(),
        #             StilettoEntity(2, 2).horizontal().vertical().rotate(), SunkenEntity(4, 0).horizontal().vertical()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 4).vertical(),
        #             LackSmashEntity(1, 2).horizontal().vertical().rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        #             SunkenEntity(3, 2).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 4).vertical(), LackSmashEntity(2, 2),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        #             StilettoEntity(2, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 4).vertical(), ConvexEntity(4, 2).vertical(),
        #             StilettoEntity(2, 1).vertical(), BigZEntity(2, 2).vertical(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(2, 5).vertical(), EquilateralLEntity(2, 2).rotate(),
        #             StilettoEntity(3, 0).vertical(), LackSmashEntity(1, 4).horizontal().vertical().rotate(),
        #             BigZEntity(3, 2).horizontal().vertical()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(2, 5).vertical(), EquilateralLEntity(4, 0),
        #             ConvexEntity(3, 2).rotate(), SunkenEntity(2, 2).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(2, 5).vertical(), EquilateralLEntity(4, 0).vertical(),
        #             BigZEntity(3, 2).horizontal().vertical(), LackSmashEntity(0, 3).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(2, 3).horizontal().vertical().rotate(),
        #             BigLEntity(2, 3).horizontal().vertical(), ConvexEntity(5, 0).horizontal().vertical().rotate(),
        #             StilettoEntity(2, 1).vertical(), EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(2, 3).horizontal().vertical().rotate(),
        #             ConvexEntity(5, 0).horizontal().vertical().rotate(), EquilateralLEntity(4, 0),
        #             BigLEntity(2, 3).horizontal().vertical(), StilettoEntity(2, 1).vertical()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(3, 1).vertical(), SunkenEntity(5, 3).rotate(),
        #             BigLEntity(1, 4).horizontal().vertical().rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        blocks = []
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(3, 2).horizontal().vertical(),
        #             BigLEntity(1, 4).horizontal().vertical().rotate(),
        #             ConvexEntity(5, 0).horizontal().vertical().rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(3, 1).vertical(),
        #             BigLEntity(1, 4).horizontal().vertical().rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        #             StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(3, 3).vertical(), BigLEntity(2, 5).vertical(),
        #             StilettoEntity(2, 1).vertical(), EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), LackSmashEntity(3, 2).horizontal().vertical().rotate(),
        #             BigLEntity(1, 4).horizontal().vertical().rotate(),
        #             ConvexEntity(5, 0).horizontal().vertical().rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 4).vertical(),
        #             LackSmashEntity(0, 3).horizontal().vertical().rotate(),
        #             EquilateralLEntity(3, 3).horizontal().vertical().rotate()]
        # entities = [FullSmashEntity(0, 2), BigLEntity(0, 4).vertical(), BigZEntity(2, 2).vertical(),
        #             StilettoEntity(2, 1).vertical(), EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        #             ConvexEntity(4, 2).vertical()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(2, 3),
        #             FullSmashEntity(4, 1)]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(2, 3),
        #             FullSmashEntity(4, 1)]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(1, 3).vertical(),
        #             LackSmashEntity(2, 4).horizontal().vertical(), FullSmashEntity(4, 4).horizontal().vertical()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 4).rotate(),
        #             FullSmashEntity(5, 2).horizontal().vertical().rotate(),
        #             LackSmashEntity(3, 1).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), FullSmashEntity(4, 1),
        #             StilettoEntity(2, 3), BigZEntity(4, 1).rotate()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), FullSmashEntity(4, 1).vertical(),
        #             BigZEntity(4, 1).horizontal().vertical().rotate(), LackSmashEntity(4, 4).horizontal().vertical()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        #             BigZEntity(4, 1).horizontal().vertical().rotate(), LackSmashEntity(5, 3).vertical().rotate(),
        #             FullSmashEntity(4, 1).horizontal(), StilettoEntity(2, 3)]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal(), LackSmashEntity(0, 4).vertical().rotate(),
        #             FullSmashEntity(4, 4).horizontal().vertical(), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal(), StilettoEntity(0, 5).horizontal().vertical(),
        #             LackSmashEntity(0, 4).vertical().rotate(), FullSmashEntity(4, 4).vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal(), StilettoEntity(0, 5).horizontal().vertical(),
        #             FullSmashEntity(4, 4), LackSmashEntity(0, 4).vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal(), LackSmashEntity(0, 4).vertical().rotate(),
        #             FullSmashEntity(4, 4), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal(), FullSmashEntity(4, 4).horizontal().vertical(),
        #             LackSmashEntity(0, 4).vertical().rotate(), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             EquilateralLEntity(3, 3).horizontal().rotate(), FullSmashEntity(4, 4).horizontal().vertical(),
        #             LackSmashEntity(0, 4).vertical().rotate(), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             StilettoEntity(0, 5).horizontal().vertical(), LackSmashEntity(0, 4).vertical().rotate(),
        #             FullSmashEntity(4, 4).horizontal().vertical(), EquilateralLEntity(3, 3).horizontal().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             LackSmashEntity(0, 4).vertical().rotate(), FullSmashEntity(4, 4).horizontal().vertical(),
        #             StilettoEntity(0, 5).horizontal().vertical(), EquilateralLEntity(3, 3).horizontal().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             LackSmashEntity(0, 4).vertical().rotate(), BigZEntity(2, 4).horizontal(),
        #             StilettoEntity(0, 4).vertical(), EquilateralLEntity(4, 3).vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             BigZEntity(2, 4).horizontal(), LackSmashEntity(0, 4).vertical().rotate(),
        #             EquilateralLEntity(4, 3).vertical().rotate(), StilettoEntity(0, 4).vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             BigZEntity(2, 4).horizontal(), LackSmashEntity(0, 4).vertical().rotate(),
        #             StilettoEntity(0, 4).vertical(), EquilateralLEntity(4, 3).vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(1, 3).rotate(),
        #             BigZEntity(2, 4).vertical(), LackSmashEntity(0, 4).vertical().rotate(),
        #             EquilateralLEntity(4, 3).vertical().rotate(), StilettoEntity(0, 4).vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             EquilateralLEntity(3, 4), LackSmashEntity(5, 2).horizontal().vertical().rotate(),
        #             StilettoEntity(3, 2).horizontal(), FullSmashEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             EquilateralLEntity(3, 4).horizontal().vertical(), BigZEntity(3, 3).horizontal().vertical().rotate(),
        #             StilettoEntity(1, 5).vertical().rotate(), LackSmashEntity(0, 4).rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal(),
        #             LackSmashEntity(5, 2).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             StilettoEntity(0, 4).vertical(), FullSmashEntity(0, 4).horizontal().vertical().rotate(),
        #             BigZEntity(2, 4).horizontal(), EquilateralLEntity(4, 3).vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             StilettoEntity(1, 3).horizontal(), BigZEntity(2, 4).horizontal().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(),
        #             LackSmashEntity(5, 3).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             StilettoEntity(3, 2).horizontal(), FullSmashEntity(0, 4).horizontal().vertical().rotate(),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate(),
        #             LackSmashEntity(5, 2).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             StilettoEntity(3, 2).horizontal(), BigZEntity(4, 2).horizontal().vertical().rotate(),
        #             LackSmashEntity(4, 4).horizontal(), FullSmashEntity(0, 4).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             FullSmashEntity(0, 4).vertical().rotate(),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal(),
        #             LackSmashEntity(4, 0).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             FullSmashEntity(0, 4).horizontal().rotate(), LackSmashEntity(4, 0).horizontal().vertical().rotate(),
        #             StilettoEntity(3, 2).horizontal(), EquilateralLEntity(4, 3).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), BigZEntity(2, 4).horizontal().rotate(),
        #             LackSmashEntity(5, 3).vertical().rotate(), StilettoEntity(0, 5).horizontal().vertical()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             LackSmashEntity(4, 0).horizontal().vertical().rotate(),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             BigZEntity(2, 4).vertical(), FullSmashEntity(0, 4).horizontal().rotate(),
        #             StilettoEntity(3, 2).horizontal(), EquilateralLEntity(4, 3).vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             BigZEntity(2, 4).horizontal(), EquilateralLEntity(4, 3).vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             BigZEntity(4, 2).horizontal().vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal(),
        #             LackSmashEntity(4, 4).horizontal()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(), ConvexEntity(2, 1).horizontal().rotate(),
        #             BigZEntity(4, 2).horizontal().vertical().rotate(), LackSmashEntity(4, 4).horizontal(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(3, 2).horizontal()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(),
        #             ConvexEntity(2, 3).horizontal().vertical().rotate(), FullSmashEntity(0, 4).vertical().rotate(),
        #             BigZEntity(4, 2).vertical().rotate(), LackSmashEntity(4, 0).horizontal().vertical().rotate(),
        #             StilettoEntity(1, 2)]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(),
        #             ConvexEntity(2, 3).horizontal().vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate(),
        #             LackSmashEntity(5, 2).horizontal().vertical().rotate(), StilettoEntity(1, 2)]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(),
        #             ConvexEntity(2, 3).horizontal().vertical().rotate(),
        #             LackSmashEntity(5, 2).horizontal().vertical().rotate(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(1, 2),
        #             EquilateralLEntity(4, 3).horizontal().vertical().rotate()]
        # entities = [BigLEntity(0, 0).rotate(), SunkenEntity(0, 1).rotate(),
        #             ConvexEntity(2, 3).horizontal().vertical().rotate(),
        #             BigZEntity(4, 2).horizontal().vertical().rotate(), LackSmashEntity(4, 4).horizontal(),
        #             FullSmashEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(1, 2)]

        entities = [
            BigZEntity(0, 0).rotate(),
            LackSmashEntity(0, 2).horizontal().vertical().rotate(),
            FullSmashEntity(5, 0).horizontal(),
            StilettoEntity(1, 0).horizontal().vertical().rotate(),
            EquilateralLEntity(4, 2).vertical().rotate(),
            ConvexEntity(4, 0).vertical().rotate(),
        ]
        for entity in entities:
            board.add_entity(entity)
            blocks.extend(entity.blocks)

        # 是否有多出的
        print(bool(set(blocks) - totals))

        # 是否有重复的
        print(len(blocks) == len(set(blocks)))

        # 是否能够匹配
        print(not bool(totals - set(blocks)))

        # 判断一独，二独，三独，四独
        print(self.validate_trap(totals - set(blocks)))

        # board.add_entity(BigLEntity())
        # board.add_entity(LackSmashEntity(2, 3))
        # board.add_entity(EquilateralL(2, 3))
        board.show()

    @staticmethod
    def get_around(block):
        surrounds = set()
        surrounds.add(Block(block.row + 1, block.col))
        surrounds.add(Block(block.row - 1, block.col))
        surrounds.add(Block(block.row, block.col + 1))
        surrounds.add(Block(block.row, block.col - 1))
        return surrounds

    def validate_trap(self, blocks):
        # 校验有独立的一个空，两个空，三个空，四个空的场景
        if not blocks:
            return True

        blocks = list(blocks)
        groups = []
        queue = Queue()

        while blocks:
            group = []
            block = blocks.pop()
            group.append(block)
            queue.put(block)

            while not queue.empty():
                block = queue.get()
                surrounds = self.get_around(block)
                exists = surrounds & set(blocks)
                for exist in exists:
                    group.append(exist)
                    queue.put(exist)
                    blocks.remove(exist)

            if len(group) < 5:
                return False
            groups.append(group)

        return True

    def check_one(self):
        entities = []
        board = Board()
        board.months.pop(self.month - 1)
        board.days.pop(self.day - 1)
        totals = set(board.months + board.days)

        entities.append(ConvexEntity().rotate().horizontal())
        entities.append(LackSmashEntity(0, 2).vertical())
        entities.append(StilettoEntity(0, 5).horizontal().vertical())
        entities.append(EquilateralLEntity(4, 0))
        entities.append(FullSmashEntity(1, 3).rotate())
        entities.append(BigZEntity(2, 1).rotate())
        entities.append(SunkenEntity(3, 3))
        entities.append(BigLEntity(3, 4).rotate().vertical())

        blocks = []
        for entity in entities:
            board.add_entity(entity)
            blocks.extend(entity.blocks)

        print(set(entities))
        print(totals)
        print(set(blocks))

        print(len(totals))
        print(len(blocks))
        print(len(set(blocks)))

        # 是否有多出的
        print(bool(set(blocks) - totals))

        # 是否有重复的
        print(len(blocks) != len(set(blocks)))

        # 是否能够匹配
        print(not bool(totals - set(blocks)))

        board.show()

    def check_other_one(self):
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal().vertical(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), FullSmashEntity(4, 1),
        #             StilettoEntity(2, 3), BigZEntity(4, 1).rotate(), LackSmashEntity(5, 3).rotate().vertical()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(2, 3),
        #             BigZEntity(4, 1).horizontal().vertical().rotate(), FullSmashEntity(4, 1),
        #             LackSmashEntity(5, 3).vertical().rotate()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(2, 3),
        #             FullSmashEntity(4, 1).horizontal().vertical(), LackSmashEntity(5, 3).vertical().rotate(),
        #             BigZEntity(4, 1).rotate()]
        # entities = [BigLEntity(0, 0), SunkenEntity(0, 3).horizontal(), ConvexEntity(1, 0).rotate(),
        #             EquilateralLEntity(0, 4).horizontal().vertical().rotate(), StilettoEntity(2, 3),
        #             FullSmashEntity(4, 1), LackSmashEntity(5, 3).vertical().rotate(), BigZEntity(4, 1).rotate()]
        entities = [
            BigLEntity(0, 0),
            SunkenEntity(0, 3).horizontal(),
            ConvexEntity(1, 0).rotate(),
            EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
            StilettoEntity(2, 3),
            FullSmashEntity(4, 1),
            LackSmashEntity(5, 3).vertical().rotate(),
            BigZEntity(4, 1).rotate(),
        ]
        board = Board()
        board.months.pop(self.month - 1)
        board.days.pop(self.day - 1)
        totals = set(board.months + board.days)

        blocks = []
        for entity in entities:
            board.add_entity(entity)
            blocks.extend(entity.blocks)

        print(set(entities))
        print(totals)
        print(set(blocks))

        print(len(totals))
        print(len(blocks))
        print(len(set(blocks)))

        # 是否有多出的
        print(bool(set(blocks) - totals))

        # 是否有重复的
        print(len(blocks) != len(set(blocks)))

        # 是否能够匹配
        print(not bool(totals - set(blocks)))

        board.show()


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # Solution(2, 2).check_one()
    # app.exec()
    # Solution(10, 2).check_other_one()
    Solution(5, 1).solute()
    # Solution(2, 3).solve()
