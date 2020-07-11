""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py 
@create   : 2020/7/1 22:33 
"""
import re
from django.conf import settings
from rest_framework import serializers

from oauth.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    用户增删改查序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'mobile', 'email', 'is_active']

        # extra_kwargs = {
        #     'username': {
        #         'write_only': True,
        #         'max_length': 20,
        #         'min_length': 4,
        #         'error_messages': {
        #             'unique': '用户已存在',
        #             'max_length': '密码过长'
        #         }
        #     },
        # }

        def validate(self, attrs):
            # 数据验证
            if attrs.get('mobile'):
                if not re.match(r'^1[3-9]\d{9}$', attrs.get('mobile')):
                    raise serializers.ValidationError('手机格式不正确')
            return attrs

        def create(self, validated_data):
            validated_data['password'] = settings.DEFAULT_PWD
            user = Users.objects.create_user(**validated_data)
            return user
