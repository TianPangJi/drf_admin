# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : assets.py
@create   : 2020/10/31 9:29
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from cmdb.models import Assets
from oauth.models import Users


class AssetsAdminSerializer(serializers.ModelSerializer):
    """
    资产管理员序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'username']


class BaseAssetsSerializer(WritableNestedModelSerializer):
    """
    资产基类序列化器, 仅用于继承, (并重写save方法,填写asset_type默认属性)
    """
    asset_type = serializers.CharField(read_only=True)

    class Meta:
        model = Assets
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 添加choices中文显示
        ret['asset_type_display'] = instance.get_asset_type_display()
        ret['asset_status_display'] = instance.get_asset_status_display()
        if instance.department:
            ret['department_display'] = instance.department.name
        else:
            ret['department_display'] = ''
        if instance.admin:
            ret['admin_display'] = instance.admin.username
        else:
            ret['admin_display'] = ''
        if instance.cabinet:
            ret['cabinet_display'] = instance.cabinet.name
            if instance.cabinet.idc:
                ret['idc'] = instance.cabinet.idc.name
            else:
                ret['idc'] = ''
        else:
            ret['cabinet_display'] = ''
            ret['idc'] = ''
        return ret
