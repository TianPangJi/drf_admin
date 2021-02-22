# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : middleware.py
@create   : 2020/8/21 21:46
"""
import json
import logging
import time

from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response

from monitor.models import OnlineUsers
from oauth.utils import get_request_browser, get_request_os, get_request_ip


class OperationLogMiddleware:
    """
    操作日志Log记录
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.operation_logger = logging.getLogger('operation')  # 记录非GET操作日志
        self.query_logger = logging.getLogger('query')  # 记录GET查询操作日志

    def __call__(self, request):
        try:
            request_body = json.loads(request.body)
        except Exception:
            request_body = dict()
        if request.method == "GET":
            request_body.update(dict(request.GET))
            logger = self.query_logger
        else:
            request_body.update(dict(request.POST))
            logger = self.operation_logger
        # 处理密码, log中密码已******替代真实密码
        for key in request_body:
            if 'password' in key:
                request_body[key] = '******'
        response = self.get_response(request)
        try:
            response_body = response.data
            # 处理token, log中token已******替代真实token值
            if response_body['data'].get('token'):
                response_body['data']['token'] = '******'
        except Exception:
            response_body = dict()
        log_info = f'[{request.user} [Request: {request.method} {request.path} {request_body}] ' \
                   f'[Response: {response.status_code} {response.reason_phrase} {response_body}]]'
        if response.status_code >= 500:
            logger.error(log_info)
        elif response.status_code >= 400:
            logger.warning(log_info)
        else:
            logger.info(log_info)
        return response


class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = '请求失败'
                detail = response.data.get('detail')
                code = 1
                data = {}
            elif response.status_code == 200 or response.status_code == 201:
                msg = '成功'
                detail = ''
                code = 200
                data = response.data
            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        return response


class OnlineUsersMiddleware(MiddlewareMixin):
    """
    在线用户监测, (采用类心跳机制,10分钟内无任何操作则任务该用户已下线)
    """

    def process_response(self, request, response):
        if request.user.is_authenticated:
            conn = get_redis_connection('online_user')
            last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            request_ip = get_request_ip(request)
            # redis + django orm 实现在线用户监测
            if conn.exists(f'online_user_{request.user.id}_{request_ip}'):
                conn.hset(f'online_user_{request.user.id}_{request_ip}', 'last_time', last_time)
            else:
                online_info = {'ip': request_ip, 'browser': get_request_browser(request),
                               'os': get_request_os(request), 'last_time': last_time}
                conn.hmset(f'online_user_{request.user.id}_{request_ip}', online_info)
                if not OnlineUsers.objects.filter(user=request.user, ip=request_ip).exists():
                    OnlineUsers.objects.create(**{'user': request.user, 'ip': request_ip})
            # key过期后, 使用redis空间通知, 使用户下线
            conn.expire(f'online_user_{request.user.id}_{request_ip}', 10 * 60)
        return response


class IpBlackListMiddleware(MiddlewareMixin):
    """
    IP黑名单校验中间件
    """

    def process_request(self, request):
        request_ip = get_request_ip(request)
        # 在redis中判断IP是否在IP黑名单中/
        conn = get_redis_connection('user_info')
        if conn.sismember('ip_black_list', request_ip):
            from django.http import HttpResponse
            return HttpResponse('IP已被拉入黑名单, 请联系管理员', status=status.HTTP_400_BAD_REQUEST)
