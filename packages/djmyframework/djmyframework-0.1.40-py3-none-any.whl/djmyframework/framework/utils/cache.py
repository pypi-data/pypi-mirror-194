# -*- coding: utf-8 -*-

import time
from functools import wraps

from django.core.cache import cache

from django.middleware.cache import CacheMiddleware
from .attribute import *


class CACHE_TYPE(object):
    LOG_CACHE = 'CACHE_KEYS'


def cache_func(cache_key, func, args=(), timeout=0, cache_type_key=CACHE_TYPE.LOG_CACHE) -> ('', int):
    # 默认不缓存，直接执行方法返回，不调用缓存模块
    if timeout == 0:
        return func(*args), ""

    result = cache.get(cache_key, None)
    result_cache_time_key = '%s_time' % cache_key  # 设置缓存时间的key
    result_cache_time = ''
    if result == None:
        result = func(*args)
        cache.set(result_cache_time_key, int(time.time()), timeout=timeout)  # 设置缓存时间
        cache.set(cache_key, result, timeout=timeout)
        cache_keys = cache.get(cache_type_key, set())
        cache_keys.add(result_cache_time_key)
        cache_keys.add(cache_key)
        cache.set(cache_type_key, cache_keys)
    else:
        result_cache_time = cache.get(result_cache_time_key, 0)
    return result, result_cache_time


def clear_cache(cache_type_key):
    """删除缓存
    """
    cache_keys = cache.get(cache_type_key, set())
    cache_keys.add(cache_type_key)
    cache.delete_many(cache_keys)


def make_middleware_decorator(middleware_class):
    from ..request import find_request
    def _make_decorator(*m_args, **m_kwargs):
        def _decorator(view_func):
            middleware = middleware_class(view_func, *m_args, **m_kwargs)

            @wraps(view_func)
            def _wrapped_view(*args, **kwargs):
                request = find_request(*args)
                if hasattr(middleware, 'process_request'):
                    result = middleware.process_request(request)
                if result is not None:
                    return result
                if hasattr(middleware, 'process_view'):
                    result = middleware.process_view(request, view_func, args, kwargs)
                    if result is not None:
                        return result
                try:
                    response = view_func(*args, **kwargs)
                except Exception as e:
                    if hasattr(middleware, 'process_exception'):
                        result = middleware.process_exception(request, e)
                        if result is not None:
                            return result
                    raise
                if hasattr(response, 'render') and callable(response.render):
                    if hasattr(middleware, 'process_template_response'):
                        response = middleware.process_template_response(request, response)
                    # Defer running of process_response until after the template
                    # has been rendered:
                    if hasattr(middleware, 'process_response'):
                        def callback(response):
                            return middleware.process_response(request, response)

                        response.add_post_render_callback(callback)
                else:
                    if hasattr(middleware, 'process_response'):
                        return middleware.process_response(request, response)
                return response

            return _wrapped_view

        return _decorator

    return _make_decorator


def cache_page(timeout, *, cache=None, key_prefix=None):
    """
    重写下 django 页面缓存 适配 viewset 的 method
    """

    return make_middleware_decorator(CacheMiddleware)(
            page_timeout=timeout, cache_alias=cache, key_prefix=key_prefix,
    )
