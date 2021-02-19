# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : users.py
@create   : 2020/7/1 22:33
"""
import re

from django.conf import settings
from rest_framework import serializers

from oauth.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    用户增删改查序列化器
    """
    roles_list = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    department_name = serializers.ReadOnlyField(source='department.name')
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'mobile', 'email', 'is_active', 'department', 'department_name',
                  'date_joined', 'roles', 'roles_list', 'is_superuser']

    def validate(self, attrs):
        # 数据验证
        if attrs.get('username'):
            if attrs.get('username').isdigit():
                raise serializers.ValidationError('用户名不能为纯数字')
        if attrs.get('mobile'):
            if not re.match(r'^1[3-9]\d{9}$', attrs.get('mobile')):
                raise serializers.ValidationError('手机格式不正确')
        if attrs.get('mobile') == '':
            attrs['mobile'] = None
        return attrs

    def get_roles_list(self, obj):
        return [{'id': role.id, 'desc': role.desc} for role in obj.roles.all()]

    def create(self, validated_data):
        user = super().create(validated_data)
        # 添加默认密码
        user.set_password(settings.DEFAULT_PWD)
        user.save()
        return user


class UsersPartialSerializer(serializers.ModelSerializer):
    """
    用户局部更新(激活/锁定)序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'is_active']


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    重置密码序列化器
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # partial_update, 局部更新required验证无效, 手动验证数据
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if not password:
            raise serializers.ValidationError('字段password为必填项')
        if not confirm_password:
            raise serializers.ValidationError('字段confirm_password为必填项')
        if password != confirm_password:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    def save(self, **kwargs):
        # 重写save方法, 保存密码
        self.instance.set_password(self.validated_data.get('password'))
        self.instance.save()
        return self.instance
