# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 14:35

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import json
import os

CONFIG_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "common", "config.json"))
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as w:
        json.dump({
            "log_path": "./",
            "is_save_log": False,
            "checkpoint_dir_path": "./"
        }, w, ensure_ascii=False, indent="\t")

from .base.base import BaseCrawl
from .base.base_container import Container, RowContainer
from .common.config import Config

__version__ = '0.1'
__all__ = ['BaseCrawl',
           'Container',
           'RowContainer',
           'Config'
           ]
