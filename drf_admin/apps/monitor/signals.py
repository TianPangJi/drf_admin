# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : signals.py
@create   : 2020/10/6 13:46
"""

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django_redis import get_redis_connection

from .models import IpBlackList


@receiver(pre_save, sender=IpBlackList)
def create_update_ip_black_list(sender, instance, **kwargs):
    """
    IP黑名单创建及更新信号处理
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    conn = get_redis_connection('user_info')
    ip_id = instance.id
    if ip_id:
        # 更新IP黑名单, 更新redis黑名单IP
        conn.srem('ip_black_list', IpBlackList.objects.get(id=instance.id).ip)
        conn.sadd('ip_black_list', instance.ip)

    else:
        # 新增IP黑名单, 添加redis黑名单IP
        conn.sadd('ip_black_list', instance.ip)


@receiver(post_delete, sender=IpBlackList)
def delete_ip_black_list(sender, instance, **kwargs):
    """
    IP黑名单删除时信号处理
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # 删除IP黑名单时, 删除redis黑名单中的IP
    conn = get_redis_connection('user_info')
    conn.srem('ip_black_list', instance.ip)
