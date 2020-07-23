""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : roles.py 
@create   : 2020/6/27 17:55 
"""
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from drf_admin.utils.views import MultipleDestroyMixin
from system.models import Roles
from system.serializers.roles import RolesSerializer


class RolesViewSet(ModelViewSet, MultipleDestroyMixin):
    """
    create:
    角色--增加

    destroy:
    角色--删除

    multiple_delete:
    角色--批量删除

    update:
    角色--修改

    list:
    角色--获取列表
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
