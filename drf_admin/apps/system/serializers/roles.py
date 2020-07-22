"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : roles.py
@create   : 2020/7/22 21:30
"""
from rest_framework import serializers

from system.models import Roles, Permissions


class RolesSerializer(serializers.ModelSerializer):
    """角色管理序列化器"""

    class Meta:
        model = Roles
        fields = '__all__'


class RoleOauthSerializer(serializers.ModelSerializer):
    """角色授权"""
    permissions_list = serializers.SerializerMethodField()
    permissions = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True,
                                                     queryset=Permissions.objects.all())

    class Meta:
        model = Roles
        fields = ['id', 'permissions', 'permissions_list']

    def get_permissions_list(self, obj):
        # 待修改
        return [{'id': permission.id, 'desc': permission.desc} for permission in obj.permissions.all()]
