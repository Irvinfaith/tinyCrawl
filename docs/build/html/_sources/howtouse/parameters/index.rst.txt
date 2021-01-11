Main parameters主要参数说明
============================


iter_url 可传递参数的链接
----------------------------

``BaseCrawl`` 类中的 ``iter_url`` 参数，是一个带格式化输出的链接：

.. code-block:: python

    iter_url = "http://example.com/?page=%s"

其中 ``%s`` 是python中的格式化输出的方法，使用过程中，将需遍历的参数（多为页数）置为 ``%s`` ，以让程序内部进行参数的迭代


iter_num_range 迭代参数
---------------------------

``BaseCrawl`` 类中的 ``iter_num_range`` 参数，是一个可迭代的的对象，即含 ``__iter__`` 属性的对象：：

例如range，list等迭代器

.. code-block:: python

    iter_num_range = range(1, 6, 1)

或者：

.. code-block:: python

    iter_num_range = [1, 2, 3, 4, 5]


即迭代的参数是从1到5的连续数列，通常是指爬取的页数，需要爬取从1到5页的内容。


thread_num 线程数
--------------------------

``BaseCrawl`` 类中的 ``thread_num`` 参数，定义线程数的参数：

thread_num=1即为单线程爬取，thread_num > 1即为多线程爬取



