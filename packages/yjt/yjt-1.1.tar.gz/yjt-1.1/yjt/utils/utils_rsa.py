# -*-coding:utf-8 -*-

"""
# Time       ：2022/3/2 17:06
# Author     ：AMU
# Description：RSA相关
"""
import rsa
import base64


def rsa_create_key():
    """
    生成公钥和密钥

    :return:
    """
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1()
    with open('public.pem', 'wb+') as f:
        f.write(pub)

    pri = privkey.save_pkcs1()
    with open('private.pem', 'wb+') as f:
        f.write(pri)


def rsa_en(text):
    """
    用公钥加密

    :param text:
    :return:
    """
    with open('public.pem', 'rb') as publickfile:
        p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    text = rsa.encrypt(text.encode('UTF-8'), pubkey)

    # text = base64.b64encode(text)  # byte转base64
    encrypt_text = text.hex()  # byte转16进制

    return encrypt_text


def rsa_de(encrypt_text):
    """
    用私钥解密

    :param encrypt_text:
    :return:
    """
    # encrypt_text = base64.b64decode(encrypt_text)  # base64转byte
    encrypt_text = bytes.fromhex(encrypt_text)  # 16进制转byte

    with open('private.pem', 'rb') as privatefile:
        p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    lase_text = rsa.decrypt(encrypt_text, privkey).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str

    return lase_text
