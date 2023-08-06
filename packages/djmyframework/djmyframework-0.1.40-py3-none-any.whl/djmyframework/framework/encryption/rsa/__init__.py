# -*- coding: utf-8 -*-
# @Time    : 2022/12/9 14:08 
# @Author  : xzr
# @File    : __init__.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import base64
import re

from Crypto.Hash import SHA, MD5, SHA256
from Crypto.PublicKey import RSA

from Crypto import Random
import rsa
import binascii
import sys
from rsa import transform, core, pem, common
from Crypto.Util import Padding, number

PRIVATE_KEY_TPL = '''-----BEGIN PRIVATE KEY-----
%s
-----END PRIVATE KEY-----
'''

PUBLIC_KEY_TPL = '''-----BEGIN PUBLIC KEY-----
%s
-----END PUBLIC KEY-----'''


def split_rsa_key(key):
    if not '\n' in key:
        return ''.join([('%s\n' % s) if ((i + 1) % 64 == 0) else s for i, s in enumerate(key)])
    return key


def format_key(key_str, format):
    if key_str[:5] != '-----':
        return format % split_rsa_key(key_str)
    return key_str


def str_to_bytes(s, encode='utf-8'):
    """Convert str to bytes."""
    if isinstance(s, str):
        return s.encode(encode)
    return s


def pub_encrypt(msg, public_key, encode='utf-8'):
    """
    公钥加密
    @param msg:
    @param public_key:
    @return:
    """
    from Crypto.Cipher import PKCS1_v1_5
    msg = str_to_bytes(msg, encode)
    public_key = format_key(public_key, PUBLIC_KEY_TPL)
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)

    block_size = number.ceil_div(number.size(rsa_key.n), 8) - 11  # 根据密钥确定每个分块的最大长度
    # padded_msg = Padding.pad(msg, block_size, style="pkcs7")  # 补位，默认补位模式：PKCS7
    padded_msg = msg
    encrypt_list = []
    for i in range(0, len(padded_msg), block_size):  # 分块加密
        sub_msg = padded_msg[i: i + block_size]
        sub = cipher.encrypt(sub_msg)
        encrypt_list.append(sub)
    text = b"".join(encrypt_list)  # 拼接加密后的信息
    return base64.b64encode(text).decode()


def pri_decrypt(encrypted_base64: str, private_key, encode='utf-8'):
    """
    私钥解密
    @param encrypted_base64:
    @param private_key:
    @return:
    """
    from Crypto.Cipher import PKCS1_v1_5
    private_key = format_key(private_key, PRIVATE_KEY_TPL)
    encrypted = base64.b64decode(encrypted_base64)
    rsa_key = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypt_block = number.ceil_div(number.size(rsa_key.n), 8)  # 每块加密后的大小
    block_size = encrypt_block - 11  # 每块补位前的大小
    decrypt_list = []
    for i in range(0, len(encrypted), encrypt_block):  # 分块解密
        sub_msg = encrypted[i: i + encrypt_block]
        sub = cipher.decrypt(sub_msg, Random.new().read)
        decrypt_list.append(sub)

    padded = b"".join(decrypt_list)
    # text = Padding.unpad(padded, block_size, style="pkcs7")
    return padded.decode(encode)


def pub_verify(msg, signature, public_key, method="SHA", encode='utf-8'):
    """
    rsa 公钥验签
    @param msg:
    @param signature:
    @param key:
    @param method:
    @return:
    """
    from Crypto.Signature import PKCS1_v1_5
    public_key = format_key(public_key, PUBLIC_KEY_TPL)
    msg = str_to_bytes(msg, encode)
    signature = base64.b64decode(signature)
    key = RSA.importKey(public_key)
    if method == "SHA":
        h = SHA.new(msg)
    elif method == "SHA256":
        h = SHA256.new(msg)
    elif method == "MD5":
        h = MD5.new(msg)
    else:
        h = SHA.new(msg)
    verifier = PKCS1_v1_5.new(key)

    return verifier.verify(h, signature)


