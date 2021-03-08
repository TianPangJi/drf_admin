# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : redis.py
@create   : 2021/2/28 18:17
"""
import uuid

from django_redis import get_redis_connection


def acquire_lock(lock_name: str, time_out: int = 10, cache_name: str = 'default'):
    """
    获取redis全局锁
    :param lock_name: 锁名称
    :param time_out: 失效时间
    :param cache_name: redis库名称配置
    :return: uuid
    """
    conn = get_redis_connection(cache_name)
    if conn.exists(lock_name):
        return ''
    else:
        uid = uuid.uuid4().hex
        conn.set(lock_name, uid)
        conn.expire(lock_name, time_out)
        return uid


def release_lock(lock_name: str, uid, cache_name: str = 'default'):
    """
    释放redis锁
    :param lock_name: 锁名称
    :param uid: key的value值
    :param cache_name: redis库名称配置
    :return: None
    """
    conn = get_redis_connection(cache_name)
    if conn.exists(lock_name):
        value = conn.get(lock_name).decode()
        if value == uid:
            conn.delete(lock_name)
