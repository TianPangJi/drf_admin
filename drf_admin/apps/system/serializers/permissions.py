# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py
@create   : 2020/7/22 21:44
"""
from rest_framework import serializers

from drf_admin.common.models import get_child_ids
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
        else:
            if attrs.get('method', '') == '' or attrs.get('path', '') == '':
                raise serializers.ValidationError('接口权限, 方法与路径为必传参数')
            path = str(attrs.get('path'))
            if not all([path.startswith('/'), path.endswith('/')]):
                raise serializers.ValidationError('请求路径必须以"/"开头及结尾')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('menu') is False:
            if Permissions.objects.filter(pid=instance.id, menu=True):
                raise serializers.ValidationError('菜单权限存在子菜单, 请先修改子菜单')
        if validated_data.get('pid'):
            if Permissions.objects.filter(id=validated_data.get('pid').id, menu=False):
                raise serializers.ValidationError('菜单父权限必须为菜单权限')
            permissions_id = get_child_ids(instance.id, Permissions)
            if validated_data.get('pid').id in permissions_id:
                raise serializers.ValidationError('父权限不能为其本身或其子权限')
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
