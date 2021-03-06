# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : assets.py
@create   : 2020/10/21 19:44
"""
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cmdb.models import Assets, IDC, Cabinets
from cmdb.serializers.assets import AssetsAdminSerializer
from drf_admin.common.models import get_child_ids
from drf_admin.utils.views import ChoiceAPIView, AdminViewSet
from oauth.models import Users
from system.models import Departments


class AssetsStatusAPIView(ChoiceAPIView):
    """
    get:
    资产--models状态列表

    资产models中的状态列表信息, status: 200(成功), return: 资产models中的状态列表
    """
    choice = Assets.asset_status_choice


class AssetsAdminListAPIView(ListAPIView):
    """
    get:
    资产--管理员查询

    资产管理员列表信息, status: 200(成功), return: 资产管理员列表信息
    """
    queryset = Users.objects.all()
    serializer_class = AssetsAdminSerializer
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


class BaseAssetsAPIView(AdminViewSet):
    """
    资产基类, 仅用于继承, 重写get_queryset且指定asset_type
    eg:
        def get_queryset(self):
            return super().get_queryset(asset_type='server')
    """

    def get_queryset(self, **kwargs):
        # 解决drf-yasg加载报错
        if isinstance(self.request.user, AnonymousUser):
            return Assets.objects.none()
        asset_type = kwargs.get('asset_type')
        assert asset_type is not None, '关键字参数asset_type, 为必传参数'
        assert asset_type in [values[0] for values in
                              Assets.asset_type_choice], 'asset_type应存在与Assets.asset_type_choice'
        return Assets.objects.filter(asset_type=asset_type)
        # # 管理员角色用户可查看所有
        # if {'name': 'admin'} in self.request.user.roles.values('name'):
        #     return Assets.objects.filter(asset_type=asset_type)
        # # 每个用户只能查看到所属部门及其子部门下的服务器, 及该用户管理服务器
        # if self.request.user.department:
        #     departments = get_child_ids(self.request.user.department.id, Departments)
        #     return (Assets.objects.filter(asset_type=asset_type).filter(
        #         Q(department__in=departments) | Q(admin=self.request.user))).distinct()
        # else:
        #     return Assets.objects.filter(asset_type=asset_type, admin=self.request.user)
