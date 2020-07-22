# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py
@create   : 2020/7/22 21:44
"""
from rest_framework import serializers

from system.models import Permissions


class PermissionsSerializer(serializers.ModelSerializer):
    """
    权限管理序列化器
    """

    class Meta:
        model = Permissions
        fields = '__all__'
