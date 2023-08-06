# -*-coding:utf-8 -*-

"""
# Time       ：2022/3/2 17:07
# Author     ：AMU
# Description：MD5相关方法
"""

import hashlib


def md5(raw):
    """
    返回指定字符串的 md5 值

    :param raw:
    :return:
    """
    if isinstance(raw, str):
        return hashlib.md5(raw.encode(encoding='UTF-8')).hexdigest()
    elif isinstance(raw, (int, float, complex)):
        return hashlib.md5(str(raw).encode(encoding='UTF-8')).hexdigest()
    else:
        return False
