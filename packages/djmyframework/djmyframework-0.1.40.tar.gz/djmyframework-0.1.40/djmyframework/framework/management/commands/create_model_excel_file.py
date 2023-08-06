# coding:utf-8
# 生产所有模型的 Excel


import datetime
import os
import os.path

import xlsxwriter
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import NOT_PROVIDED
from django.db.models.fields.related import ForeignKey
from django.forms import ModelForm
from mako.lookup import TemplateLookup

from framework.filters import MyFilterBackend
from framework.models import BaseModel, BaseModelMixin
from framework.route import reverse_view
from ...utils import mkdirs, ObjectDict
from django.conf import settings
from django.apps import apps
from django.db import models
from ...utils.excel import bold1_format


class Command(BaseCommand):
    help = '创建所有模型的 Excel 文件描述,%s app_name.model' % __file__

    def add_arguments(self, parser):

        parser.add_argument('args', nargs='*')

    def model_field2db_field(self, field):
        """转换成文档描述"""
        if isinstance(field, models.CharField):
            return 'VARCHAR', str(getattr(field, 'max_length', ''))
        if isinstance(field, models.TextField):
            return 'TEXT', ''
        if isinstance(field, (models.IntegerField, models.ForeignKey, models.OneToOneField)):
            return 'INT', '11'
        if isinstance(field, models.BigIntegerField):
            return 'BIGINT', '20'
        if isinstance(field, models.DateTimeField):
            return 'DATETIME', ''
        if isinstance(field, models.TimeField):
            return 'TIME', ''
        if isinstance(field, models.BooleanField):
            return 'TINYINT', '1'
        if isinstance(field, models.JSONField):
            return 'JSON', ''
        return 'VARCHAR', ''

    def handle(self, *args, **options):
        file_name = os.path.join(settings.BASE_DIR, 'models_describe.xls')
        wb = xlsxwriter.Workbook(file_name, {'constant_memory': True})
        models = apps.get_models()
        headings = ['序号', '字段名', '类型', '长度', '是否允许NULL', '默认值', '索引', '描述']
        bold1 = wb.add_format({
                'bold'     : True,  # 字体加粗
                'border'   : 1,  # 单元格边框宽度
                'align'    : 'center',
                'valign'   : 'vcenter',  # 字体对齐方式
                'fg_color' : '#FFFF00',  # 单元格背景颜色
                'text_wrap': True,  # 是否自动换行
        })
        catalogue_ws = wb.add_worksheet('数据表目录')
        i = 1
        catalogue_ws.set_column('B:Q', 30)
        catalogue_ws.write_row(f'A{i}', ['', '表名', '简述', '描述'], bold1)
        for model in models:
            fields = model._meta.fields
            table_name = model._meta.db_table
            if len(table_name) >= 31:
                table_name = model._meta.db_table.replace(f'{model._meta.app_label}_', '')
            table_des = f'{table_name}: {str(model._meta.verbose_name)}'
            i += 1
            catalogue_ws.write_url(f'B{i}', f'internal:{table_name}!A2', string=table_name)
            catalogue_ws.write_row(f'A{i}', [i - 1, table_name, table_des, model.__doc__])

            ws = wb.add_worksheet(table_name)
            ws.set_column('A:Q', 20)
            j = 2

            # ws.write_row('A1', ['返回目录'])
            ws.write_url(f'A1', f'internal:数据表目录!A2', string='返回数据表目录')
            ws.merge_range('B1:H1', table_des, bold1)
            ws.write_row(f'A{j}', headings, bold1)
            ii = 0
            for field in fields:
                j += 1
                ii += 1
                dbfield, length = self.model_field2db_field(field)
                default = field.get_default()
                default = '' if default is None else str(default)
                ws.write_row(f'A{j}',
                             [ii, field.attname, dbfield, length, field.null, default,
                              field.db_index,
                              f'{field.verbose_name} {field.help_text}'])
        wb.close()
