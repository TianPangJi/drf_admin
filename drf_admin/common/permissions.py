# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : permissions.py
@create   : 2021/2/14 17:11
"""
import json

from system.models import Permissions


def redis_storage_permissions(redis_conn):
    permissions = Permissions.objects.filter(menu=False).values('id', 'path', 'method', 'sign')
    # 如果还没有任何权限控制，直接跳过后续逻辑，以免报错
    if not permissions.exists():
        return None

    permissions_dict = dict()
    for permission in permissions:
        # 去除不可见字符
        method = str(permission.get('method')).replace('\u200b', '')
        path = str(permission.get('path')).replace('\u200b', '')
        sign = str(permission.get('sign')).replace('\u200b', '')
        _id = permission.get('id')
        if permissions_dict.get(path):
            permissions_dict[path].append({
                'method': method,
                'sign': sign,
                'id': _id,
            })
        else:
            permissions_dict[path] = [{
                'method': method,
                'sign': sign,
                'id': _id,
            }]
    for key in permissions_dict:
        permissions_dict[key] = json.dumps(permissions_dict[key])
    redis_conn.hmset('user_permissions_manage', permissions_dict)
