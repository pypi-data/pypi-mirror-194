# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 09:44 
# @Author  : xzr
# @File    : user_agent.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
from user_agents.parsers import UserAgent

from framework.utils.attribute import CacheAttribute


class RequestUserAgent(UserAgent):

    def __init__(self, request):
        ua_string = request.META.get('HTTP_USER_AGENT', '')
        super().__init__(ua_string)
        self.ua_string = self.ua_string.lower()

    @CacheAttribute
    def is_wechat(self):
        return 'wechat' in self.ua_string or 'micromessenger' in self.ua_string

    @CacheAttribute
    def is_dingtalk(self):
        return 'dingtalk' in self.ua_string

    @CacheAttribute
    def is_alipay(self):
        return 'alipay' in self.ua_string or 'aliapp' in self.ua_string
