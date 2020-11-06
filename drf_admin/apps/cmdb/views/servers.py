# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : servers.py
@create   : 2020/10/17 18:45
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from cmdb.models import Servers
from cmdb.serializers.servers import ServersAssetsSerializer
from cmdb.views.assets import BaseAssetsAPIView
from drf_admin.utils.views import ChoiceAPIView


class ServersViewSet(BaseAssetsAPIView):
    """
    create:
    服务器--新增

    服务器新增, status: 201(成功), return: 新增服务器信息

    destroy:
    服务器--删除

    服务器删除, status: 204(成功), return: None

    multiple_delete:
    服务器--批量删除

    服务器批量删除, status: 204(成功), return: None

    update:
    服务器--修改

    服务器修改, status: 200(成功), return: 修改增服务器信息

    partial_update:
    服务器--局部修改

    服务器局部修改, status: 200(成功), return: 修改增服务器信息

    list:
    服务器--获取列表

    服务器列表信息, status: 200(成功), return: 服务器信息列表

    retrieve:
    服务器--服务器详情

    服务器详情信息, status: 200(成功), return: 单个服务器信息详情
    """
    serializer_class = ServersAssetsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['asset_status']
    search_fields = ('name', 'sn', 'manage_ip')
    ordering_fields = ('id', 'name', 'sn')

    def get_queryset(self, **kwargs):
        return super().get_queryset(asset_type='server')


class ServersSystemTypeAPIView(ChoiceAPIView):
    """
    get:
    服务器--models系统类型列表

    服务器models中的系统类型列表信息, status: 200(成功), return: 服务器models中的系统类型列表
    """
    choice = Servers.server_system_type_choice


class ServersTypeAPIView(ChoiceAPIView):
    """
    get:
    服务器--models类型列表

    服务器models中的类型列表信息, status: 200(成功), return: 服务器models中的类型列表
    """
    choice = Servers.server_type_choice
