# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py
@create   : 2020/9/9 20:08
"""
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from monitor.models import OnlineUsers
from monitor.serializers.users import OnlineUsersSerializer


class OnlineUsersListAPIView(ListAPIView):
    """
    get:
    监控--在线用户

    获取在线用户信息, status: 200(成功), return: 在线用户信息
    """

    queryset = OnlineUsers.objects.all()
    serializer_class = OnlineUsersSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('user__username', 'ip')
