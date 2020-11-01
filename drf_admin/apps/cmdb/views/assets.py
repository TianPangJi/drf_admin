# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : assets.py
@create   : 2020/10/21 19:44
"""
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cmdb.models import Assets, IDC, Cabinets
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


class IDCCabinetsTreeAPIView(APIView):
    """
    get:
    资产--机房机柜Tree

    获取机房机柜Tree, status: 200(成功), return: 机房机柜Tree结构数据
    """

    def get(self, request):
        idc_queryset = IDC.objects.all()
        data = []
        for idc in idc_queryset:
            cabinet_queryset = Cabinets.objects.filter(idc=idc.id)
            if cabinet_queryset:
                idc_data = dict()
                idc_data['value'] = str(idc.id) + str(idc.name)
                idc_data['label'] = idc.name
                idc_data['children'] = list()
                for cabinet in cabinet_queryset:
                    cabinet_data = dict()
                    cabinet_data['value'] = cabinet.id
                    cabinet_data['label'] = cabinet.name
                    idc_data['children'].append(cabinet_data)
                data.append(idc_data)
            else:
                continue
        return Response(data={'results': data}, status=status.HTTP_200_OK)
