# -*-coding:utf-8 -*-

"""
# Time       ：2022/6/25 15:08
# Author     ：AMU
# Description：图片验证码
"""
import random
import string
from base64 import b64encode
from io import BytesIO
from pathlib import Path
from typing import Tuple, Union

from PIL import Image, ImageDraw, ImageFont

path = Path(__file__).parent.joinpath("font")
font_arr = [str(f) for f in path.glob("*.ttf")]

# background_color = [(255, 255, 255), (211, 211, 211), (245, 245, 245)]
background_color = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]


def _color():
    # return tuple((random.randint(0, 255) for _ in range(3)))
    return tuple((random.randint(50, 150) for _ in range(3)))


def _get_xy(width, height):
    return [
        random.randint(width / 2, width),
        random.randint(height / 2, height),
        random.randint(0, width),
        random.randint(0, height),
    ]


def captcha(num: int = 4, scope: str = "digits") -> str:
    """
    生成随机验证码
    :param num: 验证码位数
    :param scope: 验证码内容范围 digits upper lower 用下划线组合, 分别代表 数字,大写字母, 小写字母
    :return: 文本验证码
    """
    s: str = ""
    if "digits" in scope:
        s = s + string.digits
    if "upper" in scope:
        s = s + string.ascii_uppercase
    if "lower" in scope:
        s = s + string.ascii_lowercase

    return "".join([random.choice(s) for _ in range(num)])


def img_captcha(
        width: int = 150,
        height: int = 60,
        font_size: int = 39,
        code_num: int = 4,
        scope: str = "digits",
        raw: str = "",
        byte_stream: bool = False,
) -> Tuple[Union[Image.Image, BytesIO], str]:
    """
    生成图形验证码，返回Image对象 , 验证码文本
    :param width: 验证码长度（x轴） 默认: 150
    :param height: 图片宽度（y轴） 默认: 60
    :param font_size: 字体大小 默认: 39
    :param code_num: 验证码位数 默认: 4
    :param scope: 验证码内容范围: digits upper lower 任意组合, 分别代表: 数字,大写字母, 小写字母; 默认: digits
    :param raw: 指定内容 默认: ""
    :param byte_stream: byte io 流的形式返回
    :return: (Image, str)
    """
    # 创建图形
    img = Image.new("RGB", (width, height), random.choice(background_color))
    # 画笔
    draw = ImageDraw.Draw(img)
    if not raw:
        text = captcha(num=code_num, scope=scope)
    else:
        text = raw
    # 写字
    for i, t in enumerate(text):
        # 字体
        font = ImageFont.truetype(font=random.choice(font_arr), size=font_size, encoding="Medium")
        variation_names = font.get_variation_names()
        # print(variation_names)
        # variation_arr = ["Normal", "Regular", "Medium", "Bold"]
        variation_arr = ["Regular", "Medium", "Bold"]
        for variation in variation_arr:
            if str.encode(variation) in variation_names:
                font.set_variation_by_name(variation)
                break

        font_x = font_size + i * (width / (code_num + 2)) + random.randint(-width // code_num // 4,
                                                                           width // code_num // 4)
        font_y = random.randint(2, height - font_size - 2)
        draw.text(
            xy=(font_x, font_y,),
            text=t,
            fill=_color(),
            font=font,
        )

    # 干扰
    for i in range(4):
        draw.line(xy=_get_xy(width, height), fill=_color())
        for ii in range(10):
            draw.point(xy=_get_xy(width, height), fill=_color())

    if byte_stream:
        byte_io = BytesIO()
        img.save(byte_io, "JPEG")
        byte_io.seek(0)
        result = byte_io
    else:
        result = img
    return result, text


def b64_captcha(
        width: int = 150,
        height: int = 60,
        font_size: int = 39,
        code_num: int = 4
) -> Tuple[str, str]:
    img, code = img_captcha(width, height, font_size, code_num, byte_stream=True)
    b64_img = "data:image/jpeg;base64," + b64encode(img.getvalue()).decode(encoding="utf-8")
    return b64_img, code


__all__ = ["captcha", "img_captcha", "b64_captcha"]
