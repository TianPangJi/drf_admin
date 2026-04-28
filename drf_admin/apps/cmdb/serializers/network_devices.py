# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : network_devices.py
@create   : 2020/10/17 18:45
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from cmdb.models import NetworkDevices
from cmdb.serializers.assets import BaseAssetsSerializer


class NetworkDevicesSerializer(WritableNestedModelSerializer):
    """
    网络设备序列化器
    """
    asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NetworkDevices
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['device_type_display'] = instance.get_device_type_display()
        return ret


class NetworkDevicesAssetsSerializer(BaseAssetsSerializer):
    """
    网络设备资产序列化器
    """
    network = NetworkDevicesSerializer()

    def save(self, **kwargs):
        instance = super(NetworkDevicesAssetsSerializer, self).save(**kwargs)
        instance.asset_type = 'network'
        instance.save()
        return instance
