# -*- coding: utf-8 -*-
# @Time    : 2021-02-25 11:00
# @Author  : xzr
# @File    : sql
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import copy
import hashlib
import re
from math import ceil

import sqlparse
from django.core.cache import cache
from django.db import connections
from django.utils.functional import cached_property
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import Name


def get_table_name(tokens):
    for token in tokens:
        if token.ttype is None:
            return token.value
    return " "


def get_parent_table_name(tokens):
    for i, token in enumerate(tokens):
        if token.value.lower() == 'like':
            parent_table_name = tokens[i + 1].value
            return parent_table_name
    return ''


def get_table_columns(tokens):
    columns = set()
    for token in tokens:

        if isinstance(token, (IdentifierList, Identifier)):
            columns |= get_table_columns(token.tokens)
        if token.ttype is Name:
            columns.add(token.value.strip('`'))
            break
    return set(columns)


def get_ddl_table_info(sql_texts):
    result = {}

    parse = sqlparse.parse(sql_texts)
    for stmt in parse:
        # Get all the tokens except whitespaces
        tokens = [t for t in sqlparse.sql.TokenList(stmt.tokens) if t.ttype != sqlparse.tokens.Whitespace]
        is_create_stmt = False
        parent_table_name = ''
        table_name = ''
        for i, token in enumerate(tokens):
            # Is it a create statements ?
            if token.match(sqlparse.tokens.DDL, 'CREATE'):
                is_create_stmt = True
                table_name = get_table_name(tokens[i:])
                result.setdefault(table_name, set())
                parent_table_name = get_parent_table_name(tokens)
                if parent_table_name:
                    result[table_name] = copy.copy(result.get(parent_table_name, set()))
                continue

            # If it was a create statement and the current token starts with "("
            if is_create_stmt and token.value.startswith("("):
                columns = get_table_columns(token.tokens)
                result[table_name] |= columns

    return result


def md5_encrypt(content):
    """
    md5加密数据
    """

    return hashlib.md5(content.encode('utf-8')).hexdigest()


safe_sql_pattern = re.compile(r"""'|"|;|>|<|%|--""", flags=re.I)


def get_safe_sql_value(value):
    """防止sql注入"""
    value = re.sub(safe_sql_pattern, '', str(value))
    return value


def dict_fetchall(cursor):
    """将游标返回的结果保存到一个字典对象中"""
    desc = cursor.description
    return (dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            )


def execute_raw_sql(sql, alias='readonly', use_dict=True):
    conn = connections[alias]
    cur = conn.cursor()
    cur.execute(sql)
    if use_dict:
        return dict_fetchall(cur)
    else:
        return cur.fetchall()


class SqlPagination(object):
    """使用原始 SQL 分页获取结果"""

    def __init__(self, sql, page_size, page_no):
        self.sql = sql
        self.md5_key = md5_encrypt(sql)
        self.cache_count = 0
        self.page_size = int(page_size)
        self.page_no = int(page_no)
        self.limit_str = ''
        self.set_limit()

    def get_count_sql(self):
        return 'select count(0)  from (%s) newTable' % self.sql

    def _get_count(self):
        count_sql = self.get_count_sql()
        result = execute_raw_sql(count_sql, use_dict=False)
        return result[0][0]

    @cached_property
    def count(self):
        self.cache_count = cache.get(self.md5_key)
        if self.cache_count is None:
            self.cache_count = self._get_count()
            cache.set(self.md5_key, self.cache_count, 60 * 10)
        return self.cache_count

    def get_query_sql(self):
        return '%s %s' % (self.sql, self.limit_str)

    def set_limit(self):
        """设置sql limit
        """
        self.limit_str = 'limit %s,%s' % ((self.page_no - 1) * self.page_size, self.page_size)

    def get_results(self, alias='default', use_dict=True):
        query_sql = self.get_query_sql()
        return execute_raw_sql(query_sql, alias, use_dict)

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0:
            return 0
        return ceil(self.count / self.page_size)
