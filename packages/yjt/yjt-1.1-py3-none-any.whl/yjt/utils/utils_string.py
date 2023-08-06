# -*-coding:utf-8 -*-

"""
# Time       ：2022/5/5 12:04
# Author     ：AMU
# Description：字符串处理相关
"""
import re
from typing import List, Union
from collections import OrderedDict


def tag_format(
        raw: Union[str, List[Union[str, int, float]]],
        fmt: str,
        to_number: bool = False,
        delimiter: str = ','
) -> Union[str, List[Union[str, int, float]]]:
    """
    标签型数据格式处理

    :param raw: 原始数据
    :param fmt: 目标格式 list|str_show|str_database
    :param to_number: 目标形式为list时, 数字型字符串是否转化为 int|float
    :param delimiter: 分隔符, 默认","
    :return:
    """
    if fmt == 'list':
        if isinstance(raw, str):
            return tag_format_to_list(raw=raw, to_number=to_number, delimiter=delimiter)
        else:
            raise RuntimeError('fn:tag_format(fmt=list) 原始数据类型不正确')

    if fmt in ['str_show', 'str_database']:
        if isinstance(raw, list):
            tmp = tag_format_to_str(raw=raw, delimiter=delimiter)
            if fmt == 'str_database':
                return tmp
            else:
                return tmp.strip(delimiter)
        else:
            raise RuntimeError('fn:tag_format(fmt=str_show|str_database) 原始数据类型不正确')

    raise RuntimeError('fn:tag_format(fmt) 目标格式不正确')


# noinspection PyBroadException
def tag_format_to_list(
        raw: str,
        to_number: bool = False,
        delimiter: str = ','
) -> List[Union[str, int, float]]:
    """
    字符串 转 数组

    * tag数据(字符串)规则: 元素不重复，元素不为空，元素两边无空，元素以英文逗号分隔
    """
    if raw:
        arr = raw.split(delimiter)  # 使用delimiter分隔成list
        arr = [item.strip() for item in arr if item.strip()]  # 元素两边去空，并去除空元素
        arr = list(OrderedDict.fromkeys(arr))  # 去重
        if to_number:
            for i, v in enumerate(arr):
                if re.match(r'^[\d|.]+$', v):
                    try:
                        arr[i] = int(v)
                    except:
                        try:
                            arr[i] = float(v)
                        except:
                            pass

    else:
        arr = []

    return arr


def tag_format_to_str(
        raw: List[Union[str, int, float]],
        delimiter: str = ','
) -> str:
    """
    数组 转 字符串

    * tag数据(字符串)规则: 元素不重复，元素不为空，元素两边无空，元素以英文逗号分隔，首尾为英文逗号
    """
    arr = [str(item).strip() for item in raw if str(item).strip()]  # 元素两边去空，并去除空元素
    arr = list(OrderedDict.fromkeys(arr))  # 去重
    if arr:
        tmp = delimiter.join(arr)
        return f'{delimiter}{tmp}{delimiter}'
    else:
        return ''
