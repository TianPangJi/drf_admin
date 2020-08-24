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

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


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
        if request_body.get('password'):
            request_body['password'] = '******'
        response = self.get_response(request)
        try:
            response_body = response.data
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
    eg: {}
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json' and isinstance(
                response.data, dict):
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
