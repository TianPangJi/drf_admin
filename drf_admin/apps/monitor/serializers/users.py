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

from monitor.models import OnlineUsers


class OnlineUsersSerializer(serializers.ModelSerializer):
    """
    在线用户监控
    """
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    browser = serializers.SerializerMethodField()
    os = serializers.SerializerMethodField()
    last_time = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = OnlineUsers
        fields = ['id', 'username', 'name', 'ip', 'browser', 'os', 'last_time', 'create_time']

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_name(self, obj):
        return obj.user.name

    def get_browser(self, obj):
        conn = get_redis_connection(f'online_user')
        browser = conn.hget(f'online_user_{obj.user.id}_{obj.ip}', 'browser')
        return browser.decode() if browser else ''

    def get_os(self, obj):
        conn = get_redis_connection(f'online_user')
        os = conn.hget(f'online_user_{obj.user.id}_{obj.ip}', 'os')
        return os.decode() if os else ''

    def get_last_time(self, obj):
        conn = get_redis_connection(f'online_user')
        last_time = conn.hget(f'online_user_{obj.user.id}_{obj.ip}', 'last_time')
        return last_time.decode() if last_time else ''
