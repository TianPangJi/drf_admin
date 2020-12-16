# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : roles.py
@create   : 2020/7/22 21:30
"""
from rest_framework import serializers

from system.models import Roles


class RolesSerializer(serializers.ModelSerializer):
    """
    角色管理序列化器
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions', 'desc', 'create_time']
        extra_kwargs = {
            'permissions': {
                'read_only': True,
            },
        }


class RolesPartialSerializer(serializers.ModelSerializer):
    """
    用户局部更新序列化器(角色授权)
    """

    class Meta:
        model = Roles
        fields = ['id', 'permissions']

    def validate(self, attrs):
        permissions = attrs.get('permissions')
        for permission in permissions:
            if permission.pid and permission.pid not in permissions:
                raise serializers.ValidationError('缺失父节点权限')
        return attrs
