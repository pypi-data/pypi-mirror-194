# -*-coding:utf-8 -*-

"""
# Time       ：2022/4/29 20:35
# Author     ：AMU
# Description：类单例装饰器
"""

import threading


def single(cls):
    """
    单例装饰器方法

    :param cls:
    :return:
    """
    _s_instance = {}
    _s_lock = threading.Lock()

    def __single(*args, **kwargs):
        if cls not in _s_instance:
            with _s_lock:
                if cls not in _s_instance:
                    _s_instance[cls] = cls(*args, **kwargs)
        return _s_instance[cls]

    return __single
