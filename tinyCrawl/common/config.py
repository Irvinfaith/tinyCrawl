# -*- coding: utf-8 -*-
"""
Created on 2020/11/26 10:14

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import os
import json
import importlib
from types import ModuleType

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')


class Config(dict):
    def __init__(self):
        with open(CONFIG_PATH, "r") as w:
            s = w.readlines()
        super().__init__(json.loads(''.join([i.strip() for i in s])))

    def __getattr__(self, item):
        from ..utils.utils import mkdirs
        if 'path' in item:
            mkdirs(self[item])
        return self[item]

    def __setitem__(self, key, value):
        if key not in self.keys():
            raise ValueError("Invalid key `{}`".format(key))
        super().__setitem__(key, value)
        with open(CONFIG_PATH, "w") as w:
            json.dump(self, w, ensure_ascii=False, indent="\t")
        _reload_all(__import__("tinyCrawl"))

    def set(self, key, value):
        """Set global parameters.

            Now has three parameters could be set.

            - ``checkpoint_dir_path``: Path of checkpoint file

            - ``is_save_log``: Whether to save log files

            - ``log_path``: Path of log files

        Args:
            key(str): Name of parameter
            value(str or bool): Value to be set

        Returns:

        """
        self.__setitem__(key, value)


def __walk_module(module, map):
    if module not in map:
        map[module] = None
        importlib.reload(module)
        module_dict = module.__dict__
        for attr in module_dict:
            if "tinyCrawl" not in str(module_dict[attr]):
                continue
            # 如果词典中有其他模块的话,递归处理
            if isinstance(module_dict[attr], ModuleType):
                __walk_module(module_dict[attr], map)


def _reload_all(*modules):
    visited_map = {}
    for module in modules:
        if isinstance(module, ModuleType):
            __walk_module(module, visited_map)
