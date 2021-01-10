# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 21:34

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
from tinyCrawl import BaseCrawl, RowContainer


class Scratch(BaseCrawl):
    def __init__(self, iter_url, iter_num_range, thread_num):
        super().__init__(iter_url, iter_num_range, thread_num)

    def crawl(self, url):
        tmp = RowContainer("tmp")
        with open(url) as f:
            d = [i.strip() for i in f.readlines()]
        for _ in d:
            tmp.append(_)

    def sink(self):
        print(self.out)

def test_implement():
    mc = Scratch("../examples/test_files/%s.txt", range(1, 5), 3)
    mc.main()