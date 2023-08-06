# coding:utf-8
# django 连接数据库的东东


from django.db import connections


def reconnect_db(alias='default'):
    try:
        connections[alias].connection.ping()
    except:
        connections[alias].close()


def reconnect_all_db():
    # connection.ensure_connection()    # 自带方法只能重置 default 连接
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()
