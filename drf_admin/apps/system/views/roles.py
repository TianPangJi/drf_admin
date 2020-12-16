# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : roles.py
@create   : 2020/6/27 17:55
"""
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from drf_admin.utils.views import AdminViewSet
from system.models import Roles
from system.serializers.roles import RolesSerializer, RolesPartialSerializer


class RolesViewSet(AdminViewSet):
    """
    create:
    角色--新增

    角色新增, status: 201(成功), return: 新增角色信息

    destroy:
    角色--删除

    角色删除, status: 204(成功), return: None

    multiple_delete:
    角色--批量删除

    角色批量删除, status: 204(成功), return: None

    update:
    角色--修改

    角色修改, status: 200(成功), return: 修改后的角色信息

    partial_update:
    角色--局部修改(角色授权)

    角色局部修改, status: 200(成功), return: 修改后的角色信息

    list:
    角色--获取列表

    角色列表信息, status: 200(成功), return: 角色信息列表
    """
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'desc')
    ordering_fields = ('id', 'name')

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return RolesPartialSerializer
        else:
            return RolesSerializer

    def update(self, request, *args, **kwargs):
        if self.get_object().name == 'admin':
            return Response(data={'detail': 'admin角色不可修改'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().name == 'admin':
            return Response(data={'detail': 'admin角色不可删除'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if self.get_object().name == 'admin':
            return Response(data={'detail': 'admin角色, 默认拥有所有权限'}, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)

    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        try:
            admin = Roles.objects.get(name='admin')
            if isinstance(delete_ids, list):
                if admin.id in delete_ids:
                    return Response(data={'detail': 'admin角色不可删除'}, status=status.HTTP_400_BAD_REQUEST)
        except Roles.DoesNotExist:
            pass
        return super().multiple_delete(request, *args, **kwargs)
