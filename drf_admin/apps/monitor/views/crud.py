# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : crud.py
@create   : 2020/12/9 20:40
"""
from easyaudit.models import CRUDEvent
from rest_framework.generics import ListAPIView

from monitor.serializers.crud import CRUDSerializer


class CRUDListAPIView(ListAPIView):
    """
    get:
    监控--CRUD变更记录列表

    CRUD变更记录列表, status: 200(成功), return: CRUD变更记录列表信息
    """
    serializer_class = CRUDSerializer

    def get_queryset(self):
        return CRUDEvent.objects.exclude(object_repr__istartswith='OnlineUsers')
