# -*- coding: utf-8 -*-
# @Time : 2020-06-09 14:07
# @Author : xzr
# @File : encrypt.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc :


import base64
from Crypto.Cipher import AES
import gzip
from base64 import b64encode, b64decode
from urllib.parse import quote
from framework.encryption.des.des import des_encrypt

'''
采用AES对称加密算法
'''

#实现 base64+gzip+AES-ECB

# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


KEY = 'slakdma'
# 加密方法
def encrypt(text, key=KEY):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    # 用base64转成字符串形式
    encrypted_text = base64.encodebytes(encrypt_aes)  # 执行加密并转码返回bytes  # str(encoding=utf-8)
    # gzip压缩
    en_gzip = gzip.compress(encrypted_text)
    # base64编码
    en_base64 = base64.b64encode(en_gzip)
    return en_base64


# 解密方法
def decrypt(encrypt_text, key=KEY):
    # 秘钥

    # 密文
    # base64解码
    de_base64 = base64.b64decode(encrypt_text)
    # gzip解压
    de_gzip = gzip.decompress(de_base64)

    text = str(de_gzip, encoding="utf-8")
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypted_text


def get_dynamic_data(raw_data):
    """
    微信跳转到农行APP进行快e通支付，返回的是一个链接。这个函数为了获取dynamicData参数

    https://wx.abchina.com/webank/main-view/openTagForId?id=oNFcmoITJ9Q%3D&dynamicData=xxx

    跳转掌银url的动态参数部分，若链接为固定，则此参数不传，若动态则必填。具体加密规则：字符串进行des cbc加密，密钥为:bankabc1，偏移量:abchina1，
    加密之后进行base64转码，再调用JavaScript encodeURIComponent()进行编码，
    得到的结果即为dynamicData的值，举例：原串为tokenID=16038668758730826969,结果为wwAZS%2FhB0hJ1QEeNOku5C%2Ba0UfRB7azVHW7WM1Jz2Po%3D

    https://wx.abchina.com/webank/main-view/openTagForId?id=oNFcmoITJ9Q%3D&dynamicData=wwAZS%2FhB0hJ1QEeNOku5C%2Ba0UfRB7azVHW7WM1Jz2Po%3D
    """
    key = b64encode('bankabc1'.encode())
    iv = 'abchina1'.encode()

    encrypted_data = des_encrypt(key, raw_data, iv)
    encrypted_data = quote(encrypted_data, safe='')

    return encrypted_data


if __name__ == '__main__':
    en_result = encrypt('alsdewtwet3q3eraqwrqwewewklasd')
    print(en_result)
    de_result = decrypt(en_result)
    print(de_result)