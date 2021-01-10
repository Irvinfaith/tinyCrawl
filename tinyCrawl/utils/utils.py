# -*- coding: utf-8 -*-
"""
Created on 2021/1/8 10:24

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import os
import re

from ..utils.logger import LogConfig

logger = LogConfig(__file__).logger


def is_abs_path(path, return_abs_path=False):
    is_abs = False
    if not os.path.isabs(path):
        logger.info("Path is not absolute path")
        dir_path = os.path.abspath(path)
    else:
        is_abs = True
        dir_path = path
    logger.info("Absolute path: " + dir_path)
    if return_abs_path:
        return is_abs, dir_path
    else:
        return is_abs


def is_file_path(path, return_dir_path=False):
    """判断路径是文件路径还是目录路径，并可返回目录路径

    Args:
        path(str): 路径地址
        return_dir_path(bool): 是否返回目录路径

    Returns:
        str: 目录路径
    """
    is_file = False
    # 判断path是否为文件
    if '.' in re.split('[\/\\\\]', path)[-1]:
        is_file = True
    if return_dir_path:
        if is_file:
            return is_file, os.path.abspath(os.path.dirname(path))
        else:
            return is_file, os.path.abspath(path)
    return is_file


def mkdirs(path, return_path=False):
    """根据路径判断是否创建dir，并可返回绝对路径

    Args:
        path(str): 绝对路径/相对路径/文件路径
        return_path(bool): 是否返回绝对路径

    Returns:
        str: 绝对路径
    """
    is_abs, abs_path = is_abs_path(path, return_abs_path=True)
    is_file, dir_path = is_file_path(path, return_dir_path=True)
    if not os.path.exists(abs_path):
        logger.info("Current path dose not exists.")
        if is_file:
            os.makedirs(dir_path)
            logger.info("Absolute path dirs created: " + dir_path)
        else:
            os.makedirs(abs_path)
            logger.info("Absolute path dirs created: " + abs_path)
    else:
        logger.info("Current path exists: " + os.path.abspath(dir_path))
    if return_path:
        return abs_path
