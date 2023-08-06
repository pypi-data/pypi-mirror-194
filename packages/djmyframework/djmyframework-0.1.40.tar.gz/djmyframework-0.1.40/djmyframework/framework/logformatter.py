import logging

from .utils import string_color, read_1970_time
from django.db import connection
from django.conf import settings

class JsonPrettyFormatter:
    NO_PRINT = ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                'thread', 'threadName', 'processName', 'process']

    def format_default(self, record: logging.LogRecord) -> str:
        header = (f'【{record.levelname}】{read_1970_time(record.msecs)}\n'
                  f'rid: {record.__dict__["request_id"]}\n')
        for i in record.__dict__:
            if i not in self.NO_PRINT:
                header += f'{i}: {string_color(record.__dict__[i], "white")}\n'
        return header

    def format_info(self, record: logging.LogRecord) -> str:
        record.__dict__['container_id'] = getattr(settings, 'CONTAINER_ID', '')
        if record.__dict__.get('category') == 'error':
            return (f'【错误】{read_1970_time(record.created)}\n'
                    f'rid: {record.__dict__["request_id"]}\n'
                    f'uri: {record.__dict__["path"]}\n'
                    f'{record.__dict__["method"]}: {string_color(record.msg, "cyan")}\n'
                    f'-----EXCEPT BEGIN-----\n'
                    f'{string_color(record.__dict__["except"], "red")}'
                    f'-----EXCEPT END-----\n')
        if record.__dict__.get('category') == 'response':
            if settings.DEBUG:
                record.__dict__['queries'] = len(connection.queries)
            return (f'【返回请求】{read_1970_time(record.created)}\n'
                    f'rid: {record.__dict__["request_id"]} cost_timez: {record.__dict__["cost_timez"]} queries: {record.__dict__.get("queries")} \n'
                    f'uri: {record.__dict__["path"]} client_ip: {record.__dict__.get("client_ip")}\n'
                    f'{record.__dict__["method"]}: {string_color(record.msg, "cyan")}\n'
                    f'response: {string_color(record.__dict__["response"], "green")}\n')
        if record.__dict__.get('category') == 'request':
            return (f'【发起请求】{read_1970_time(record.created)}\n'
                    f'rid: {record.__dict__["request_id"]}\n'
                    f'uri: {record.__dict__["path"]}\n'
                    f'{record.__dict__["method"]}: {string_color(record.msg, "cyan")}\n'
                    f'response: {string_color(record.__dict__["response"], "blue")}')
        return self.format_default(record)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname == 'INFO':
            return self.format_info(record)
        return self.format_default(record)
