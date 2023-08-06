# -*-coding:utf-8 -*-

"""
# Time       ：2022/1/4 17:20
# Author     ：AMU
# Description：PIL图像处理工具
"""

from PIL import Image, ImageFilter


def image_resize(im, w=None, h=None):
    """
    缩放加剪切

    :param im:
    :param w:
    :param h:
    :return:
    """
    if not w and not h:
        print('not')
        return im

    # 锐化
    # im = im.filter(ImageFilter.SHARPEN)

    # 原图尺寸
    org_w, org_h = im.size

    # 没有定义宽
    if not w:
        new_h = int(h)
        new_w = round(new_h * (org_w / org_h))
        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        return im

    # 没有定义高
    if not h:
        new_w = int(w)
        new_h = round(new_w / (org_w / org_h))
        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        return im

    # 宽高均定义
    w = int(w)
    h = int(h)
    if (org_w / org_h) > (w / h):
        new_h = h
        new_w = round(new_h * (org_w / org_h))
        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        x1 = round((new_w - w) / 2)
        y1 = 0
        im = im.crop((x1, y1, x1 + w, y1 + h))
    else:
        new_w = w
        new_h = round(new_w / (org_w / org_h))
        im = im.resize((new_w, new_h), Image.ANTIALIAS)
        x1 = 0
        y1 = round((new_h - h) / 2)
        im = im.crop((x1, y1, x1 + w, y1 + h))

    # im = im.filter(ImageFilter.SHARPEN)

    return im
