# -*- coding: utf-8 -*-
# @Time : 2020-06-05 16:22
# @Author : xzr
# @File : enum.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc :
from collections import OrderedDict

from framework.utils.myenum import Enum, EmptyEnumElement
from .translation import _
from .utils.attribute import CachedClassAttribute


class BoolEnum(Enum):
    Yes = 1, _('是')
    No = 0, _('否')


class BaseDictEnum(Enum):

    @classmethod
    def keys(cls):
        return [k for k, _ in cls]

    @classmethod
    def values(cls):
        return [v for _, v in cls]

    @classmethod
    def dict(cls):
        return dict([(k, v) for k, v in cls])


class BaseGroupEnum(BaseDictEnum):
    __cache_map = OrderedDict()

    def __new__(cls, key):
        return cls.__cache_map.get(key, EmptyEnumElement)

    @CachedClassAttribute
    def choices(cls):
        for _, v in cls:
            for k, _ in v.choices:
                cls.__cache_map[k] = k
        return [(k, k.name) for k, _ in cls.__cache_map.items()]

    @classmethod
    def items(cls):
        return dict([(k, v.dict()) for k, v in cls])

    @classmethod
    def keys(cls):
        result = []
        for _, v in cls:
            result.extend(v.keys())
        return result

    @classmethod
    def types(cls):
        return super().keys()
