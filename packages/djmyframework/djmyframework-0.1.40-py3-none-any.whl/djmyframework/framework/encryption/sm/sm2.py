# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 14:02 
# @Author  : xzr
# @File    : sm2.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import base64
import binascii

from gmssl import sm3, func
from gmssl.sm2 import CryptSM2, default_ecc_table
from pysmx.SM2 import generate_keypair


def str_to_bytes(s):
    """Convert str to bytes."""
    if isinstance(s, str):
        return s.encode()
    return s


class MyCryptSM2(CryptSM2):
    def __init__(self, private_key, public_key, ecc_table=default_ecc_table):
        super().__init__(private_key, public_key, ecc_table)
        if public_key[:2] == '04':
            self.public_key = self.public_key[2:]

    def encrypt(self, data, is_c1c2c3=True):
        """
        c1 c2 c3 顺序 去掉 头部 04
        @param data:
        @param is_c1c2c3:
        @return:
        """
        data = str_to_bytes(data)
        public_key = self.public_key

        # 加密函数，data消息(bytes)
        msg = data.hex()  # 消息转化为16进制字符串
        k = func.random_hex(self.para_len)
        C1 = self._kg(int(k, 16), self.ecc_table['g'])
        xy = self._kg(int(k, 16), public_key)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:2 * self.para_len]
        ml = len(msg)
        t = sm3.sm3_kdf(xy.encode('utf8'), ml / 2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % ml
            C2 = form % (int(msg, 16) ^ int(t, 16))
            C3 = sm3.sm3_hash([
                    i for i in bytes.fromhex('%s%s%s' % (x2, msg, y2))
            ])
            if is_c1c2c3:
                return bytes.fromhex('04%s%s%s' % (C1, C2, C3))
            else:
                return bytes.fromhex('%s%s%s' % (C1, C3, C2))

    def decrypt(self, data, is_c1c2c3=True):
        """
        c1 c2 c3 顺序 去掉 头部 04
        @param data:
        @param is_c1c2c3:
        @return:
        """
        data = str_to_bytes(data)
        # 解密函数，data密文（bytes）
        if data[:1] == b'\x04':
            data = data[1:]
        data = data.hex()
        len_2 = 2 * self.para_len
        len_3 = len_2 + 64
        if is_c1c2c3:
            C1 = data[0:len_2]
            C2 = data[len_2:len(data) - 64]
            C3 = data[-64:]
        else:
            C1 = data[0:len_2]
            C3 = data[len_2:len_3]
            C2 = data[len_3:]
        xy = self._kg(int(self.private_key, 16), C1)
        # print('xy = %s' % xy)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:len_2]
        cl = len(C2)
        t = sm3.sm3_kdf(xy.encode('utf8'), cl / 2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % cl
            M = form % (int(C2, 16) ^ int(t, 16))
            u = sm3.sm3_hash([
                    i for i in bytes.fromhex('%s%s%s' % (x2, M, y2))
            ])
            return bytes.fromhex(M)

    def _sm3_z(self, data):
        """
        SM3WITHSM2 签名规则:  SM2.sign(SM3(Z+MSG)，PrivateKey)
        其中: z = Hash256(Len(ID) + ID + a + b + xG + yG + xA + yA)
        """
        # sm3withsm2 的 z 值
        z = '0080' + '31323334353637383132333435363738' + \
            self.ecc_table['a'] + self.ecc_table['b'] + self.ecc_table['g'] + \
            self.public_key
        z = binascii.a2b_hex(z)
        Za = sm3.sm3_hash(func.bytes_to_list(z))
        M_ = (Za + data.hex()).encode('utf-8')
        e = sm3.sm3_hash(func.bytes_to_list(binascii.a2b_hex(M_)))
        return e

    def sign_with_sm3(self, data, random_hex_str=None):
        data = str_to_bytes(data)
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        if random_hex_str is None:
            random_hex_str = func.random_hex(self.para_len)
        sign = self.sign(sign_data, random_hex_str)  # 16进制
        return sign

    def verify_with_sm3(self, sign, data):
        data = str_to_bytes(data)
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        return self.verify(sign, sign_data)

    @classmethod
    def generate_keypair(cls):
        """生成密钥对"""
        key = generate_keypair()
        return key.privateKey.hex().upper(), key.publicKey.hex().upper()


Sm2 = MyCryptSM2

if __name__ == '__main__':
    public_key = '04E0E2E37F11901483CDFBC47F489D87D5D78C55DD7F919B73DEA83007748668B7871A1BA9608F156E25B7D64C7821379BAC1E2C591D5A50FF311D1AAE026C1DAE'
    private_key = 'D25595C27BC0E4C678533F06D9D7BA66EECDBCED47268112B48E5CEA4563EC00'
    encrypt_data = 'lVBwcL8/t7Hm8rcLLlcbOp/i3fllEvP+6gYLDbnmQuqKydxGmR0scZz2kA6iLvpTgRY0hb8S0ty/OoMDdoE7MJCtkIgJihziorn3ay4iQofCZDODbJP679SiubQceAo23BQaIQ=='
    encrypt_data = base64.b64decode(encrypt_data)
    sm2 = MyCryptSM2(private_key, public_key)
    src = 'appid=34ec69ce-b3d5-4934-85fa-b269e4ff329c&secret=f9f8d6ee-79a5-4cfb-96fb-7597d188b9b5&sign=3831e4dce5b13ab4f411692f6b8c21a13c7b79d831b644a3d49577db05bca103&timestamp=1668700805'
    print(sm2.sign_with_sm3(src))
    print(sm2.verify_with_sm3('354b50a37797faf781537ce64e188f00b1970695606366ed7fb1d028f141990079eeafe79ff5520bac4bd95e85a1028c2abe779a62046aa173189f9d3742fe27',
                              src))

    data = sm2.decrypt(encrypt_data, False)
    print(data)
    assert data == b'asdf'
    data2 = sm2.decrypt(base64.b64decode('htBS2Af1TIeWvxbu6S6r2cD7bvt9POZjrqJIv1ZNCWQQB+cee90q5e6+Nsjnr6XfiYy7UFsF7wUCiJjvCBvuzZsMo46LnIRqtVV5/hIKysnMFKeQ2GTqiqXOb3DF1oSAasab5A=='), False)
    print(data2)
    assert data2 == b'asdf'

    encrypt_data = sm2.encrypt(b'asdfbb', False)
    print(base64.b64encode(encrypt_data))
    print(sm2.decrypt(encrypt_data, False), sm2.decrypt(encrypt_data, False) == b'asdfbb')

    private_key = 'DEE7AF4A18C94FD60EFD40C8C87FC26F1764D303CF05E0D76CFDE2C1AF3B59DD'
    public_key = 'FA8C90FBC4D0E52428B5B46D36C40B70E9456797334489B76BEA01F25AD414B72EEF03AE4E168CC9FAA94ED6EEF13D8EFDC08A40E6EC9283A97A24F16C9FC6B7'
    print(private_key, public_key)
    sm2 = MyCryptSM2(private_key, public_key)
    e1 = sm2.encrypt(b'asdasd', False)
    print(base64.b64encode(e1))
    print(sm2.decrypt(e1, False))

    bb = sm2.decrypt(base64.b64decode('RwJcWKTVxYA5ThyFqPi5AWZINfYWV39IjGRBnXCGBpvKj3461pgAbFsxAZ2xSFlhPHd+yD/xiKhmbIiLTn6S/Yfv54xdADzCoUVsMMLC/RZpoyPHH9KJugmk6mz2SUy2PuXd'), False)
    assert bb == b'123'
    print(bb)

    x = "E0E2E37F11901483CDFBC47F489D87D5D78C55DD7F919B73DEA83007748668B7"
    y = "871A1BA9608F156E25B7D64C7821379BAC1E2C591D5A50FF311D1AAE026C1DAE"
    d = "D25595C27BC0E4C678533F06D9D7BA66EECDBCED47268112B48E5CEA4563EC00"
    public_key = x + y
    private_key = d
    sm2 = MyCryptSM2(private_key, public_key)
    sgin = base64.b64decode('MEYCIQCpgR9KFHMEZ1qsZfTQDc8z/+O3Nn3H9Acp+B7pBJMKKQIhAKcduK2sbaFHAuJalQ34iDbR1+FP7j1N0M52t7vJPBBZ').hex()
    print(sgin)
    from gmssl import func as GMFunc

    #
    data = b'694ae636094ce1d92b8c5d8f1b3fad6e565b6f9fdd4623a4c31b98295a6e9692'
    random_hex_str = GMFunc.random_hex(sm2.para_len)
    sgin = sm2.sign(data, random_hex_str)
    # sgin = base64.b64decode('hGUZuhylErqmJSpYaD4gNbItVy/v+LwXEEya5BwOWAgo6ejvgrknbdeX7hfC6hgSSHCcqt869wrnIjelQC2vxw==').hex()
    print(sgin, data)
    print(sm2.verify(sgin, data))

    sgin = sm2.sign_with_sm3(data, random_hex_str)
    # sgin = base64.b64decode('hGUZuhylErqmJSpYaD4gNbItVy/v+LwXEEya5BwOWAgo6ejvgrknbdeX7hfC6hgSSHCcqt869wrnIjelQC2vxw==').hex()
    print(sgin, data)
    print(sm2.verify_with_sm3(sgin, data))

    x = "95510badce29f70be07df6e2b0ce75be124a56c08e82435e72b4aa6c17679f45"
    y = "5a6892aadde2a6b7a58ca7b0e10ca78d3811ff27e9f728cd80d53c1b9a6461db"
    d = "d3f24d61bb2816882b8474b778dd7c3166d665f9455dc9d551c989c161e76ab0"
    public_key = x + y
    private_key = d
    sm2 = MyCryptSM2(private_key, public_key)
    sourceData = '3112 1669883234242 20221201162714 100370100001696'
    sign = 'MEQCIDRKBQMIIwZ1YV7VTBC9Bb6KVqk4tT9pMsmA+SpBKPPoAiBZzlIfrr6woUGkovyCBPTXbch+R81aErQ5I5LcUmh75A=='
    sign = base64.b64decode(sign).hex()
    print(sign,sm2.verify_with_sm3(sign, sourceData))


    privateKey = "1F0E2F085955461A9B87820AFBD513712CAEA89687BE657DE4EC91613BE62D32";
    publicKey = "0493FC9669F3AAC5450284F9E2E54D65AADEF2F8AD77F8DE2F4C167BA2B1244205F2DF671590E841C01AF63AA6F5F2377367D4277CBDB7F1FF5039F55A55EC4BDF";
    sopPublicKey = "04CABE03249C94BDC8A6A4440DA1B2ADFACF73F4340E5F1B9A76463694B44C2E5600A9BEAA035739383C292CF9F1C4695FAAC7963CD5033D5D647A6B1EBE78EC6A";

    private_key = d
    sm2 = MyCryptSM2('', sopPublicKey)
    sm4_key = 'Ec3HTsBlyhqK19yq'
    encryptKey ='0465EEDBA965D6BB36238E4EA7F7A037AC70195BC0E09F824FF6A1EC3BC4B5F59BCCB2C9C32C9B589682DD0D281D0805836EA3D223632A465CD439918CB232F5EB2A799C0073187A27FE4202A776292B6057A64C432A045A9D0FB34CC16CF62388651B353D44BE53EF17517600A03B2D3F'
    secret = sm2.encrypt(sm4_key, False)
    secret = base64.b64encode(secret).decode()
    print(secret)

    source_text='''I4aLcpB+xhL4eR72/eLT/HsO/qNlzt2AjCQ+w++o56XM/Gret1lqV/sWryZNGeQsIh1mlQtFVbOJ
WdzmaWqlAk7QYxvMzo2RtStJAji2sO6Rv2mCovo6x+tQ/vTbCmxwkelyZ+GUtmpufDJ1mG6IqCxZ
RdByeb07jeoqNEDrOQzi0tlFUduVZvXj8sacxCQesYb3zgWNHueGq4A4ULBqTQGLXiEYtq4ur1Lr
ZcX6H/8sot/znbeLA3XlcnXYnuXBHmCr81bjJKcNwlCiqszuHNfbwmAGigWpNgr6OYowUzjof2Kf
0Y3xnbJgQOskiFA01Kse6MdHeXAi8xoi7HRZBB+FBblri+CQRuY9vJfVhJTxQPzGC0gShtKap1+h
cIFt561yb7trMTVQE0ioZ/ZSsOngZd9AOcv91F0I1869S50MYxtK7lMFLtNpRUlJUOkm8YyZJKIz
edxSy+iHXuF3bm6gZFgVJzkK9S5El7QicKQc5Lbzdcr9e5+bju+uTgxG5zlkZVaqu61LgfX/hb9R
7e/PQWno3GutNWTrK+3G9frHlBF5f8F7pM8WJgkli1UuIqQBlJ0pVR/UhJcmUl3QuwEdV/0z3Bm/
O0+szw8mhEudDKda22rthPh0r4u2ciYW048A9EB449C7E90F274BDC66CE4EE6B75290DD323CF961C32946FB31B8108A953053E62F7EC80B83ABC12EF23E0E7E1E09D73BF7EC1477700D10316786D8B9E0D44AFB40B1F64C24FD0929C523644364B295394843131199AB78499EA1C832EAB3A5226823D2F0545B30FB70D9FDA8E006'''
    sm2 = MyCryptSM2(privateKey, publicKey)
    key_sign = sm2.sign_with_sm3(sm4_key)
    print(key_sign)
    key_sign = '888b01fddd806fbbc2c7ee6373bbb18fc6b9307d70079d8665909911b2c08b88f77ba28cad3c9edfc534374bdf26c13c2c0ea2dc4fa2f47a626c3616a14c55ac'
    print(sm2.verify_with_sm3(key_sign,source_text))