def pri_sign(msg, pri_key, method="SHA"):
    """
    rsa 私钥签名
    @param msg:
    @param key:
    @param method:
    @return:
    """
    from Crypto.Signature import PKCS1_v1_5
    pri_key = format_key(pri_key, PRIVATE_KEY_TPL)
    key = RSA.importKey(pri_key)
    msg = str_to_bytes(msg)
    if method == "SHA":
        h = SHA.new(msg)
    elif method == "SHA256":
        h = SHA256.new(msg)
    elif method == "MD5":
        h = MD5.new(msg)
    else:
        h = SHA.new(msg)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature).decode()


def pri_encrypt(msg, pri_key, encode='utf-8'):
    """私钥加密
    """
    from rsa.pkcs1 import _pad_for_encryption, _pad_for_signing
    pri_key = format_key(pri_key, PRIVATE_KEY_TPL)
    msg = str_to_bytes(msg, encode)
    priv_key = rsa.PrivateKey.load_pkcs1(str_to_bytes(pri_key))
    keylength = common.byte_size(priv_key.n)
    block_size = keylength - 11
    encrypt_list = []
    for i in range(0, len(msg), block_size):  # 分块解密
        sub_msg = msg[i: i + block_size]
        padded = _pad_for_signing(sub_msg, keylength)
        payload = transform.bytes2int(padded)
        encrypted = priv_key.blinded_encrypt(payload)
        block = transform.int2bytes(encrypted, keylength)
        encrypt_list.append(block)
    block = b''.join(encrypt_list)

    return base64.b64encode(block).decode()


def pub_decrypt(encrypted_base64, public_key, encode='utf-8'):
    """公钥解密
    """
    public_key = format_key(public_key, PUBLIC_KEY_TPL)
    encrypted = base64.b64decode(encrypted_base64)
    key = rsa.PublicKey.load_pkcs1_openssl_pem(str_to_bytes(public_key))
    encrypt_block = common.byte_size(key.n)
    d = key.e
    n = key.n
    bytes_list = []

    for i in range(0, len(encrypted), encrypt_block):  # 分块解密
        num = transform.bytes2int(encrypted[i: i + encrypt_block])
        decrypto = core.decrypt_int(num, d, n)
        out = transform.int2bytes(decrypto)
        sep_idx = out.index(b"\x00", 2)
        out = out[sep_idx + 1:]
        bytes_list.append(out)
    decrypt_data = b''.join(bytes_list).decode(encode)
    return decrypt_data


