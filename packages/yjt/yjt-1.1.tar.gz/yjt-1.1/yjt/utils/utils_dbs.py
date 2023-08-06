# -*-coding:utf-8 -*-

"""
# Time       ：2021/10/19 11:39
# Author     ：AMU
# Description：数据库相关辅助方法
"""
import datetime
from typing import Union
from sqlalchemy.engine import Row
from itertools import chain


def row_to_dict(row: Union[list, Row]):
    """
    将返回数据元组(sqlalchemy.engine.result.RowProxy)转为字典

    :param row: 原始数据
    :return:
    """
    if row:
        if isinstance(row, list):
            return [dict(zip(result.keys(), result)) for result in row]
        else:
            return dict(zip(row.keys(), row))
    else:
        return None


def row_to_list(row):
    if row:
        if len(row[0]) == 1:
            return list(chain.from_iterable(row))
        else:
            return [list(r) for r in row]
    else:
        return []


def datetime_to_str(raw: Union[list, dict], f: str = '%Y-%m-%d %H:%M:%S'):
    """
    将数据字典中的时间数据转为字符串

    :param raw: 原始数据
    :param f: 输出的时间字符串格式
    :return:
    """
    if isinstance(raw, list):
        for item in raw:
            for k in item:
                if isinstance(item[k], datetime.datetime):
                    item[k] = item[k].strftime(f)

    elif isinstance(raw, dict):
        for k in raw:
            if isinstance(raw[k], datetime.datetime):
                raw[k] = raw[k].strftime(f)

    return raw
