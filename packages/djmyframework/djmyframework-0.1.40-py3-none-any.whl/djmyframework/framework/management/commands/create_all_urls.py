# coding:utf-8
import traceback
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, reverse
from framework.urls import create_all_ulrs_py_file


class Command(BaseCommand):
    help = '创建所有请求URL 文件描述,%s ' % __file__

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        create_all_ulrs_py_file()
