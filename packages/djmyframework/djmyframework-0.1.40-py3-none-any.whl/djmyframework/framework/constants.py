# -*- coding: utf-8 -*-
# @Time    : 2021/8/26 15:44
# @Author  : xzr
# @File    : constants.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
from framework.utils.http_status import *

ID = 'id'
ALIAS = 'alias'

MODEL_STATUS_DESC = {
    'enable': '正常',
    'disable': '禁用',
    'delete': '删除',
    'unknown': '未知',
    'expire': '过期',
}

MODEL_STATUS_CHOICE = (
    ('delete', '删除'),
    ('enable', '正常'),
    ('disable', '禁用'),
    ('expire', '过期'),
    ('unknown', '未知'),
)

CONSOLE_COLOR = {
    'white': '\033[1;30m',
    'red': '\033[1;31m',
    'green': '\033[1;32m',
    'yellow': '\033[1;33m',
    'blue': '\033[1;34m',
    'pink': '\033[1;35m',
    'cyan': '\033[1;36m',
    'grey': '\033[1;37m',
    'end': '\033[0m',
}

INDUSTRY_TYPE_MAP = {
    1: '互联网/电子商务',
    2: 'IT软件与服务',
    3: 'IT硬件与设备',
    4: '电子技术',
    5: '通信与运营商',
    6: '网络游戏',
    7: '银行',
    8: '基金|理财|信托',
    9: '保险',
    10: '餐饮',
    11: '酒店',
    12: '旅游',
    13: '快递',
    14: '物流',
    15: '仓储',
    16: '培训',
    17: '院校',
    18: '学术科研',
    19: '交警',
    20: '博物馆',
    21: '公共事业|非盈利机构',
    22: '医药医疗',
    23: '护理美容',
    24: '保健与卫生',
    25: '汽车相关',
    26: '摩托车相关',
    27: '火车相关',
    28: '飞机相关',
    29: '建筑',
    30: '物业',
    31: '消费品',
    32: '法律',
    33: '会展',
    34: '中介服务',
    35: '认证',
    36: '审计',
    37: '传媒',
    38: '体育',
    39: '娱乐休闲',
    40: '印刷',
    41: '其它'
}

