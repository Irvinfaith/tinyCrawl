How to use 如何使用
============================================


tinyCrawl 支持2种运行方法

- 函数式：定义爬虫的方法 task()，实例化 ``BaseCrawl(iter_url, iter_num_range, thread_num)`` 后，调用其 ``run`` 方法，以 ``task对象`` 作为参数执行
- 继承式：继承 ``BaseCrawl(iter_url, iter_num_range, thread_num)`` ，重写 ``crawl()`` 和 ``sink()`` 方法，其中 ``crawl()`` 类似于上一方法中的爬虫方法task()，定义爬取单页的爬虫代码， ``sink()`` 是将结果输出的方法，最后执行 ``main()`` 方法执行总程序

函数式
--------

.. code-block:: python

    from tinyCrawl import BaseCrawl, RowContainer

    from urllib.request import urlopen
    from lxml import etree

    # 定义xpath
    song_name_xpath = '//div[@class="song-name"]/a/text()'
    singer_xpath = '//div[@class="singers"]/a[1]/text()'
    album_xpath = '//div[@class="album"]/a[1]/text()'

    def task(url):
        """
        定义爬取单页的爬虫代码

        """
        # 定义数据存放的容器，容器名字就是最后爬取结果存放字典的self.out的key
        song_name_list = RowContainer("song name")
        singer_list = RowContainer("singer")
        album_list = RowContainer("album")

        page = urlopen(url).read().decode("utf-8", 'ignore')
        parse = etree.HTML(page)
        for _song_name, _singer, _album in zip(parse.xpath(song_name_xpath),
                                               parse.xpath(singer_xpath),
                                               parse.xpath(album_xpath)):
            # 将数据append进指定容器中
            song_name_list.append(str(_song_name))
            singer_list.append(str(_singer))
            album_list.append(str(_album))

    if __name__ == '__main__':
        # 第一个参数是链接地址，需通过 %s 定义页数等迭代的参数
        # 第二个参数是迭代的范围，
        # 第三个参数是启用的线程数，大于1就是多线程，等于1就是单线程
        bc = BaseCrawl("http://example.com/?page=%s", range(1, 5), 3)
        # 输入task的对象，开始执行程序
        bc.run(task)
        # 执行完毕后，通过out属性，获取结果
        print(bc.out)

继承式
-------------

.. code-block:: python

    from tinyCrawl import BaseCrawl, RowContainer
    from urllib.request import urlopen
    from lxml import etree
    import pandas as pd

    # 需继承BaseCrawl类，覆写crawl和sink方法
    class Scratch(BaseCrawl):
        def __init__(self, iter_url, iter_num_range, thread_num):
            super().__init__(iter_url, iter_num_range, thread_num)

        # 覆写crawl方法
        def crawl(self, url):
        # 定义数据存放的容器，容器名字就是最后爬取结果存放字典的self.out的key
        song_name_list = RowContainer("song name")
        singer_list = RowContainer("singer")
        album_list = RowContainer("album")

        page = urlopen(url).read().decode("utf-8", 'ignore')
        parse = etree.HTML(page)
        for _song_name, _singer, _album in zip(parse.xpath(song_name_xpath),
                                               parse.xpath(singer_xpath),
                                               parse.xpath(album_xpath)):
            # 将数据append进指定容器中
            song_name_list.append(str(_song_name))
            singer_list.append(str(_singer))
            album_list.append(str(_album))

        # 覆写sink方法，将爬取的结果输出
        def sink(self):
            # self.out是字典结构的结果，可以直接输入pandas存为dataframe
            recent_music = pd.DataFrame(self.out)
            recent_music.to_csv("D:/tmptest.csv", index=0)


    if __name__ == '__main__':
        mc = Scratch("http://example.com/?page=%s", range(1, 5), 3)
        # 调用main函数执行程序
        mc.main()

output:

.. code-block:: bash

    2021-01-10 16:18:36,944 - base.py - __init__ - [line:30] - INFO: Checkpoint path: D:\breakpoint_page.txt
    2021-01-10 16:18:38,539 - base.py - __source - [line:119] - INFO: Now is running on multithread mode, total thread num is `3`
    2021-01-10 16:18:38,539 - base.py - __source - [line:126] - INFO: Total iteration num: 4
    2021-01-10 16:18:38,541 - base.py - _multi_thread_wrap - [line:59] - INFO: ThreadPoolExecutor-1_0 now is processing: http://example.com/?page=1
    2021-01-10 16:18:38,541 - base.py - _multi_thread_wrap - [line:59] - INFO: ThreadPoolExecutor-1_1 now is processing: http://example.com/?page=2
    2021-01-10 16:18:38,542 - base.py - _multi_thread_wrap - [line:59] - INFO: ThreadPoolExecutor-1_2 now is processing: http://example.com/?page=3
    2021-01-10 16:18:41,544 - base.py - __task_done - [line:115] - INFO: ThreadPoolExecutor-1_1 task finished; (Time took: 3.0009s)
    2021-01-10 16:18:41,544 - base.py - __task_done - [line:115] - INFO: ThreadPoolExecutor-1_0 task finished; (Time took: 3.0019s)
    2021-01-10 16:18:41,544 - base.py - __task_done - [line:115] - INFO: ThreadPoolExecutor-1_2 task finished; (Time took: 3.0009s)
    2021-01-10 16:18:41,545 - base.py - _multi_thread_wrap - [line:59] - INFO: ThreadPoolExecutor-1_1 now is processing: http://example.com/?page=4
    2021-01-10 16:18:44,551 - base.py - __task_done - [line:115] - INFO: ThreadPoolExecutor-1_1 task finished; (Time took: 3.0022s)
    2021-01-10 16:18:44,551 - base.py - __source - [line:151] - INFO: All done. (Time took: 6.0102s)
