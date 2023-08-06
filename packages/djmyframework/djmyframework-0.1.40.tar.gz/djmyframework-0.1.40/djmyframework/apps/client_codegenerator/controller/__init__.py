# -*- coding: utf-8 -*-

from client_codegenerator.serializer import RspCodeChoicesSer
from config.api_doc import schema_view
from framework.response import render_to_response
from framework.route import Route
from framework.utils.cache import cache_page
from framework.views import Response, Request, BaseViewSet, api_get, api_post, api_doc


@Route('client_codegenerator')
class ClientCodeGeneratorViewSet(BaseViewSet):

    @api_doc(tags=['基础接口'], request_body=RspCodeChoicesSer, responses=RspCodeChoicesSer)
    @api_post
    def choices(self, request: Request):
        """所有枚举类的
        只是告诉前端 枚举类含义
        """
        return Response(data=request)

    def to_method_title(self, x):
        return ''.join(
                [n.title() if i > 1 else n for i, n in enumerate(x.replace('_', '/').split('/'))])

    def get_definition_schema(self, parameter_schema, definitions):
        ref = parameter_schema.get('$ref', '')
        ref_key = ref.split('/')[-1]
        if ref_key:
            definition_schema = definitions.get(ref_key)
            return ref_key, definition_schema
        return '', None

    def get_schema_properties_desc(self, parameter_schema, schema):
        desc_text = ''
        ref_key, definition_schema = self.get_definition_schema(parameter_schema, schema.definitions)
        if definition_schema:
            desc_text = ','.join([f'{key_name} {definition_schema.get("title", "")}' for key_name, definition_schema in definition_schema['properties'].items()])
        return desc_text

    def get_schema_text(self, parameter_schema, schema, is_unfold=True):
        jsdoc_type_map = {'integer': 'number'}
        if parameter_schema:
            ref_key, definition_schema = self.get_definition_schema(parameter_schema, schema.definitions)
            if ref_key:
                if definition_schema and is_unfold:
                    definition_unfold = ', '.join([f'{key_name}:{self.get_schema_text(definition_schema, schema)}' for key_name, definition_schema in definition_schema['properties'].items()])
                    return '{%s}' % definition_unfold
                return ref_key
            schema_type = parameter_schema.get('type')
            return jsdoc_type_map.get(schema_type, schema_type or '')
        return ''

    def get_schema(self):
        rsp = schema_view.without_ui(cache_timeout=0)(self.request._request)
        schema = rsp.data
        return schema

    @cache_page(10)
    @api_get
    def jscode(self, request: Request):
        schema = self.get_schema()
        return render_to_response('client_codegenerator/jscode.html', locals(), content_type='application/javascript;charset=utf-8')
