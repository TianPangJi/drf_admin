"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : roles.py
@create   : 2020/7/22 21:30
"""
from rest_framework import serializers

from system.models import Roles


class RolesSerializer(serializers.ModelSerializer):
    """角色管理序列化器"""

    class Meta:
        model = Roles
        fields = '__all__'
