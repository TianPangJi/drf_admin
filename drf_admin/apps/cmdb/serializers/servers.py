# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : servers.py
@create   : 2020/10/17 18:45
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from cmdb.models import Accounts, Servers
from cmdb.serializers.assets import BaseAssetsSerializer


class AccountsSerializer(serializers.ModelSerializer):
    """
    服务器登录账户序列化器
    """
    server = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Accounts
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['password'] = instance.get_password_display('password')
        return ret


class ServersSerializer(WritableNestedModelSerializer):
    """
    服务器序列化器
    """
    accounts = AccountsSerializer(many=True)  # 使用model中指定的related_name, 防止意外Bug
    asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Servers
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['server_type_display'] = instance.get_server_type_display()
        ret['server_system_type_display'] = instance.get_server_system_type_display()
        return ret


class ServersAssetsSerializer(BaseAssetsSerializer):
    """
    服务器资产序列化器
    """
    server = ServersSerializer()  # 使用model中指定的related_name, 防止意外Bug

    def save(self, **kwargs):
        # 添加默认asset_type为server
        instance = super(ServersAssetsSerializer, self).save(**kwargs)
        instance.asset_type = 'server'
        instance.save()
        return instance
