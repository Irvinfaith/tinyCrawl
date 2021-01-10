# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 15:35

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import time
from tinyCrawl import BaseCrawl, RowContainer

def task(url):
    tmp = RowContainer("tmp")
    with open(url) as f:
        d = [i.strip() for i in f.readlines()]
    for _ in d:
        tmp.append(_)
    time.sleep(3)

bc = BaseCrawl("./test_files/%s.txt", range(1, 5), 3)
bc.run(task)