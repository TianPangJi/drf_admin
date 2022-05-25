# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : centre.py
@create   : 2020/11/7 14:06
"""
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser

from information.serializers.centre import ChangePasswordSerializer, ChangeInformationSerializer, ChangeAvatarSerializer


class ChangePasswordAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改密码

    个人中心修改密码, status: 200(成功), return: None
    """
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class ChangeInformationAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改个人信息

    个人中心修改个人信息, status: 200(成功), return: 修改后的个人信息
    """
    serializer_class = ChangeInformationSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class ChangeAvatarAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改个人头像

    个人中心修改个人头像, status: 200(成功), return: 修改后的个人信息
    """
    serializer_class = ChangeAvatarSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
