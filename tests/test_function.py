# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 21:29

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
from tinyCrawl import BaseCrawl, RowContainer

def test_function():
    def task(url):
        tmp = RowContainer("tmp")
        with open(url) as f:
            d = [i.strip() for i in f.readlines()]
        for _ in d:
            tmp.append(_)
    bc = BaseCrawl("../examples/test_files/%s.txt", range(1, 5), 3)
    bc.run(task)