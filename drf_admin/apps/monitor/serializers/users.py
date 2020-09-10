# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py
@create   : 2020/9/9 20:11
"""
from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import Users


class OnlineUsersSerializer(serializers.ModelSerializer):
    """
    在线用户监控
    """
    ip = serializers.SerializerMethodField()
    browser = serializers.SerializerMethodField()
    os = serializers.SerializerMethodField()
    last_time = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'ip', 'browser', 'os', 'last_time']

    def get_ip(self, obj):
        conn = get_redis_connection('online_user')
        return conn.hget(f'online_user_{obj.id}', 'ip').decode()

    def get_browser(self, obj):
        conn = get_redis_connection('online_user')
        return conn.hget(f'online_user_{obj.id}', 'browser').decode()

    def get_os(self, obj):
        conn = get_redis_connection('online_user')
        return conn.hget(f'online_user_{obj.id}', 'os').decode()

    def get_last_time(self, obj):
        conn = get_redis_connection('online_user')
        return conn.hget(f'online_user_{obj.id}', 'last_time').decode()
