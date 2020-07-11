"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : exceptions.py
@create   : 2020/7/11 13:44
"""
import logging
from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.views import set_rollback
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status, exceptions

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义异常处理, 捕获或有异常
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            # data = exc.detail
            data = {'detail': exc.detail}
        else:
            data = {'detail': exc.detail}
        set_rollback()
        response = Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
        # 数据库异常
        view = context['view']
        logger.error('[%s] %s' % (view, exc))
        response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    else:
        # 未知错误
        view = context['view']
        logger.error('[%s] %s' % (view, exc))
        response = Response({'detail': '服务端未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
