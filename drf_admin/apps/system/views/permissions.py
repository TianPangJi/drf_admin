""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py 
@create   : 2020/6/27 17:56 
"""
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from drf_admin.utils.views import MultipleDestroyMixin
from system.models import Permissions
from system.serializers.permissions import PermissionsSerializer


class PermissionsViewSet(ModelViewSet, MultipleDestroyMixin):
    """
    create:
    权限--增加

    destroy:
    权限--删除

    multiple_delete:
    权限--批量删除

    update:
    权限--修改

    list:
    权限--获取列表
    """
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'desc', 'path')
    ordering_fields = ('id', 'name')
