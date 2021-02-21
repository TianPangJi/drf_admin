# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : users.py
@create   : 2020/6/27 17:55
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_admin.apps.system.serializers.users import UsersSerializer, UsersPartialSerializer, ResetPasswordSerializer
from drf_admin.utils.views import AdminViewSet
from oauth.models import Users
from system.filters.users import UsersFilter
from system.models import Permissions


class UsersViewSet(AdminViewSet):
    """
    create:
    用户--新增

    用户新增, status: 201(成功), return: 新增用户信息

    destroy:
    用户--删除

    用户删除, status: 204(成功), return: None

    multiple_delete:
    用户--批量删除

    用户批量删除, status: 204(成功), return: None

    update:
    用户--修改

    用户修改, status: 200(成功), return: 修改后的用户信息

    partial_update:
    用户--局部修改

    用户局部修改(激活/锁定), status: 200(成功), return: 修改后的用户信息

    list:
    用户--获取列表

    用户列表信息, status: 200(成功), return: 用户信息列表

    retrieve:
    用户--详情
    
    用户详情信息, status: 200(成功), return: 单个用户信息详情
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = UsersFilter
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UsersPartialSerializer
        else:
            return UsersSerializer


class ResetPasswordAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    patch:
    用户--重置密码

    用户重置密码, status: 200(成功), return: None
    """
    queryset = Users.objects.all()
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PermissionsAPIView(APIView):
    """
    get:
    用户--获取用户拥有权限ID列表

    获取用户拥有权限ID列表, status: 200(成功), return: 用户拥有权限ID列表
    """

    def get(self, request, pk):
        try:
            user = Users.objects.get(id=pk)
        except Users.DoesNotExist:
            raise ValidationError('无效的用户ID')
        # admin角色
        if 'admin' in user.roles.values_list('name', flat=True) or user.is_superuser:
            return Response(data={'results': Permissions.objects.values_list('id', flat=True)})
        # 其他角色
        return Response(data={'results': list(filter(None, set(user.roles.values_list('permissions__id', flat=True))))})
