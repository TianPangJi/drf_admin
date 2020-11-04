# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : error.py
@create   : 2020/10/3 16:18
"""
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from monitor.models import ErrorLogs
from monitor.serializers.error import ErrorLogsSerializer


class ErrorLogAPIView(ListAPIView):
    """
    get:
    监控--错误日志列表

    错误日志列表, status: 200(成功), return: 错误日志列表信息

    delete:
    监控--错误日志清空

    错误日志清空, status: 204(成功), return: None
    """
    queryset = ErrorLogs.objects.all()
    serializer_class = ErrorLogsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'view', 'desc', 'ip')

    def delete(self, request):
        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
