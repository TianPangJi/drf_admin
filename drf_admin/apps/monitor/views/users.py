# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py
@create   : 2020/9/9 20:08
"""
from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView

from monitor.serializers.users import OnlineUsersSerializer
from oauth.models import Users


class OnlineUsersListAPIView(ListAPIView):
    """
    get:
    监控--在线用户

    获取在线用户信息, status: 200(成功), return: 在线用户信息
    """

    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        conn = get_redis_connection('online_user')
        user_ids = [value.decode().split('_')[-1] for value in conn.keys('online_user_*')]
        queryset = Users.objects.filter(id__in=user_ids)
        return queryset
