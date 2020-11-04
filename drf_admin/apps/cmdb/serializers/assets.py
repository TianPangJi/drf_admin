# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : assets.py
@create   : 2020/10/31 9:29
"""
from rest_framework import serializers

from oauth.models import Users


class AssetsAdminSerializers(serializers.ModelSerializer):
    """资产管理员序列化器"""

    class Meta:
        model = Users
        fields = ['id', 'username']
