# -*- coding: utf-8 -*-
# @Time    : 2022/4/18 19:15 
# @Author  : xzr
# @File    : test_excel.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :

import xlsxwriter
import openpyxl

from config.export_file import ExportExcelFile
from ..utils.excel import bold_format


def test_excel():
    wb = xlsxwriter.Workbook('test_excel.xls')
    ws = wb.add_worksheet()
    bold = wb.add_format(bold_format)
    headings = ['充值订单号', '充值时间', '充值到账时间', '充值金额', '储值钱包到账', '赠送钱包到账', '储值钱包', '姓名',
                '人员编号', '手机号码', '充值类型', '充值渠道', '第三方订单号', '交易流水号', '充值状态', '对账状态']
    ws.set_column('A1:D1', 20)

    ws.write_row('A1', headings, bold)

    wb.close()


def test_ExportExcelFile():
    file_name = 'test_excel.xls'
    template_excel = 'order_withdraw_details_list_export_task'

    wb, file_path = ExportExcelFile.get_template_excel_wb('order_withdraw_details_list_export_task')

    ws = wb.active
    ws.append(['1', '2', '34', '5', '3'])
    wb.save(file_path)
    wb.close()
