# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 10:16 
# @Author  : xzr
# @File    : request.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :


from rest_framework.request import Request as RestRequest
from rest_framework.request import Empty
from .utils.cache import CacheAttribute
from objectdict import ObjectDict
from django.http.request import HttpRequest


class MyRequest(RestRequest):

    # @CacheAttribute
    # def data(self):
    #     data = super().data
    #     self._full_data = ObjectDict(data)
    #     self._full_data.update(dict(self.query_params.items()))
    #     for key in self._full_data.keys():
    #         v = self._full_data.get(key)
    #         if len(v) == 1:
    #             self._full_data[key] = v[0]
    #     return self._full_data

    @property
    def POST(self):
        # Ensure that request.POST uses our request parsing.
        if self._data is Empty:
            self._load_data_and_files()
        return self._data

    def force_plaintext_errors(self, value):
        """取消 ajax 返回 html"""
        pass


Request = MyRequest


def find_request(*args) -> HttpRequest:
    for request in args:
        if isinstance(request, (RestRequest, Request, HttpRequest)):
            return request
