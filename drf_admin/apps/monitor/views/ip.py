# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : ip.py
@create   : 2020/10/3 19:05
"""
from rest_framework.filters import SearchFilter

from drf_admin.utils.views import AdminViewSet
from monitor.models import IpBlackList
from monitor.serializers.ip import IpBlackListSerializer


class IpBlackListViewSet(AdminViewSet):
    """
    create:
    监控--IP黑名单增加

    IP黑名单增加, status: 201(成功), return: 新增黑名单IP

    destroy:
    监控--IP黑名单删除

    IP黑名单删除, status: 204(成功), return: None

    multiple_delete:
    监控--IP黑名单批量删除

    IP黑名单批量删除, status: 204(成功), return: None

    update:
    监控--IP黑名单修改

    角色修改, status: 200(成功), return: 修改增ip信息

    list:
    监控--IP黑名单列表

    IP黑名单列表, status: 200(成功), return: IP黑名单列表信息

    retrieve:
    监控--IP黑名单ip详情

    黑名单ip详情信息, status: 200(成功), return: 单个黑名单ip详情
    """
    queryset = IpBlackList.objects.all()
    serializer_class = IpBlackListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('ip',)
