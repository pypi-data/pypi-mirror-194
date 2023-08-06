import binascii

import base64

from gmssl.func import list_to_bytes, unpadding, bytes_to_list, padding
from pysmx.SM4 import Sm4 as _Sm4, ENCRYPT, DECRYPT


def str_to_bytes(s):
    """Convert str to bytes."""
    if isinstance(s, str):
        return s.encode()
    return s


class Sm4(_Sm4):

    def __init__(self, key):
        if isinstance(key, str):
            key = bytes.fromhex(key)
        self.key = key

    def decrypt_ecb(self, data) -> bytes:
        self.sm4_setkey(self.key, DECRYPT)
        data = self.sm4_crypt_ecb(data)
        return list_to_bytes(unpadding(data))

    def encrypt_ecb(self, input_data) -> bytes:
        input_data = bytes_to_list(input_data)
        input_data = padding(input_data)
        self.sm4_setkey(self.key, ENCRYPT)
        data = self.sm4_crypt_ecb(input_data)
        return list_to_bytes(data)

    def decrypt_ecb_b64(self, data, decode='utf-8') -> str:
        return self.decrypt_ecb(base64.b64decode(data)).decode(decode)

    def encrypt_ecb_b64(self, input_data) -> str:
        return base64.b64encode(self.encrypt_ecb(input_data))

    def encrypt_cbc(self, data: bytes, iv_data='') -> bytes:
        data = str_to_bytes(data)
        iv_data = bytes_to_list(iv_data) if iv_data else [0] * 16
        input_data = bytes_to_list(data)
        input_data = padding(input_data)
        self.sm4_set_key(self.key, ENCRYPT)
        en_data = self.sm4_crypt_cbc(iv_data, input_data)
        return list_to_bytes(en_data)

    def decrypt_cbc(self, data: bytes, iv_data='') -> bytes:
        data = str_to_bytes(data)
        iv_data = bytes_to_list(iv_data) if iv_data else [0] * 16
        self.sm4_setkey(self.key, DECRYPT)
        data = sm4.sm4_crypt_cbc(iv_data, data)
        return list_to_bytes(unpadding(data))

    def decrypt_cbc_b64(self, data, iv) -> str:
        return self.decrypt_cbc(base64.b64decode(data), iv)

    def encrypt_cbc_b64(self, input_data, iv) -> str:
        return base64.b64encode(self.encrypt_cbc(input_data, iv))


if __name__ == '__main__':
    key = '3868501278578523'
    key = key.encode().hex()
    key = 'NxkYwh1GqUEYPtSu'
    data = 'eAYYOLMLIOA9t7skv3rd+iwj8VWJBDohNmrDo4v/E1g='
    sm4 = Sm4(key)
    d = sm4.decrypt_ecb_b64(data)
    print(d)

    e1 = sm4.encrypt_ecb(b'asdbb')
    print(e1)
    d1 = sm4.decrypt_ecb(e1)
    print(d1)
    assert d1 == b'asdbb'

    key = 'Ec3HTsBlyhqK19yq'.encode()
    iv = 'UISwD9fW6cFh9SNS'.encode()

    input_data = '{"body":{"aPDURespData":"000000230080000000020759273137bdbc52f06dafa969784a579ace6fb3830e929e5a58f5381008e64641203e241944ac1703d94d866a4de86eb7d1ed535b964c1400414721db5223f0a5084736323f","busiMainId":"202212061057178871084883","deviceName":"vivo","phone":"13544441235","reqTransTime":"20221206105717"},"head":{"appID":"961925472724332544001","merchantId":"testMerchant001","method":"","partnerTxSriNo":"202212061057178871084883","reqTime":"20221206105717","version":"1"}}'
    en_data1 = '''I4aLcpB+xhL4eR72/eLT/HsO/qNlzt2AjCQ+w++o56XM/Gret1lqV/sWryZNGeQsIh1mlQtFVbOJ
WdzmaWqlAk7QYxvMzo2RtStJAji2sO6Rv2mCovo6x+tQ/vTbCmxwkelyZ+GUtmpufDJ1mG6IqCxZ
RdByeb07jeoqNEDrOQzi0tlFUduVZvXj8sacxCQesYb3zgWNHueGq4A4ULBqTQGLXiEYtq4ur1Lr
ZcX6H/8sot/znbeLA3XlcnXYnuXBHmCr81bjJKcNwlCiqszuHPzblmjcOFQdw3ULQjpjTHbQjQfP
b+0u1akz8nTh2yJ7EjRaCqSUYyAXdprCkkJ33FG1lRk1f8zb+ZSvJ0opVRMElVNsIkUUx48RpQwY
OkMNmxSjufDbkjr+JZKD5uIP0ikdcdeBc2ye299bIjvjYb+HRMr+PwkDut5Td3bX9Am33vyX66pL
ueqnkSaWFgT10YjTxNGI/MNBsbWKcH7SzgnxconrTmJDUs53itsz7/wNNYnewnc63WPiHmNhH1Va
7TuQmyXc1LVTkzFYAauGERWo0qthWGdLVzLAefYL0HTxaONATqLyQ0psmJIT4eLADDxov3ACG4Ux
7B4e8svM1LiAatF/nNHJ2RBzABbkpf5s'''
    sm4 = Sm4(key)
    en_data = sm4.encrypt_cbc_b64(input_data, iv)
    print(en_data)
    print('en_data1', sm4.decrypt_cbc_b64(en_data1, iv))
    print(sm4.decrypt_cbc_b64(en_data1, iv) == input_data.encode())
