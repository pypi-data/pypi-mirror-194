# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 11:34 
# @Author  : xzr
# @File    : urls.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import traceback
from pathlib import Path
from typing import Union

from django.urls import path as _path
from django.urls import get_resolver, URLPattern, reverse, URLResolver
from django.conf import settings


def get_view_name(view_module):
    return '%s.%s' % (view_module.__module__, view_module.__name__)


def path(route, view, kwargs=None, name=None):
    if not name:
        name = get_view_name(view)
    return _path(route, view, kwargs=kwargs, name=name)


def create_all_ulrs_py_file(file_name='_all_urls.py'):
    """创建一个导入所有url处理的py文件，方便 pycharm 全局搜索"""

    resolver = get_resolver()
    url_patterns = resolver.url_patterns
    all_import_text_list = []

    def genrate_import_text(url_pattern: Union[URLPattern, URLResolver]):
        import_text_list = []
        if isinstance(url_pattern, URLPattern):
            module_name, cls_name = url_pattern.lookup_str.rsplit('.', 1)
            import_text = f'from {module_name} import {url_pattern.callback.__name__}'
            if hasattr(url_pattern.callback, 'actions'):
                for __, val in url_pattern.callback.actions.items():
                    import_text += f';{url_pattern.callback.__name__}.{val}'
            url_path = ''
            if url_pattern.name:
                if url_pattern.pattern.regex.groupindex:
                    try:
                        print(list(url_pattern.pattern.regex.groupindex.values()), url_pattern.pattern.regex.groupindex, url_pattern.name)
                        url_path = f'{reverse(url_pattern.name, args=tuple(url_pattern.pattern.regex.groupindex.values()))}'
                    except Exception as e:
                        traceback.print_exc()
                else:
                    url_path = f'{reverse(url_pattern.name)}'
            import_text = f'{import_text} # {url_path} {url_pattern.name}'
            import_text_list.append(import_text)
        elif isinstance(url_pattern, URLResolver):
            print('URLResolver')
            for url_p in url_pattern.url_patterns:
                import_text_list += genrate_import_text(url_p)
        return import_text_list

    for url_pattern in url_patterns:
        all_import_text_list += genrate_import_text(url_pattern)

    all_import_text = '\n'.join(all_import_text_list)
    with Path(settings.BASE_DIR, file_name).open('w') as f:
        f.write(all_import_text)
        print('Write all urls to %s' % f.name)