def encrypt_private_key(a_message, private_key):
    from Crypto.Cipher import PKCS1_OAEP
    a_message = str_to_bytes(a_message)
    pri_key = format_key(private_key, PRIVATE_KEY_TPL)
    private_key = RSA.importKey(pri_key)
    encryptor = PKCS1_OAEP.new(private_key)
    encrypted_msg = encryptor.encrypt(a_message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg


if __name__ == "__main__":
    pub_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDicjx8R+cMKK0N/Fj0nkYugAj5
hcbgCuucc2ujW7BfwfLj0oxxBM11/qlCmqj4rOdquavZambihXbPbqwWfGL1D5kt
sbVMcpdH87zV7eo+Z9ZJ0k7+Z7FzGk8OhgoKETh7S9P/dMldUYCde8ljQN2lpQyi
TfRyVv8gwaNcuy9hKQIDAQAB
-----END PUBLIC KEY-----'''
    pri_key = '''-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAOJyPHxH5wworQ38
WPSeRi6ACPmFxuAK65xza6NbsF/B8uPSjHEEzXX+qUKaqPis52q5q9lqZuKFds9u
rBZ8YvUPmS2xtUxyl0fzvNXt6j5n1knSTv5nsXMaTw6GCgoROHtL0/90yV1RgJ17
yWNA3aWlDKJN9HJW/yDBo1y7L2EpAgMBAAECgYBZn0DVJ1gIdejYCjHizumT6dSj
fRDTBz9s8jl9tAJAQ/CvvlsbN/1hX+L5m2CY20XT9ZxQNk52BMCbJIAzfhNjj3x1
tWu/R40u0J+i1eosJY/+9zCff81wuUsxJnCbT1KyeXzg+FxCD6PwQFilPVjj1gfU
yW8shOwAcq2XFfpr6QJBAPvCmUgB8YpQ4JHTiy5PME37vRIDfqM3kGCVLdenEUSe
d0pbm157MXjI/cWhDsFsolKSqvW/YtSHkLP0cbK28ycCQQDmQoC74YnQpHVXEea2
togc2km5aPGFdXBoUlwnlrsiVGWYbHa/lAFKGauhnqbo6F2FpOk36f3/9wGgiztM
M3svAkEAnQCAYp2DqgRB5+8KrviHYTqKcD9prBOsn+6oRgJUDHzeW6rBO6yL7404
ZRTJhOpgWCpLHzIZSfy4yuC4PwFEpQJBALoqjKDbEizxurliDNIvNE93oeHZWmTX
9cEyzbVoZfa0m8un7j6osH4z0ROEDVkD/hE+qxz8/9MC53rg91l9yhsCQCthiI3/
O9ZhZbRk5IymlLg8/h5dcpSdmMVxZS/uZ6VTQFwQZHItcyUTy3syEUjcVmJPJ6jF
WjGoMW7gJW6oFW8=
-----END PRIVATE KEY-----'''

    pri_key = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDicjx8R+cMKK0N/Fj0nkYugAj5hcbgCuucc2ujW7BfwfLj0oxx
BM11/qlCmqj4rOdquavZambihXbPbqwWfGL1D5ktsbVMcpdH87zV7eo+Z9ZJ0k7+
Z7FzGk8OhgoKETh7S9P/dMldUYCde8ljQN2lpQyiTfRyVv8gwaNcuy9hKQIDAQAB
AoGAWZ9A1SdYCHXo2Aox4s7pk+nUo30Q0wc/bPI5fbQCQEPwr75bGzf9YV/i+Ztg
mNtF0/WcUDZOdgTAmySAM34TY498dbVrv0eNLtCfotXqLCWP/vcwn3/NcLlLMSZw
m09Ssnl84PhcQg+j8EBYpT1Y49YH1MlvLITsAHKtlxX6a+kCQQD7wplIAfGKUOCR
04suTzBN+70SA36jN5BglS3XpxFEnndKW5teezF4yP3FoQ7BbKJSkqr1v2LUh5Cz
9HGytvMnAkEA5kKAu+GJ0KR1VxHmtraIHNpJuWjxhXVwaFJcJ5a7IlRlmGx2v5QB
ShmroZ6m6OhdhaTpN+n9//cBoIs7TDN7LwJBAJ0AgGKdg6oEQefvCq74h2E6inA/
aawTrJ/uqEYCVAx83luqwTusi++NOGUUyYTqYFgqSx8yGUn8uMrguD8BRKUCQQC6
Koyg2xIs8bq5YgzSLzRPd6Hh2Vpk1/XBMs21aGX2tJvLp+4+qLB+M9EThA1ZA/4R
Pqsc/P/TAud64PdZfcobAkArYYiN/zvWYWW0ZOSMppS4PP4eXXKUnZjFcWUv7mel
U0BcEGRyLXMlE8t7MhFI3FZiTyeoxVoxqDFu4CVuqBVv
-----END RSA PRIVATE KEY-----'''

    sign = bytes.fromhex(
            '15448E170453B9E1F8880DA2873E52E589C4A24535D91934486FF2C394B64B16EAABFF6B24775A0272972084445391103AAB4A1F80F0E975C390C1130D95B504BCE92D3E3F0AB5F6E7851661EF564E124D22B698B7D671A443FFA146605F0DF0A20A3C75522D669F4C490EDA4AA61BD8C5B4F6BB1FA3F5D4930988CEA5E023A4')
    sign = base64.b64encode(sign)
    msg = '123abc中文'
    print(pub_verify(msg, sign, pub_key, encode='gbk'))

    encrypted_base64 = 'A5CB24AD1DE71F44AB959770AB52B0D665C93170A59D506C8CA3226902C442B3D2368ACE5A64F30A9D1BFB0646F934FBE8328F3F197EAB34742856E7A2D35AAD244ACD348FFCB9D73CBDBEA950C9C8380A9A3CFB23C79D1CD015D2BEF83B679CB6F02A11AB1DB6A83A04ABAA642E144DDB42AD2DDC23DD7BDC08EDA758D1F938'
    encrypted_base64 = bytes.fromhex(encrypted_base64)
    encrypted_base64 = base64.b64encode(encrypted_base64)
    decrypt_data = pri_decrypt(encrypted_base64, pri_key, encode='gbk')
    print(decrypt_data, decrypt_data == '123abc中文')

    print('私钥签名，公钥验签：')
    sign = pri_sign(msg, pri_key=pri_key)
    print(sign)
    print(pub_verify(msg, sign, pub_key))

    print('公钥加密，私钥解密：')
    msg = 'kf撒录入激情哦金额去哦泡完脚让老师没法了飞机票去哦我就去破解额啊来开门莱克吉米噢3asklmflfm223鹏1iPad1-08018i4啊睡觉罗卡角2欧姐kf撒录入激情哦金额去哦泡完脚让老师没法了飞机票去哦我就去破解额啊来开门莱克吉米噢3asklmflfm223鹏1iPad1kf撒录入激情哦金额去哦泡完脚让老师没法了飞机票去哦我就去破解额啊来开门莱克吉米噢3asklmflfm223鹏1iPad1kf撒录入激情哦金额去哦泡完脚让老师没法了飞机票去哦我就去破解额啊来开门莱克吉米噢3asklmflfm223鹏1iPad1'
    encrypted = pub_encrypt(msg, pub_key)
    print(msg, encrypted)
    print(pri_decrypt(encrypted, pri_key))

    print('私钥加密，公钥解密：')
    encrypted_base64 = 'QojbU4g+wEbAnat6+HOcjW8M26sMfnorwjzTa+N22hTWEjUgNktyLBse0QMJmTxRryCefNSWoghOfZT9NwtYXOC/iR2sNW7YjWK+icLlrL723bR3L6Qp1RFS+V9O5OgvqzD5o39iTme7gAQfw0YauXhWs+wYBd/GwrvGJDov1qg='
    print(pub_decrypt(encrypted_base64, pub_key))
    encrypted_base64 = 'it0JiVDFRl1rCQk07M5980N6aiCoCVKqXMZaenJs8J9yC6qOxI0M8mz7DOU81ToSMsjs8y9X/1iql2D8ULuf5gQGR9Owb9+W7wnJNKpYBAdlozNqA9Q/W/PjIUqxYVCPIBwg8jYoUrIkSXsz/60eQJO1FkhN6rn0SwG+SR0VOwRwuUPY3j0CZurSxSMeElINWnK/oMs3wo0ww/iIagvuO0RBqEDJelr02K3Uqv+c6pPpZQI7QZw3KibYVRqAdRtmHK2STOef1g3+OIMD9kB+DkjUPJBk8uwSWoYmh1i+/iq/EOz4xvalIR+pzyGwgceGXMLi/pl82+5GuC/XTdS77JXnsiXNcDYUfbBuYL3Fva3BMTXaSihdWBWKfiDI6YVw9hGdpKR3qnX/eKKHQ6sQKgC3a42clBOU/2HIYxQaqbOOtFoK/ZNpTQaYD0lJj6uD69OLODIzxQ2tl0bxSHF+dDC2o9ZAVreJSWxUoHAzzfauoUgnzPBf7awmM5XfOKTMx4Y9nTrzimLSl5RZC2vBQqtWHSKeB4aBCT1qMaHLzrNwKk2v/ga9hG8Q/6weI/ghQbCjdMyJPrmqz/QeaBUZPWw42sRaptsDi345Gqk4cOfVXT4Ug/3GSprqQRZyVqy53ZCpa5UC6jjhrbJX3hvL1gG48Yzh9BG2VQhnguzaD2s='
    print(pub_decrypt(encrypted_base64, pub_key))

    encrypted_base64 = pri_encrypt(msg, pri_key)
    print(encrypted_base64)
    print(pub_decrypt(encrypted_base64, pub_key))
