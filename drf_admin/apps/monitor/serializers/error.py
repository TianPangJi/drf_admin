# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : error.py
@create   : 2020/10/3 16:26
"""
from rest_framework import serializers

from monitor.models import ErrorLogs


class ErrorLogsSerializer(serializers.ModelSerializer):
    """
    错误日志序列化器
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = ErrorLogs
        fields = '__all__'
