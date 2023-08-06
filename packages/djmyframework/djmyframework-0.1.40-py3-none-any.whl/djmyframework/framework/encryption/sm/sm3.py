##############################################################################
#                                                                            #
#                            国产SM3加密算法                                  #
#                                                                            #
##############################################################################
import base64
import hashlib

from pysmx.SM3 import SM3
from base64 import b64encode, b64decode


def md5(s):
    sign_str = hashlib.md5()
    sign_str.update(s.encode('utf-8'))
    return sign_str.hexdigest()


def sm3_encrypt(msg):
    sm3 = SM3()
    sm3.update(msg)
    return sm3.hexdigest()

def sm3_base64(msg):
    sm3 = SM3()
    sm3.update(msg)
    return base64.b64encode(sm3.digest()).decode('utf-8')

if __name__ == '__main__':
    """测试"""
    print(sm3_encrypt('SM3Test'))  # 打印结果：901053b4681483b737dd2dd9f9a7f56805aa1b03337f8c1abb763a96776b8905
    stringA = "accNum=2&amount=100.00&cardAccNum=2&eWalletId=1&liquidationDate=20170101&serialNum=29199388433&sourceChannel=1"
    stringSignTemp = f"{stringA}&key=123456"
    print(stringSignTemp)
    print(sm3_encrypt(stringSignTemp).upper())  # 322C77067A392E9A8960CDEBCE147B5E
    print(md5(stringSignTemp).upper())  # 322C77067A392E9A8960CDEBCE147B5E
