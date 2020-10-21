# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : servers.py
@create   : 2020/10/17 18:45
"""
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from cmdb.models import Assets, Servers
from cmdb.serializers.servers import ServersAssetsSerializers
from drf_admin.utils.views import AdminViewSet
from system.models import Departments


class ServersViewSet(AdminViewSet):
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

    serializer_class = ServersAssetsSerializers
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['asset_status']
    search_fields = ('name', 'sn', 'manage_ip')
    ordering_fields = ('id', 'name', 'sn')

    def get_queryset(self):
        # ①管理员角色用户可查看所有
        if {'name': 'admin'} in self.request.user.roles.values('name'):
            return Assets.objects.filter(asset_type='server')
        # ②每个用户只能查看到所属部门及其子部门下的服务器, 及该用户管理服务器
        departments = self.__get_user_departments(self.request.user.department.id,
                                                  set(str(self.request.user.department.id)))
        return (Assets.objects.filter(asset_type='server').filter(
            Q(department__in=departments) | Q(admin=self.request.user))).distinct()

    def __get_user_departments(self, department_id, department_ids_set):
        # 获取该请求用户所属部门及其子部门的部门id集合
        departments = Departments.objects.filter(pid=department_id)
        for department in departments:
            department_ids_set.add(str(department.id))
            self.__get_user_departments(department, department_ids_set)
        return department_ids_set


class ServersSystemTypeAPIView(APIView):
    """
    get:
    服务器--models系统类型列表

    服务器models中的系统类型列表信息, status: 200(成功), return: 服务器models中的系统类型列表
    """

    def get(self, request):
        methods = [{'value': value[0], 'label': value[1]} for value in Servers.server_system_type_choice]
        return Response(data={'results': methods})


class ServersTypeAPIView(APIView):
    """
    get:
    服务器--models类型列表

    服务器models中的类型列表信息, status: 200(成功), return: 服务器models中的类型列表
    """

    def get(self, request):
        methods = [{'value': value[0], 'label': value[1]} for value in Servers.server_type_choice]
        return Response(data={'results': methods})
