""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py 
@create   : 2020/7/1 22:33 
"""
from rest_framework import serializers

from drf_admin.apps.oauth.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    用户增删改查序列化器
    """

    class Meta:
        model = Users
        fields = '__all__'
