# -*- coding: utf-8 -*-
import random

import time

from puzzle import *


class ForSolution(Solution):
    def solve(self):
        board = Board()

        month_block = board.months[self.month - 1]
        day_block = board.days[self.day - 1]
        board.draw_block(month_block.col, month_block.row, TARGET_COLOR, month_block.__class__.__name__)
        board.draw_block(day_block.col, day_block.row, TARGET_COLOR, str(self.day))
        board.months.remove(month_block)
        board.days.remove(day_block)

        totals = set(board.months + board.days)

        result = []
        calculated = 0

        def traceback(classes, entities, entity_filled):
            if not classes:
                return

            nonlocal calculated
            # if calculated % 1000000 == 0:
            #     print("{}:{}".format(calculated, entities))
            entity_class = classes.pop()
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
                                entity_filled_set = set(entity_filled)

                                # 有超出的
                                if entity_filled_set - totals:
                                    # print("overflow")
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)
                                    continue

                                # 有重复的
                                if len(entity_filled) != len(entity_filled_set):
                                    # print("duplicate")
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)
                                    continue

                                left_blocks = totals - entity_filled_set
                                # 有成功
                                if not left_blocks:
                                    print("success in:%d" % calculated)
                                    print(entities)
                                    result.append(entities)
                                    return entities

                                # 有空洞
                                if not self.validate_trap(left_blocks):
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

            classes.append(entity_class)

        random.shuffle(self.entity_classes)

        print(time.ctime())
        success_entities = traceback(self.entity_classes, [], [])
        print(calculated)
        print(len(result))
        print(success_entities)
        print(time.ctime())

        # print(len(result))
        for success in success_entities:
            board.add_entity(success)
        board.show()

    def solute(self, entities=None):

        # 2-2
        # entities = [SunkenEntity(0, 0), ConvexEntity(0, 2).horizontal().rotate(),
        #             StilettoEntity(0, 5).horizontal().rotate(), EquilateralLEntity(3, 4), FullSmashEntity(0, 3),
        #             LackSmashEntity(5, 2).horizontal().vertical().rotate(), BigZEntity(1, 3).vertical().rotate(),
        #             BigLEntity(2, 2).horizontal().rotate()]

        # 5-1
        entities = [
            BigZEntity(0, 0).rotate(),
            LackSmashEntity(5, 2).rotate(),
            FullSmashEntity(5, 0),
            StilettoEntity(0, 4).vertical(),
            EquilateralLEntity(0, 1).horizontal().vertical(),
            ConvexEntity(2, 0),
            SunkenEntity(4, 4),
            BigLEntity(0, 4).rotate(),
        ]
        board = Board()

        # 2-3
        entities = [
            SunkenEntity(0, 0),
            ConvexEntity(0, 3).horizontal().vertical().rotate(),
            StilettoEntity(1, 5).vertical().rotate(),
            EquilateralLEntity(2, 3).vertical(),
            FullSmashEntity(0, 3),
            LackSmashEntity(2, 2).horizontal().vertical(),
            BigZEntity(2, 0),
            BigLEntity(2, 5).vertical(),
        ]

        # 10-7
        # entities = [SunkenEntity(0, 0).horizontal(), ConvexEntity(1, 0), StilettoEntity(0, 5).horizontal().rotate(),
        #             EquilateralLEntity(0, 3).horizontal().rotate(), FullSmashEntity(5, 3).rotate(),
        #             LackSmashEntity(0, 3).vertical(), BigZEntity(1, 3).vertical().rotate(),
        #             BigLEntity(2, 4).horizontal()]

        # 10-1
        entities = [
            SunkenEntity(0, 0).horizontal(),
            ConvexEntity(0, 1).vertical().rotate(),
            StilettoEntity(1, 4).horizontal().vertical(),
            EquilateralLEntity(0, 3).horizontal().vertical(),
            FullSmashEntity(2, 2).rotate(),
            LackSmashEntity(0, 4).vertical().rotate(),
            BigZEntity(2, 4).vertical().rotate(),
            BigLEntity(2, 5).vertical(),
        ]

        # 10-2
        entities = [
            SunkenEntity(0, 1).horizontal().rotate(),
            ConvexEntity(0, 0).horizontal().vertical(),
            StilettoEntity(0, 5).horizontal().vertical(),
            EquilateralLEntity(0, 2).vertical(),
            FullSmashEntity(3, 3),
            LackSmashEntity(5, 0).horizontal().vertical(),
            BigZEntity(0, 3).vertical().rotate(),
            BigLEntity(3, 4).vertical().rotate(),
        ]

        # 10-4
        entities = [
            SunkenEntity(0, 0).horizontal().rotate(),
            ConvexEntity(0, 2).horizontal().vertical(),
            StilettoEntity(1, 4).vertical(),
            EquilateralLEntity(0, 4).vertical().rotate(),
            FullSmashEntity(0, 3).rotate(),
            LackSmashEntity(5, 2).horizontal().vertical().rotate(),
            BigZEntity(1, 1),
            BigLEntity(3, 4).horizontal().vertical().rotate(),
        ]
        entities = [
            BigZEntity(0, 0),
            BigLEntity(0, 3).vertical().rotate(),
            FullSmashEntity(5, 0),
            ConvexEntity(4, 3),
            LackSmashEntity(5, 2).horizontal().vertical().rotate(),
            EquilateralLEntity(0, 1).horizontal().vertical().rotate(),
            StilettoEntity(0, 4).horizontal(),
            SunkenEntity(0, 2).horizontal(),
        ]

        # 10-3
        entities = [
            ConvexEntity(0, 0).horizontal().vertical(),
            BigZEntity(0, 3).vertical(),
            FullSmashEntity(0, 1).rotate(),
            SunkenEntity(4, 1),
            LackSmashEntity(4, 4).horizontal(),
            BigLEntity(2, 3).horizontal().rotate(),
            StilettoEntity(1, 5),
            EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
        ]

        # 10-5
        entities = [
            LackSmashEntity(0, 3).vertical(),
            ConvexEntity(1, 0),
            SunkenEntity(0, 0).horizontal(),
            BigZEntity(1, 3).vertical().rotate(),
            EquilateralLEntity(0, 3).horizontal().rotate(),
            FullSmashEntity(4, 3).rotate(),
            BigLEntity(2, 5).horizontal().vertical(),
            StilettoEntity(0, 5).horizontal().rotate(),
        ]

        # 10-8
        entities = [
            StilettoEntity(0, 0).horizontal().vertical(),
            ConvexEntity(1, 3).vertical().rotate(),
            SunkenEntity(0, 4).horizontal().rotate(),
            EquilateralLEntity(1, 4),
            LackSmashEntity(0, 1),
            BigZEntity(0, 4),
            FullSmashEntity(4, 4),
            BigLEntity(2, 2).horizontal().vertical(),
        ]

        entities = [
            StilettoEntity(0, 5).horizontal().vertical(),
            ConvexEntity(0, 0).horizontal(),
            SunkenEntity(1, 0).vertical(),
            EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
            LackSmashEntity(4, 1).horizontal().vertical(),
            BigZEntity(1, 2).vertical().rotate(),
            FullSmashEntity(4, 4).horizontal(),
            BigLEntity(0, 4),
        ]
        entities = [
            StilettoEntity(0, 0).horizontal().vertical(),
            ConvexEntity(3, 1).vertical().rotate(),
            SunkenEntity(2, 2).horizontal().vertical().rotate(),
            EquilateralLEntity(0, 4).horizontal().vertical().rotate(),
            LackSmashEntity(0, 1),
            BigZEntity(0, 4).horizontal().vertical(),
            FullSmashEntity(5, 3).vertical().rotate(),
            BigLEntity(1, 4).horizontal().vertical().rotate(),
        ]
        month_block = board.months[self.month - 1]
        day_block = board.days[self.day - 1]
        board.draw_block(month_block.col, month_block.row, TARGET_COLOR, month_block.__class__.__name__)
        board.draw_block(day_block.col, day_block.row, TARGET_COLOR, str(self.day))
        board.months.remove(month_block)
        board.days.remove(day_block)
        totals = set(board.months + board.days)

        blocks = []
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

        board.show()


if __name__ == '__main__':
    # ForSolution(2, 2).solute()
    # ForSolution(5, 1).solve()
    # ForSolution(5, 1).solute()
    # ForSolution(2, 3).solute()
    # ForSolution(10, 7).solute()
    ForSolution(10, 8).solute()
