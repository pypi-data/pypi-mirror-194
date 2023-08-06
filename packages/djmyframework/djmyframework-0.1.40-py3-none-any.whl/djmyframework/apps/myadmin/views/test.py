# -*- coding: utf-8 -*-
# @Time    : 2022/12/8 16:17 
# @Author  : xzr
# @File    : test.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
from django.db import connection
from django.http import HttpResponse

from framework.route import Route
from framework.views import notauth, api_view, Request


@notauth
@Route('^test$')
@api_view('get')
def test(request: Request):
    """
    主页
    """
    #time.sleep(5)
    # cur = connection.cursor()
    # cur.execute('select sleep (5);')
    # cur.fetchall()
    return HttpResponse(int(request._start_time))

@notauth
@Route('^test_mysql$')
@api_view('get')
def test_mysql(request: Request):
    """
    主页
    """
    cur = connection.cursor()
    cur.execute('select sleep (5);')
    cur.fetchall()
    return HttpResponse(int(request._start_time))