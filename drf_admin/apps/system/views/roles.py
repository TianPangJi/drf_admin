""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : roles.py 
@create   : 2020/6/27 17:55 
"""
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import UpdateAPIView

from drf_admin.utils.views import AdminViewSet
from system.models import Roles
from system.serializers.roles import RolesSerializer


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

    角色修改, status: 200(成功), return: 修改增角色信息

    partial_update:
    角色--局部修改

    角色局部修改, status: 200(成功), return: 修改增角色信息

    list:
    角色--获取列表

    角色列表信息, status: 200(成功), return: 角色信息列表
    """
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'desc')
    ordering_fields = ('id', 'name')

# class RoleOauthAPIView(UpdateAPIView):
#     """
#
#     """
#     serializer_class = RoleOauthSerializer
#     queryset = Roles.objects.all()
