Configurable parameters 可配置参数说明
============================================


以下参数可通过 ``Config`` 类的 ``set`` 方法进行设置：

- ``checkpoint_dir_path``: checkpoint存放位置
- ``is_save_log``: 是否保存日志
- ``log_path``: 日志保存路径

.. code-block:: python

    from tinyCrawl import Config
    # 实例化配置对象
    config = Config()
    # is_save_log默认不保存日志，即is_save_log为False，这里设置成True,即`保存日志`
    config.set("is_save_log", True)
    # 设置日志保存路径
    config.set("log_path", "D:/log")

