# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : signals.py
@create   : 2021/2/14 17:40
"""
import json
import logging

from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django_redis import get_redis_connection

from system.models import Permissions


@receiver(pre_save, sender=Permissions)
def update_permissions_to_redis(sender, instance, **kwargs):
    """
    Permissions模型,更新时更新redis
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    conn = get_redis_connection('user_info')
    if instance.id:
        if not instance.menu:
            # 接口权限,判断权限path的变化,更新redis
            try:
                permission = Permissions.objects.get(id=instance.id)
            except Permissions.DoesNotExist:
                return
            if permission.path != instance.path:
                # 路径更改,删除原有记录并新增一条权限记录
                if conn.hexists('user_permissions_manage', permission.path):
                    permissions = json.loads(conn.hget('user_permissions_manage', permission.path))
                    for index, value in enumerate(permissions):
                        if value.get('id') == instance.id:
                            del permissions[index]
                    if permissions:
                        conn.hset('user_permissions_manage', permission.path, json.dumps(permissions))
                    else:
                        conn.hdel('user_permissions_manage', permission.path)
                if conn.hexists('user_permissions_manage', instance.path):
                    # 如存在路径记录, 添加
                    permissions = json.loads(conn.hget('user_permissions_manage', instance.path))
                    permissions.append({
                        'method': instance.method,
                        'sign': instance.sign,
                        'id': instance.id,
                    })
                    conn.hset('user_permissions_manage', instance.path, json.dumps(permissions))
                else:
                    # 否则新增
                    conn.hset('user_permissions_manage', instance.path, json.dumps([{
                        'method': instance.method,
                        'sign': instance.sign,
                        'id': instance.id,
                    }]))
            else:
                # 路径未变,更改原有权限记录
                if permission.method != instance.method or permission.sign != instance.sign:
                    permissions = json.loads(conn.hget('user_permissions_manage', instance.path))
                    for permission in permissions:
                        if permission.get('id') == instance.id:
                            permission['method'] = instance.method
                            permission['sign'] = instance.sign
                    conn.hset('user_permissions_manage', instance.path, json.dumps(permissions))
        else:
            # 菜单权限,判断是否由接口权限改为菜单权限,如果是则删除原有记录
            try:
                permission = Permissions.objects.get(id=instance.id)
            except Permissions.DoesNotExist:
                return
            if not permission.menu and conn.hexists('user_permissions_manage', permission.path):
                permissions = json.loads(conn.hget('user_permissions_manage', permission.path))
                for index, value in enumerate(permissions):
                    if value.get('id') == instance.id:
                        del permissions[index]
                if permissions:
                    conn.hset('user_permissions_manage', permission.path, json.dumps(permissions))
                else:
                    conn.hdel('user_permissions_manage', permission.path)


@receiver(post_save, sender=Permissions)
def create_permissions_to_redis(sender, instance, **kwargs):
    """
    Permissions模型,创建时更新redis
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if not instance.menu and kwargs.get('created'):
        conn = get_redis_connection('user_info')
        if conn.exists('user_permissions_manage') and conn.hexists('user_permissions_manage', instance.path):
            permissions = json.loads(conn.hget('user_permissions_manage', instance.path))
            permissions.append({
                'method': instance.method,
                'sign': instance.sign,
                'id': instance.id,
            })
            conn.hset('user_permissions_manage', instance.path, json.dumps(permissions))
        else:
            conn.hset('user_permissions_manage', instance.path, json.dumps([{
                'method': instance.method,
                'sign': instance.sign,
                'id': instance.id,
            }]))


@receiver(pre_delete, sender=Permissions)
def delete_permissions_from_redis(sender, instance, **kwargs):
    """
    Permissions模型,删除时更新redis
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if not instance.menu:
        conn = get_redis_connection('user_info')
        if conn.exists('user_permissions_manage') and conn.hexists('user_permissions_manage', instance.path):
            permissions = json.loads(conn.hget('user_permissions_manage', instance.path))
            for index, permission in enumerate(permissions):
                if permission.get('id') == instance.id:
                    del permissions[index]
            if permissions:
                conn.hset('user_permissions_manage', instance.path, json.dumps(permissions))
            else:
                conn.hdel('user_permissions_manage', instance.path)
