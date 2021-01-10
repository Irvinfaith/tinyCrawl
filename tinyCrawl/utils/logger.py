# -*- coding: utf-8 -*-
"""
Created on 2021/1/8 10:21

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import logging
import os


class LogConfig(object):
    from ..common.config import Config
    CONFIG = Config()

    @classmethod
    def set_log_path(cls, log_path):
        cls.CONFIG.set("log_path", log_path)

    @classmethod
    def set_is_save(cls, is_save):
        cls.CONFIG.set("is_save_log", is_save)

    def __init__(self, name, level='info'):
        self.log_dir_path = LogConfig.CONFIG['log_path']
        self.is_save_log = LogConfig.CONFIG['is_save_log']
        print(self.log_dir_path)
        print(self.is_save_log)
        level_relations = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'crit': logging.CRITICAL
        }
        self.logger = logging.getLogger(name)
        # 设置日志格式
        fmt = '%(asctime)s - %(filename)s - %(funcName)s - [line:%(lineno)d] - %(levelname)s: %(message)s'
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(level_relations[level])
        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 把对象加到logger里
        if not self.logger.handlers:
            self.logger.addHandler(sh)
        if self.is_save_log:
            if not os.path.exists(self.log_dir_path):
                os.makedirs(self.log_dir_path)
            if level == 'error':
                path = os.path.join(self.log_dir_path, 'error.log')
            else:
                path = os.path.join(self.log_dir_path, 'all.log')
            # self.logger = logging.getLogger(path)
            # 往文件里写入#指定间隔时间自动生成文件的处理器
            th = logging.FileHandler(filename=path, mode="a", encoding='utf-8')
            # 设置文件里写入的格式
            th.setFormatter(format_str)
            if not self.logger.handlers:
                self.logger.addHandler(th)
            elif len(self.logger.handlers) == 1 and (not isinstance(self.logger.handlers[0], logging.FileHandler)):
                self.logger.addHandler(th)
            elif len(self.logger.handlers) > 1:
                self.logger.handlers = [i for i in self.logger.handlers if not isinstance(i, logging.FileHandler)]
                self.logger.addHandler(th)
        else:
            self.logger.handlers = [i for i in self.logger.handlers if not isinstance(i, logging.FileHandler)]


