# -*- coding: utf-8 -*-
"""
Created on 2021/1/7 13:36

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import os
import queue
import threading
import time
from collections import OrderedDict
from concurrent.futures.thread import ThreadPoolExecutor

from tinyCrawl.common.config import Config
from tinyCrawl.base.base_container import Container
from tinyCrawl.utils.logger import LogConfig

logger = LogConfig(__file__).logger
CONFIG = Config()


class BaseCrawl:
    def __init__(self, iter_url, iter_num_range, thread_num):
        """

        Args:
            iter_url(str): Formatted string, usually it is a url like: "http://example.com/?page=%s",
                        using `%s` to pass the iterable parameter.
            iter_num_range: Object has iterable property, which means has `__iter__` attribution, exp: list or range
            thread_num(int): Thread number of the program, set `1` means single-thread, set larger than 1 means multi-thread.
        """

        checkpoint_dir_path = CONFIG["checkpoint_dir_path"]
        self.checkpoint_path = os.path.join(os.path.realpath(checkpoint_dir_path), 'checkpoint.txt')
        logger.info("Checkpoint path: " + self.checkpoint_path)
        log_path = CONFIG["log_path"]
        is_save_log = CONFIG["is_save_log"]
        if is_save_log:
            logger.info("Log file is saving at path: " + os.path.realpath(log_path))
        self.iter_url = iter_url
        self.iter_num_range = iter_num_range
        self.iter_result = []
        self.out = OrderedDict()
        self.thread_num = thread_num
        if self.thread_num > 1:
            self.multi = True
            self.queue = queue.Queue(thread_num)
        elif self.thread_num == 1:
            self.multi = False
        else:
            raise KeyError("`thread_num` can not set a value less than `1`")

    def crawl(self, *args, **kwargs):
        """Crawling task function, need to be implemented.

        """
        raise NotImplementedError

    def sink(self):
        """Output the crawling result, need to be implemented.

        """
        raise NotImplementedError

    def run(self, obj):
        """Adding a crawling function into the class

        Args:
            obj: An crawling function object

        """
        self.crawl = obj
        self.__source(self.iter_url, self.iter_num_range)

    def _multi_thread_wrap(self, obj, value):
        logger.info("%s now is processing: %s" % (threading.current_thread().name, value))
        self.__checkpoint(method='w', status='unfinished', page=str(value))
        start_time = time.time()
        obj(value)
        return start_time

    def __checkpoint(self, method, status=None, page=None):
        if method == 'w':
            with open(self.checkpoint_path, 'w+') as w:
                if page is None:
                    w.write(status + '\n')
                else:
                    w.write(status + '\n' + str(page))
        if method == 'r':
            if os.path.exists(self.checkpoint_path):
                with open(self.checkpoint_path, 'r+') as w:
                    a = [i.strip() for i in w.readlines()]
            else:
                a = None
            return a

    def __check_status(self):
        status = self.__checkpoint(method='r')
        if not status:
            self.__run(flush=True)
        elif status[0] == 'unfinished':
            self.__run(flush=False)
        elif status[0] == 'finished':
            self.__run(flush=True)

    def __run(self, flush):
        if flush:
            self.__source(self.iter_url, self.iter_num_range)
        else:
            checkpoint = int(self.__checkpoint(method='r')[1])
            logger.info("Found checkpoint: iteration start from %d" % checkpoint)
            self.__source(self.iter_url, range(checkpoint, self.iter_num_range.stop, self.iter_num_range.step))

    def __add_into_queue(self, iter_url, iter_num_range):
        iter_generater = self.__get_iter(iter_url, iter_num_range)
        while 1:
            try:
                value = next(iter_generater)
                self.queue.put(value)
            except StopIteration:
                break

    @staticmethod
    def __get_iter(iter_url, iter_num_range):
        for iter_num in iter_num_range:
            yield iter_url % str(iter_num)

    @staticmethod
    def __task_done(future):
        start_time = future.result()
        current_thread = threading.current_thread().name
        logger.info(current_thread + " task finished; (Time took: %.4fs)" % (time.time() - start_time))

    def __source(self, iter_url, iter_num_range: range):
        if self.multi:
            logger.info("Now is running on multithread mode, total thread num is `%d`" % self.thread_num)
        else:
            logger.info("Now is running on single-thread mode, you can run as multithread mode by setting `thread_num`")
        # 替换%转义
        iter_url = iter_url.replace("%", "%%").replace("%%s", "%s")
        self.out = Container.container
        total_iter = len(iter_num_range)
        logger.info("Total iteration num: %d" % total_iter)
        __t1 = time.time()
        if self.multi:
            put_into_queue = threading.Thread(target=self.__add_into_queue, args=(iter_url, iter_num_range))
            put_into_queue.setDaemon(True)
            put_into_queue.start()
            pool = ThreadPoolExecutor(self.thread_num)

            while not self.queue.empty():
                value = self.queue.get()
                done = pool.submit(self._multi_thread_wrap, self.crawl, value)
                done.add_done_callback(self.__task_done)
            put_into_queue.join()
            pool.shutdown(wait=True)
        else:
            for index, iter_num in enumerate(iter_num_range):
                logger.info(
                    "Start crawling iteration num: %d; (%d iteration left)" % (iter_num, total_iter - index - 1))
                self.__checkpoint(method='w', status='unfinished', page=str(iter_num))
                url = iter_url % str(iter_num)
                # 主爬取程序
                __t2 = time.time()
                self.crawl(url)
                logger.info("End crawling iteration num: %d; (Time took: %.4fs)" % (iter_num, time.time() - __t2))

        logger.info("All done. (Time took: %.4fs)" % (time.time() - __t1))
        self.__checkpoint(method='w', status='finished')

    def main(self):
        """
        Main function to excute `crawl` and `sink` function.

        """
        self.__source(self.iter_url, self.iter_num_range)
        self.sink()
