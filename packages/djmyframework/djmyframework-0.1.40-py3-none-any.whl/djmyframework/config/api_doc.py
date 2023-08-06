# -*- coding: utf-8 -*-
# @Time    : 2021-10-11 13:20
# @Author  : xzr
# @File    : Api 文档设置
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 不能在 import settings 前导入, 导致 REST_FRAMEWORK DEFAULT_RENDERER_CLASSES 配置失效问题
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import include, re_path, get_resolver
from framework.views import notauth
from framework.static import serve as static_view
import re
from django.conf import settings

API_INFO = openapi.Info(
        title="Myadmin API",
        default_version='v1',
        description="Myadmin description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License")
)
# 可通过访问地址增加 ?apps=app1,app2 参数,限制显示的api文档
schema_view = get_schema_view(
        API_INFO,
        public=True,
        permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
        re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', notauth(schema_view.without_ui(cache_timeout=10)),
                name='schema-json'),
        re_path(r'^api/swagger', notauth(schema_view.with_ui('swagger', cache_timeout=10)),
                name='schema-swagger-ui'),
        re_path(r'^api/redoc[/]?', notauth(schema_view.with_ui('redoc', cache_timeout=10)),
                name='schema-redoc'),
        re_path(r'^%s(?P<path>.*)$' % re.escape('static'), static_view)
]
