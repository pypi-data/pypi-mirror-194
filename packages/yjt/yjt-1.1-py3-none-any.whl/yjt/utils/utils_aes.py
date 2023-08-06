# -*-coding:utf-8 -*-

"""
# Time       ：2021/10/19 11:39
# Author     ：AMU
# Description：AES加解密相关
"""
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64


class PrpCrypt(object):

    def __init__(self, key='0000000000000000', iv='0102030405060708', code_type='base64'):
        self.mode = AES.MODE_CBC
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')
        # self.key = b'qxhzngy266a186ke'
        # self.iv = b'0102030405060708'
        # block_size 128位
        self.code_type = code_type

    def encrypt(self, text):
        """
        加密

        :param text:
        :return:

        * 如果text不足16位就用空格补足为16位
        * 如果大于16但是不是16的倍数，那就补足为16的倍数
        """
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = text.encode('utf-8')

        # 这里密钥key 长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        text = self.pkcs7_padding(text)
        ciphertext = cryptor.encrypt(text)

        if self.code_type == 'base64':
            # 返回base64编码结果
            return str(base64.b64encode(ciphertext), encoding='utf-8')

        else:
            # 返回16进制字符串
            return b2a_hex(ciphertext).decode().upper()  # 全大写
            # return b2a_hex(ciphertext).decode()

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)

        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('无效的加密信息!')
        else:
            return uppadded_data

    def decrypt(self, text):
        """
        解密

        :param text:
        :return:

        * 解密后，去掉补足的空格用strip() 去掉
        """
        #  偏移量'iv'
        cryptor = AES.new(self.key, self.mode, self.iv)

        if self.code_type == 'base64':
            # 从base64解码
            content = base64.b64decode(text)
        else:
            # 从十六进制解码
            content = a2b_hex(text)

        plain_text = cryptor.decrypt(content)  # 解密
        # plain_decode = bytes.decode(plain_text)
        plain_decode = plain_text.decode('utf-8')

        return plain_decode.rstrip("\x01"). \
            rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05"). \
            rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09"). \
            rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d"). \
            rstrip("\x0e").rstrip("\x0f").rstrip("\x10")

# exp
# def default_encrypt(rawstr: str) -> str:
#     key = 'qxhzngy266a186ke'
#     iv = '1ci5crnda6ojzgtr'
#     hashstr = PrpCrypt(key=key, iv=iv).encrypt(rawstr)
#     return hashstr
#
#
# def default_decrypt(rawstr: str) -> str:
#     key = 'qxhzngy266a186ke'
#     iv = '1ci5crnda6ojzgtr'
#     return PrpCrypt(key=key, iv=iv).decrypt(rawstr)
