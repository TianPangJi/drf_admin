# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : security_devices.py
@create   : 2020/10/17 18:45
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from cmdb.models import SecurityDevices
from cmdb.serializers.security_devices import SecurityDevicesAssetsSerializer
from cmdb.views.assets import BaseAssetsAPIView
from drf_admin.utils.views import ChoiceAPIView


class SecurityDevicesViewSet(BaseAssetsAPIView):
    """
    create:
    安全设备--新增

    安全设备新增, status: 201(成功), return: 新增安全设备信息

    destroy:
    安全设备--删除

    安全设备删除, status: 204(成功), return: None

    multiple_delete:
    安全设备--批量删除

    安全设备批量删除, status: 204(成功), return: None

    update:
    安全设备--修改

    安全设备修改, status: 200(成功), return: 修改增安全设备信息

    partial_update:
    安全设备--局部修改

    安全设备局部修改, status: 200(成功), return: 修改增安全设备信息

    list:
    安全设备--获取列表

    安全设备列表信息, status: 200(成功), return: 安全设备信息列表

    retrieve:
    安全设备--安全设备详情

    安全设备详情信息, status: 200(成功), return: 单个安全设备信息详情
    """
    serializer_class = SecurityDevicesAssetsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['asset_status']
    search_fields = ('name', 'sn', 'manage_ip')
    ordering_fields = ('id', 'name', 'sn')

    def get_queryset(self, **kwargs):
        return super().get_queryset(asset_type='security')


class SecurityDevicesTypeAPIView(ChoiceAPIView):
    """
    get:
    安全设备--models类型列表

    安全设备models中的类型列表信息, status: 200(成功), return: 安全设备models中的类型列表
    """
    choice = SecurityDevices.device_type_choice
