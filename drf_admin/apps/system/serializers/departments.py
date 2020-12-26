# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : departments.py
@create   : 2020/7/29 21:29
"""
from rest_framework import serializers

from drf_admin.common.models import get_child_ids
from drf_admin.utils.views import TreeSerializer
from system.models import Departments


class DepartmentsSerializer(serializers.ModelSerializer):
    """
    部门管理序列化器
    """

    class Meta:
        model = Departments
        fields = '__all__'

    def update(self, instance, validated_data):
        # 验证服部门父部门不能为其本身或其子部门
        departments_id = get_child_ids(instance.id, Departments)
        if validated_data.get('pid') and validated_data.get('pid').id in departments_id:
            raise serializers.ValidationError('父部门不能为其本身或其子部门')
        return super().update(instance, validated_data)


class DepartmentsTreeSerializer(TreeSerializer):
    """
    部门数据序列化器(Element Tree)
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Departments
        fields = '__all__'
