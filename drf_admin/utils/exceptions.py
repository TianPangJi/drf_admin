"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : exceptions.py
@create   : 2020/7/11 13:44
"""
import logging
import traceback

from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.views import set_rollback
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status, exceptions

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('error')


def errors_handler(exc):
    """
    自定义, 错误消息格式处理
    :param exc:
    :return: data: 错误消息
    """
    try:
        if isinstance(exc.detail, list):
            msg = ''.join([str(x) for x in exc.detail])
        elif isinstance(exc.detail, dict):
            msg = ''
            for k, v in exc.detail.items():
                if k == 'non_field_errors':
                    if isinstance(v, list):
                        msg += ''.join([str(x) for x in v])
                    else:
                        msg += str(v)
                else:
                    if isinstance(v, list):
                        msg = str(k) + ':' + ''.join([str(x) for x in v])
            if not msg:
                msg = exc.detail
        else:
            msg = exc.detail
    except Exception:
        msg = exc.detail
    data = {'detail': msg}
    return data


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
        data = errors_handler(exc)
        set_rollback()
        response = Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
        # 数据库异常
        view = context['view']
        logger.error('[%s] %s' % (view, traceback.format_exc()))
        response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    else:
        # 未知错误
        view = context['view']
        logger.error('[%s] %s' % (view, traceback.format_exc()))
        response = Response({'detail': '服务端未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
