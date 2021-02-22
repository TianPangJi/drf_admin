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
from django.db import DatabaseError
from django.http import Http404
from redis.exceptions import RedisError
from rest_framework import status, exceptions
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import set_rollback

# 获取在配置文件中定义的logger，用来记录日志
from monitor.models import ErrorLogs
from oauth.utils import get_request_ip

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
            def search_error(detail: dict, message: str):
                for k, v in detail.items():
                    if k == 'non_field_errors':
                        if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                            message += ''.join([str(x) for x in v])
                        else:
                            message += str(v)
                    else:
                        if isinstance(v, list) and isinstance(v[0], ErrorDetail):
                            message += str(k)
                            message += ''.join([str(x) for x in v])
                        elif isinstance(v, list) and isinstance(v[0], dict):
                            for value_dict in v:
                                message = search_error(value_dict, message)
                return message

            msg = ''
            msg = search_error(exc.detail, msg)
        else:
            msg = exc.detail
        if not msg:
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
        # 数据库记录异常
        detail = traceback.format_exc()
        write_error_logs(exc, context, detail)
        logger.error('[%s] %s' % (view, detail))
        response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    else:
        # 未知错误
        view = context['view']
        # 数据库记录异常
        detail = traceback.format_exc()
        write_error_logs(exc, context, detail)
        logger.error('[%s] %s' % (view, detail))
        response = Response({'detail': '服务端未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


def write_error_logs(exc, context, detail):
    """
    记录错误日志信息
    :param exc: 异常
    :param context: 抛出异常的上下文
    :param detail: 异常详情
    :return:
    """
    data = {
        'username': context['request'].user.username if context['request'].user.username else 'AnonymousUser',
        'view': context['view'].get_view_name(),
        'desc': exc.__str__(),
        'ip': get_request_ip(context['request']),
        'detail': detail
    }
    ErrorLogs.objects.create(**data)
