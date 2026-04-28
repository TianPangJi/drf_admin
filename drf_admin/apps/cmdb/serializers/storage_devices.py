# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : storage_devices.py
@create   : 2020/10/17 18:45
"""
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from cmdb.models import StorageDevices
from cmdb.serializers.assets import BaseAssetsSerializer


class StorageDevicesSerializer(WritableNestedModelSerializer):
    """
    存储设备序列化器
    """
    asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StorageDevices
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['device_type_display'] = instance.get_device_type_display()
        return ret


class StorageDevicesAssetsSerializer(BaseAssetsSerializer):
    """
    存储设备资产序列化器
    """
    storage = StorageDevicesSerializer()

    def save(self, **kwargs):
        instance = super(StorageDevicesAssetsSerializer, self).save(**kwargs)
        instance.asset_type = 'storage'
        instance.save()
        return instance
