# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : storage_devices.py
@create   : 2020/10/17 18:45
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from cmdb.models import StorageDevices
from cmdb.serializers.storage_devices import StorageDevicesAssetsSerializer
from cmdb.views.assets import BaseAssetsAPIView
from drf_admin.utils.views import ChoiceAPIView


class StorageDevicesViewSet(BaseAssetsAPIView):
    """
    create:
    存储设备--新增

    存储设备新增, status: 201(成功), return: 新增存储设备信息

    destroy:
    存储设备--删除

    存储设备删除, status: 204(成功), return: None

    multiple_delete:
    存储设备--批量删除

    存储设备批量删除, status: 204(成功), return: None

    update:
    存储设备--修改

    存储设备修改, status: 200(成功), return: 修改增存储设备信息

    partial_update:
    存储设备--局部修改

    存储设备局部修改, status: 200(成功), return: 修改增存储设备信息

    list:
    存储设备--获取列表

    存储设备列表信息, status: 200(成功), return: 存储设备信息列表

    retrieve:
    存储设备--存储设备详情

    存储设备详情信息, status: 200(成功), return: 单个存储设备信息详情
    """
    serializer_class = StorageDevicesAssetsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['asset_status']
    search_fields = ('name', 'sn', 'manage_ip')
    ordering_fields = ('id', 'name', 'sn')

    def get_queryset(self, **kwargs):
        return super().get_queryset(asset_type='storage')


class StorageDevicesTypeAPIView(ChoiceAPIView):
    """
    get:
    存储设备--models类型列表

    存储设备models中的类型列表信息, status: 200(成功), return: 存储设备models中的类型列表
    """
    choice = StorageDevices.device_type_choice
