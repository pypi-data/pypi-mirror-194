# -*- coding: utf-8 -*-
# @Time    : 2022/12/28 11:49 
# @Author  : xzr
# @File    : perf_orm_select.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import contextlib
import traceback
from collections import OrderedDict
from threading import local as threading_local

from celery.signals import task_prerun, task_postrun
from django.db import models
from django.db.models import QuerySet
from django.db.models.constants import LOOKUP_SEP
from django.db.models.manager import BaseManager

from framework.middleware import BaseMiddleware
from framework.utils.attribute import CachedClassAttribute

req_orm_select_store = threading_local()
req_orm_select_store.current_req_name = None
req_orm_select_store_data = {}


def get_accesss_models_data() -> dict:
    current_req_name = getattr(req_orm_select_store, 'current_req_name', None)
    return req_orm_select_store_data.setdefault(current_req_name, {}) if current_req_name else None


def add_access_models_field(model_cls, field_name):
    accesss_models_data = get_accesss_models_data()
    if accesss_models_data is not None:
        accesss_models_data.setdefault(model_cls, set())
        accesss_models_data[model_cls].add(field_name)


def get_req_thread_model_fields(model_cls) -> set:
    accesss_models_data = get_accesss_models_data()
    return set(accesss_models_data.get(model_cls, set()) if accesss_models_data else set())


def check_req_orm_select_init():
    accesss_models_data = get_accesss_models_data()
    return accesss_models_data.get('is_init') if accesss_models_data else False


def reset_req_orm_select_store():
    try:
        get_accesss_models_data()['is_init'] = True
        del req_orm_select_store.current_req_name
    except Exception as e:
        traceback.print_exc()


class PerfOrmSelectQuerySet(QuerySet):

    def get_req_thread_fields(self) -> set:
        return get_req_thread_model_fields(self.model)

    def set_related_select_fields(self, taget_select_fields, model, parent_field_name, filed_name, parent_dict, cur_depth=0):
        select_fields = taget_select_fields
        if cur_depth < self.query.max_depth:
            related_field = model.concrete_fields_map.get(filed_name) or model.related_objects_map.get(filed_name)
            related_model = related_field.related_model
            model_only_fileds = get_req_thread_model_fields(related_model)
            if parent_field_name:
                prefix_lookup_sep = f'{parent_field_name}{LOOKUP_SEP}'
            else:
                prefix_lookup_sep = f'{filed_name}{LOOKUP_SEP}'
                
            for related_model_field_name in model_only_fileds:
                select_fields.add(f'{prefix_lookup_sep}{related_model_field_name}')

            if not model_only_fileds:
                if parent_field_name:
                    select_fields.add(f'{prefix_lookup_sep}{model._meta.pk.attname}')
                else:
                    select_fields.add(f'{prefix_lookup_sep}{related_model._meta.pk.attname}')

            if parent_dict:
                for child_field_name, child_dict in parent_dict.items():
                    parent_field_name = f'{prefix_lookup_sep}{child_field_name}'
                    self.set_related_select_fields(select_fields, related_model, parent_field_name, child_field_name, child_dict, cur_depth + 1)
        return select_fields

    def _deduction_select_filed(self):
        # 通过执行一次查询，下次推导字段
        if check_req_orm_select_init():
            existing, defer = self.query.deferred_loading
            only_fileds = get_req_thread_model_fields(self.model)
            if isinstance(self.query.select_related, dict):
                for select_related_filed_name, child_dict in self.query.select_related.items():
                    self.set_related_select_fields(only_fileds, self.model, '', select_related_filed_name, child_dict, 0)
            # 自定 defer 和 没自定 only  则自动添加字段
            if (defer and existing) or (not existing):
                self.query.add_immediate_loading(only_fileds)

    def _fetch_all(self):
        self._deduction_select_filed()
        return super()._fetch_all()


class PerfOrmSelectManager(BaseManager.from_queryset(PerfOrmSelectQuerySet), models.Manager):
    def get_queryset(self):
        """重写 get_queryset"""
        return super().get_queryset()


class PerfOrmSelectModel(models.Model):
    """优化 orm 查询 字段选择，适合多字段的表
    在一个请求线程内 记录执行模型的 query 后，通过 model 获取的属性名
    instance = Model.objects.first()
    instance.f1
    instance.f2
    下次 Model.objects.first() 自动添加 only  Model.objects.only('f1','f2')
    集成模型后 Meta 添加
    class Meta:
        base_manager_name = 'objects'
    """

    objects = PerfOrmSelectManager()

    _is_load_from_db = False

    class Meta:
        abstract = True
        base_manager_name = 'objects'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.pk and getattr(self, self._meta.pk.attname):
            self._is_load_from_db = True

    def __getattribute__(self, attrname):
        if super().__getattribute__('_is_load_from_db') and attrname in super().__getattribute__('concrete_fields_map'):
            add_access_models_field(self._meta.model, attrname)
        return super().__getattribute__(attrname)

    @CachedClassAttribute
    def concrete_fields_map(cls):
        fields_map = OrderedDict([(field.name, field) for field in cls._meta.concrete_fields if
                                  not field.primary_key])
        # 外键 attrname 也算进去
        for key in list(fields_map.keys()):
            fields_map[fields_map[key].attname] = fields_map[key]
        return fields_map


class PerfOrmSelectMiddleware(BaseMiddleware):
    """优化 orm select 的查询
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        req_view_func = self.get_check_view_func(request, view_func)
        req_name = f'{req_view_func.__module__}.{req_view_func.__name__}'
        req_orm_select_store.current_req_name = req_name

    def process_response(self, request, response):
        reset_req_orm_select_store()
        return response

    def process_exception(self, request, exception):
        reset_req_orm_select_store()


@task_prerun.connect
def celery_task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    try:
        req_orm_select_store.current_req_name = task.name
    except Exception as e:
        traceback.print_exc()


@task_postrun.connect
def celery_task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **extras):
    try:
        reset_req_orm_select_store()
    except Exception as e:
        traceback.print_exc()


@contextlib.contextmanager
def perf_orm_select_context(req_name):
    try:
        req_orm_select_store.current_req_name = req_name
        yield
    finally:
        reset_req_orm_select_store()
