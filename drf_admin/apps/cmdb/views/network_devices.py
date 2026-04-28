# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : network_devices.py
@create   : 2020/10/17 18:45
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from cmdb.models import NetworkDevices
from cmdb.serializers.network_devices import NetworkDevicesAssetsSerializer
from cmdb.views.assets import BaseAssetsAPIView
from drf_admin.utils.views import ChoiceAPIView


class NetworkDevicesViewSet(BaseAssetsAPIView):
    """
    create:
    网络设备--新增

    网络设备新增, status: 201(成功), return: 新增网络设备信息

    destroy:
    网络设备--删除

    网络设备删除, status: 204(成功), return: None

    multiple_delete:
    网络设备--批量删除

    网络设备批量删除, status: 204(成功), return: None

    update:
    网络设备--修改

    网络设备修改, status: 200(成功), return: 修改增网络设备信息

    partial_update:
    网络设备--局部修改

    网络设备局部修改, status: 200(成功), return: 修改增网络设备信息

    list:
    网络设备--获取列表

    网络设备列表信息, status: 200(成功), return: 网络设备信息列表

    retrieve:
    网络设备--网络设备详情

    网络设备详情信息, status: 200(成功), return: 单个网络设备信息详情
    """
    serializer_class = NetworkDevicesAssetsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['asset_status']
    search_fields = ('name', 'sn', 'manage_ip')
    ordering_fields = ('id', 'name', 'sn')

    def get_queryset(self, **kwargs):
        return super().get_queryset(asset_type='network')


class NetworkDevicesTypeAPIView(ChoiceAPIView):
    """
    get:
    网络设备--models类型列表

    网络设备models中的类型列表信息, status: 200(成功), return: 网络设备models中的类型列表
    """
    choice = NetworkDevices.device_type_choice
