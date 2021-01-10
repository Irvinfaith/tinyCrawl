# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 14:44

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
from collections import OrderedDict


class Container(list):
    container = OrderedDict()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        super().__init__()

    @classmethod
    def clear(cls):
        """
        Clear the data stored in the container.

        """
        cls.container.clear()


class RowContainer(Container):
    __call_index = 0

    def __new__(cls, *args, **kwargs):
        # 创建list实例
        __instance = super().__new__(cls, *args, **kwargs)
        # 更新container dict对象
        if args:
            if len(args) > 1:
                raise KeyError("RowContainer only take 1 arguement. You pass into `%d` args" % len(args))
            # 名称若存在，直接返回实例
            if args[0] in Container.container.keys():
                return Container.container[args[0]]
            # 否则新建，更新container
            else:
                Container.container.update({args[0]: __instance})
        else:
            Container.container.update({"RowContainer" + str(cls.__call_index): __instance})
        # 更新index
        cls.__call_index += 1
        return __instance

    def __init__(self, name=None):
        if name:
            # 若传参了名称，且名称不存在，则初始化父类list对象，否则不初始化
            if name not in Container.container.keys():
                super().__init__()
        else:
            super().__init__()
