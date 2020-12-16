# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : departments.py
@create   : 2020/7/29 21:29
"""
from rest_framework import serializers

from drf_admin.utils.views import TreeSerializer
from system.models import Departments


class DepartmentsSerializer(serializers.ModelSerializer):
    """
    部门管理序列化器
    """

    class Meta:
        model = Departments
        fields = '__all__'


class DepartmentsTreeSerializer(TreeSerializer):
    """
    部门数据序列化器(Element Tree)
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Departments
        fields = '__all__'
