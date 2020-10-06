# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : departments.py
@create   : 2020/7/29 21:29
"""

from rest_framework import serializers

from system.models import Departments


class DepartmentsSerializer(serializers.ModelSerializer):
    """
    部门管理序列化器
    """

    class Meta:
        model = Departments
        fields = '__all__'


class DepartmentsTreeSerializer(serializers.ModelSerializer):
    """
    部门数据序列化器(Element Tree)
    """

    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Departments
        fields = '__all__'
