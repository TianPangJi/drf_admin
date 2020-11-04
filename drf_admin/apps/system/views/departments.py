# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : departments.py
@create   : 2020/7/29 21:27
"""

from rest_framework.filters import SearchFilter, OrderingFilter

from drf_admin.utils.views import AdminViewSet, TreeAPIView
from system.models import Departments
from system.serializers.departments import DepartmentsSerializer, DepartmentsTreeSerializer


class DepartmentsViewSet(AdminViewSet, TreeAPIView):
    """
    create:
    部门--新增

    部门新增, status: 201(成功), return: 新增部门信息

    destroy:
    部门--删除

    部门删除, status: 204(成功), return: None

    multiple_delete:
    部门--批量删除

    部门批量删除, status: 204(成功), return: None

    update:
    部门--修改

    部门修改, status: 200(成功), return: 修改增部门信息

    partial_update:
    部门--局部修改

    部门局部修改, status: 200(成功), return: 修改增部门信息

    list:
    部门--获取列表

    部门列表信息, status: 200(成功), return: 部门信息列表
    """
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id', 'name')

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentsTreeSerializer
        else:
            return DepartmentsSerializer
