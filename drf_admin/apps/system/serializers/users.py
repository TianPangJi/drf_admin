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
from system.models import Roles


class UsersSerializer(serializers.ModelSerializer):
    """
    用户增删改查序列化器
    """
    roles_list = serializers.SerializerMethodField()
    roles = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, queryset=Roles.objects.all())

    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'mobile', 'email', 'is_active', 'roles', 'roles_list']

    def validate(self, attrs):
        # 数据验证
        if attrs.get('mobile'):
            if not re.match(r'^1[3-9]\d{9}$', attrs.get('mobile')):
                raise serializers.ValidationError('手机格式不正确')
        return attrs

    def get_roles_list(self, obj):
        return [{'id': role.id, 'desc': role.desc} for role in obj.roles.all()]

    def create(self, validated_data):
        validated_data['password'] = settings.DEFAULT_PWD
        user = Users.objects.create_user(**validated_data)
        return user


class UsersPartialSerializer(serializers.ModelSerializer):
    """
    用户局部更新序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'is_active']
