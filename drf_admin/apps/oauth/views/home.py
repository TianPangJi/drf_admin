# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : home.py
@create   : 2020/11/25 20:31
"""
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cmdb.models import Assets
from monitor.models import OnlineUsers

Users = get_user_model()


class HomeAPIView(APIView):
    """
    get:
    系统首頁--数据显示

    获取系统首頁数据, status: 200(成功), return: 系统首頁数据
    """

    def get(self, request):
        data = dict()
        conn = get_redis_connection('user_info')
        data['visits'] = int(conn.get('visits').decode()
                             ) if conn.get('visits') else 0
        data['users'] = Users.objects.all().count()
        data['online_users'] = OnlineUsers.objects.all().count()
        data['assets'] = Assets.objects.all().count()
        return Response(data=data, status=status.HTTP_200_OK)
