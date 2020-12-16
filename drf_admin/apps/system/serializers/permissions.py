# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py
@create   : 2020/7/22 21:44
"""
from rest_framework import serializers

from drf_admin.utils.views import TreeSerializer
from system.models import Permissions


class PermissionsSerializer(serializers.ModelSerializer):
    """
    权限管理序列化器
    """

    class Meta:
        model = Permissions
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('menu') is True:
            if attrs.get('method', '') != '' or attrs.get('path', '') != '':
                raise serializers.ValidationError('菜单权限, 方法与路径必须为空')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('menu') is False:
            if Permissions.objects.filter(pid=instance.id, menu=True):
                raise serializers.ValidationError('菜单权限存在子菜单, 请先修改子菜单')
        if validated_data.get('pid'):
            if Permissions.objects.filter(id=validated_data.get('pid').id, menu=False):
                raise serializers.ValidationError('菜单父权限必须为菜单权限')
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if validated_data.get('pid'):
            if Permissions.objects.filter(id=validated_data.get('pid').id, menu=False):
                raise serializers.ValidationError('菜单父权限必须为菜单权限')
        return super().create(validated_data)


class PermissionsTreeSerializer(TreeSerializer):
    """
    权限数据序列化器(Element Tree)
    """

    class Meta:
        model = Permissions
        fields = '__all__'
