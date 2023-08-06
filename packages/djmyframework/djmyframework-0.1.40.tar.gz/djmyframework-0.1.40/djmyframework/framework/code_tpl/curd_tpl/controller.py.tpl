# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time: ${datetime}


from framework.filters import MyFilterBackend, OrderingFilter, MyFilterSerializer
from framework.translation import _
from framework.route import Route
from framework.serializer import s,BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer,ParamsPaginationSerializer,PaginationSerializer,ModelFilterSerializer
from framework.views import CurdViewSet, ListPageNumberPagination,action,api_doc
from framework.views import render_to_response as rt
from ${app_name}.models import ${model_name}
from django.db import transaction
from django.db.models import Q, Count, Sum, When, Case, QuerySet
from collections import OrderedDict
from framework.shortcut import APIError,Response,api_doc,api_get,api_post
from ${app_name}.services.${model_lower_name} import ${model_name}Service
from framework.serializer import CeleryTaskResultSerializer
from ${app_name}.serializer.${model_lower_name} import *
from middlewares import EnhanceRequest
from framework.serializer import CeleryTaskResultSerializer

@Route('${app_name}/${model_lower_name}')
class ${model_name}Set(CurdViewSet):
    """${app_verbose_name} ${model_desc}"""

    request: EnhanceRequest

    serializer_class = ${model_name}Serializer

    # 可条件过滤的字段
    filter_fields = List${model_name}ReqSerializer.filter_fields

    # 可以查询字段
    queryset_fields = ${list(fields_name_list)}

    model = ${model_name}

    def get_queryset(self) -> QuerySet:
        return ${model_name}.objects.filter().prefetch_related(*${[f.name for f in model_many_to_many]}).select_related(*${[f.name for f in model_foreigns]}).only(*${model_name}Set.queryset_fields)

    def get_filter_q(self,params_data=None):
        filter_q = MyFilterBackend().get_filter_q(self.request.REQUEST, self.filter_fields)
        return filter_q

    @api_doc(tags=['${app_verbose_name}'], request_body=List${model_name}ReqSerializer, responses=List${model_name}RspSerializer)
    def list(self, request:EnhanceRequest,is_export=False):
        """${model_desc}列表"""

        params_data = List${model_name}ReqSerializer(request.data).params_data
        filter_q = self.filter_q(params_data)

        if is_export:
            pass
            #from ..tasks import ${model_lower_name}_list_export
            #result = ${model_lower_name}_list_export.delay(filter_q)
            #return Response(data=dict(query_id=result.id))

        total_count, num_pages, page_contents = ${model_name}Service().list(filter_q, params_data.page, params_data.page_size)

        serializer = ${model_name}Serializer(page_contents, many=True)
        data = OrderedDict(
                count=total_count,
                page=params_data.page,
                page_size=params_data.page_size,
                results=serializer.data,
                filter=params_data
        )
        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=List${model_name}ReqSerializer, responses=CeleryTaskResultSerializer)
    @api_post
    def list_export(self, request:EnhanceRequest):
        """${model_desc}列表导出"""
        return self.list(request,is_export=True)


    @api_doc(tags=['${app_verbose_name}'], request_body=Add${model_name}ReqSerializer, responses=${model_name}Serializer)
    def add(self, request:EnhanceRequest):
        """${model_desc}新增"""

        params_data = Add${model_name}ReqSerializer(request.data).params_data
        params_data.id = 0
        ${model_lower_name} = ${model_name}Service().save(params_data)
        data = ${model_name}Serializer(instance=${model_lower_name})

        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=Modify${model_name}ReqSerializer, responses=${model_name}Serializer)
    def modify(self, request:EnhanceRequest):
        """${model_desc}更改"""

        params_data = Modify${model_name}ReqSerializer(request.data).params_data
        if not params_data.id:
            raise APIError(_('未指定ID'))
        ${model_lower_name} = ${model_name}Service().save(params_data)
        data = ${model_name}Serializer(instance=${model_lower_name})
        return Response(data=data)


    @api_doc(tags=['${app_verbose_name}'], request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request:EnhanceRequest):
        """${model_desc}删除 """
        params_data = IdsSerializer(request.data).params_data
        if params_data.ids:
            self.get_queryset().filter(id__in=params_data.ids).delete()

        return Response(data=params_data)



