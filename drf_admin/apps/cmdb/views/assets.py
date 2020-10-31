# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : assets.py
@create   : 2020/10/21 19:44
"""
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cmdb.models import Assets
from cmdb.serializers.assets import AssetsAdminSerializers
from oauth.models import Users


class AssetsStatusAPIView(APIView):
    """
    get:
    资产--models状态列表

    资产models中的状态列表信息, status: 200(成功), return: 资产models中的状态列表
    """

    def get(self, request):
        methods = [{'value': value[0], 'label': value[1]} for value in Assets.asset_status_choice]
        return Response(data={'results': methods})


class AssetsAdminListAPIView(ListAPIView):
    """
    get:
    资产--管理员查询

    资产管理员列表信息, status: 200(成功), return: 资产管理员列表信息
    """
    queryset = Users.objects.all()
    serializer_class = AssetsAdminSerializers
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
