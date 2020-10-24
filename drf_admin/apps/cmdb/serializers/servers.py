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

from cmdb.models import Accounts, Servers, Assets


class AccountsSerializers(serializers.ModelSerializer):
    """服务器登录账户序列化器"""
    server = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Accounts
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['password'] = instance.get_password_display()
        return ret


class ServersSerializers(WritableNestedModelSerializer):
    """服务器序列化器"""
    accounts = AccountsSerializers(many=True)  # 使用model中指定的related_name, 防止意外Bug
    asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Servers
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['server_type_display'] = instance.get_server_type_display()
        ret['server_system_type_display'] = instance.get_server_system_type_display()
        return ret


class ServersAssetsSerializers(WritableNestedModelSerializer):
    """服务器资产序列化器"""
    server = ServersSerializers()  # 使用model中指定的related_name, 防止意外Bug
    asset_type = serializers.CharField(read_only=True, default='server')

    class Meta:
        model = Assets
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 添加choices中文显示
        ret['asset_type_display'] = instance.get_asset_type_display()
        ret['asset_status_display'] = instance.get_asset_status_display()
        if instance.department:
            ret['department_display'] = instance.department.name()
        else:
            ret['department_display'] = ''
        if instance.admin:
            ret['admin_display'] = instance.admin.username()
        else:
            ret['admin_display'] = ''
        if instance.cabinet:
            ret['cabinet_display'] = instance.cabinet.name()
        else:
            ret['cabinet_display'] = ''
        if instance.cabinet.idc:
            ret['idc'] = instance.cabinet.idc.name()
        else:
            ret['idc'] = ''
        return ret
