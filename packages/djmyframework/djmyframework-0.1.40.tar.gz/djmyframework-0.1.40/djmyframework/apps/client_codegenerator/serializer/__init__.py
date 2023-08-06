# -*- coding: utf-8 -*-
# @Time    : 2021/10/18 08:46 
# @Author  : xzr
# @File    : __init__.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :

from framework.serializer import s, DataSerializer
from framework.shortcut import RspCodeStatus
from framework.utils.myenum import Enum
from framework.translation import _
from framework.response import RspErrorEnum, RspError


class RspCodeChoicesSer(DataSerializer):
    code = s.ChoiceField(label='所有 返回 code 的状态描述', choices=RspCodeStatus.choices)