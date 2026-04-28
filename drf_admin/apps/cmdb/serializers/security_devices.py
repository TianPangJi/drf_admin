# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : security_devices.py
@create   : 2020/10/17 18:45
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from cmdb.models import SecurityDevices
from cmdb.serializers.assets import BaseAssetsSerializer


class SecurityDevicesSerializer(WritableNestedModelSerializer):
    """
    安全设备序列化器
    """
    asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SecurityDevices
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['device_type_display'] = instance.get_device_type_display()
        return ret


class SecurityDevicesAssetsSerializer(BaseAssetsSerializer):
    """
    安全设备资产序列化器
    """
    security = SecurityDevicesSerializer()

    def save(self, **kwargs):
        instance = super(SecurityDevicesAssetsSerializer, self).save(**kwargs)
        instance.asset_type = 'security'
        instance.save()
        return instance
