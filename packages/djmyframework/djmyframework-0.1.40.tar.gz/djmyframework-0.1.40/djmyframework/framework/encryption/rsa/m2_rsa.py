# -*- coding: UTF-8 -*-

import base64

import M2Crypto
from Crypto.PublicKey import RSA
from M2Crypto import *


# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.PublicKey import RSA
def str_to_bytes(s):
    """Convert str to bytes."""
    if isinstance(s, str):
        return s.encode()
    return s


private_key_tpl = '''-----BEGIN PRIVATE KEY-----
%s
-----END PRIVATE KEY-----
'''

public_key_tpl = '''-----BEGIN PUBLIC KEY-----
%s
-----END PUBLIC KEY-----'''


def private_encrypt(msg, file_name):
    """私钥加密
    """
    # print(type(msg), "原文: ", msg)

    rsa_pri = M2Crypto.RSA.load_key(file_name)
    ctxt_pri = rsa_pri.private_encrypt(msg.encode(), M2Crypto.RSA.pkcs1_padding)  # 这里的方法选择加密填充方式，所以在解密的时候 要对应。
    ctxt64_pri = base64.b64encode(ctxt_pri).decode()  # 密文是base64  方便保存 encode成str
    return ctxt64_pri


def private_encrypt_str(msg, context):
    """私钥加密
    """
    # print(type(msg), "原文: ", msg)
    _maxlength = 128 -11
    data = msg.encode()
    rsa_pri = M2Crypto.RSA.load_key_string(context.strip('\n').encode('utf-8'))
    l_dstr = []
    for i in range(len(data) // _maxlength + 1):
        _d = data[i * _maxlength:_maxlength * (i + 1)]
        b = rsa_pri.private_encrypt(_d, M2Crypto.RSA.pkcs1_padding)
        l_dstr.append(b)
    ctxt_pri = b''.join(l_dstr)
    return base64.b64encode(ctxt_pri).decode()

    return ctxt64_pri


def get_m2c_pub(pub_string):
    """将公钥字符串转为m2c的对象
    """
    pub_string = str_to_bytes(pub_string)
    return M2Crypto.RSA.load_pub_key_bio(BIO.MemoryBuffer(pub_string))


def get_m2c_private(private_string):
    """将私钥字符串转为m2c的对象
    """
    # rsa_pri = M2Crypto.RSA.load_key_bio(private_string)
    return M2Crypto.RSA.load_key_bio(BIO.MemoryBuffer(private_string))


def read_key(file_path, key_type):
    """
    读取RSA密钥
    :param file_path: 文件路径
    :param key_type: 密钥类型，private：私钥|public：公钥
    :return:
    """
    with open(file_path, "rb") as file_handler:
        rea_key = BIO.MemoryBuffer(file_handler.read())
    if key_type == "private":
        return M2Crypto.RSA.load_key_bio(rea_key)
    else:
        return M2Crypto.RSA.load_pub_key_bio(rea_key)


def public_decrypt(data, m2c_pub):
    """公钥解密数据
    """
    data = base64.b64decode(data)
    _maxlength = 128
    l_dstr = [m2c_pub.public_decrypt(data[i * _maxlength:_maxlength * (i + 1)], M2Crypto.RSA.pkcs1_padding) for i in
              range(int(len(data) / _maxlength))]
    return b''.join(l_dstr)


def private_decrypt(data, m2c_pri):
    """私钥解密数据
    """
    data = base64.b64decode(data)
    _maxlength = 128
    l_dstr = [m2c_pri.private_decrypt(data[i * _maxlength:_maxlength * (i + 1)], M2Crypto.RSA.pkcs1_padding) for i in
              range(int(len(data) / _maxlength))]
    return b''.join(l_dstr)


def read_str_key(context):
    # print(M2Crypto.RSA.load_key_string(file.strip('\n').encode('utf-8')))
    return M2Crypto.RSA.load_key_string(context.strip('\n').encode('utf-8'))


def decrypt(data, m2c_pub):  # 公钥解密数据
    data = base64.b64decode(data)
    _maxlength = 128
    l_dstr = [m2c_pub.public_decrypt(data[i * _maxlength:_maxlength * (i + 1)], RSA.pkcs1_padding) for i in range(int(len(data) / _maxlength))]
    return b''.join(l_dstr).decode()


def verify(data, signature, m2c_pub):  # 签名认证
    data = str_to_bytes(data)
    m = EVP.MessageDigest('sha1')
    m.update(data)
    digest = m.final()
    signature = base64.b64decode(signature)
    try:
        return m2c_pub.verify(digest, signature, algo='sha1')
    except:
        return False


if __name__ == "__main__":
    public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+HyGeqMMEkqZIG
Qx9teOxCBScqDYrPW9BQupS1DpTvlqCo9O08f7ekc9lVI4uxBMIi7
Kfj/qKHHPDc3IQdi0QBsV7M1Jw6gJNd07JoTz1XFABogg7CabL4FM
k1d+S8+xjvUXvXaTjp2IP+9dzg2ZIcyESHhE5m
/eeRr6kv4wSWwIDAQAB
-----END PUBLIC KEY-----'''
    m2c_key = get_m2c_pub(public_key)
    notify_data = 'dnX94IypHG3vaF3/tzQcJ0GUxY8ZI7fvZ+14n27ytsBzqDrSPG9D3bavTCRa9XALp29qsfa0ttko7ZgOPeukrlDLYk7kbu97H4O0RvP7prmCln3q8dffR/Bvx5x2ev6hVekCJ8gbMEhcET58xyc9UGzeZiX4XiMqy4tG4roi3x8='

    sign = 'RGw884RvmNJgVlpvcK/6Sj4hMn3G2i1Jbx+bFjZTPon1w7JuWxhTsOFIgULFnSDvqwb/8xYDiK5bXYkS46NtHV2ykOxGDh01SzOBKnMmXwSflwlCBvQE4PfAkr1RKk/ZbfnMo3nEgbF6mFM+u8Pv5+ryHFfGl0aFl6CuRW/glnQ='
    content = 'dealseq=511_535822662_1440734304&notify_data=dnX94IypHG3vaF3/tzQcJ0GUxY8ZI7fvZ+14n27ytsBzqDrSPG9D3bavTCRa9XALp29qsfa0ttko7ZgOPeukrlDLYk7kbu97H4O0RvP7prmCln3q8dffR/Bvx5x2ev6hVekCJ8gbMEhcET58xyc9UGzeZiX4XiMqy4tG4roi3x8=&orderid=150828823511581212854&subject=10Gold&uid=s55c6bf3462b60&v=1.0'

    print(decrypt(notify_data, m2c_key))  # dealseq=511_535822662_1440734304&fee=1.0&payresult=0
    print(verify(content, sign, m2c_key))

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

    encrypted_base64 = 'xnAgvSLXGoZCrpOsVT3kjzLG1RoVlX4PSsNhIkFQ5oLDNiAwDO/Is7vRRab1ja7za4IufijHef+0sSB9lhxz6EzvG2N47FGbfFPOT8c9z5ubPBnUOIL9gDDnMfhmvKMfVjpiZJVyyMF/u/7sTQ0fRZVSTTJTbx4OTHD1+LhbSbs='
    encrypted_base64 = 'it0JiVDFRl1rCQk07M5980N6aiCoCVKqXMZaenJs8J9yC6qOxI0M8mz7DOU81ToSMsjs8y9X/1iql2D8ULuf5gQGR9Owb9+W7wnJNKpYBAdlozNqA9Q/W/PjIUqxYVCPIBwg8jYoUrIkSXsz/60eQJO1FkhN6rn0SwG+SR0VOwRwuUPY3j0CZurSxSMeElINWnK/oMs3wo0ww/iIagvuO0RBqEDJelr02K3Uqv+c6pPpZQI7QZw3KibYVRqAdRtmHK2STOef1g3+OIMD9kB+DkjUPJBk8uwSWoYmh1i+/iq/EOz4xvalIR+pzyGwgceGXMLi/pl82+5GuC/XTdS77JXnsiXNcDYUfbBuYL3Fva3BMTXaSihdWBWKfiDI6YVw9hGdpKR3qnX/eKKHQ6sQKgC3a42clBOU/2HIYxQaqbOOtFoK/ZNpTQaYD0lJj6uD69OLODIzxQ2tl0bxSHF+dDC2o9ZAVreJSWxUoHAzzfauoUgnzPBf7awmM5XfOKTMx4Y9nTrzimLSl5RZC2vBQqtWHSKeB4aBCT1qMaHLzrNwKk2v/ga9hG8Q/6weI/ghQbCjdMyJPrmqz/QeaBUZPWw42sRaptsDi345Gqk4cOfVXT4Ug/3GSprqQRZyVqy53ZCpa5UC6jjhrbJX3hvL1gG48Yzh9BG2VQhnguzaD2s='

    # print(decrypt(encrypted_base64, get_m2c_pub(pub_key)))
    print(private_encrypt_str('asd/解密工', pri_key))
    print(private_encrypt_str('RSA在线加密/解密工具，支持1024,2048,4096bits密钥。由于公钥是可以通过私钥推算出来，所以只要提供了私钥就可进行加密和解密操作。但如果只有公钥则只能进行单向操作。密钥标识指的是模(Modulus)的MD5(16bits)摘要信息，如果私钥和公钥的标识相同那么可以认为是成对密钥。利用这一点可以帮助我们检查密钥是否正确。', pri_key))
