# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : notification.py
@create   : 2020/11/17 22:11
"""
import threading
import time

from django.conf import settings
from redis import StrictRedis

from monitor.models import OnlineUsers


def online_user_notifications():
    """
    在线用户, redis key过期后空间通知
    :return: None
    """
    conn = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3, password=settings.REDIS_PWD)
    pub_sub = conn.pubsub()

    def user_offline(msg):
        online_user_key = msg.get('data').decode()
        user_list = str(online_user_key).split('_')
        OnlineUsers.objects.filter(user=user_list[2], ip=user_list[3]).delete()

    pub_sub.psubscribe(**{'__keyevent@3__:expired': user_offline})
    while 1:
        pub_sub.get_message()
        time.sleep(0.2)


t = threading.Thread(target=online_user_notifications)
t.setDaemon(True)
t.start()
