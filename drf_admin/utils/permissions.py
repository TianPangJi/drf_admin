""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : permissions.py 
@create   : 2020/6/28 21:52 
"""
import json
import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from drf_admin.common.permissions import redis_storage_permissions


class UserLock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '用户已被锁定,请联系管理员'
    default_code = 'not_authenticated'


class RbacPermission(BasePermission):
    """
    自定义权限认证
    """

    @staticmethod
    def pro_uri(uri):
        base_api = settings.BASE_API
        uri = '/' + base_api + '/' + uri + '/'
        return re.sub('/+', '/', uri)

    def has_permission(self, request, view):
        # 验证用户是否被锁定
        if not request.user.is_active:
            raise UserLock()
        request_url = request.path
        # 如果请求url在白名单，放行
        for safe_url in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=safe_url), request_url):
                return True
        # admin权限放行
        conn = get_redis_connection('user_info')
        if conn.exists('user_info_%s' % request.user.id):
            user_permissions = json.loads(conn.hget('user_info_%s' % request.user.id, 'permissions').decode())
            if 'admin' in user_permissions:
                return True
        else:
            user_permissions = []
            if 'admin' in request.user.roles.values_list('name', flat=True):
                return True
        # RBAC权限验证
        # Step 1 验证redis中是否存储权限数据
        request_method = request.method
        if not conn.exists('user_permissions_manage'):
            redis_storage_permissions(conn)
        # Step 2 判断请求路径是否在权限控制中
        url_keys = conn.hkeys('user_permissions_manage')
        for url_key in url_keys:
            if re.match(settings.REGEX_URL.format(url=self.pro_uri(url_key.decode())), request_url):
                redis_key = url_key.decode()
                break
        else:
            return True
        # Step 3 redis权限验证
        permissions = json.loads(conn.hget('user_permissions_manage', redis_key).decode())
        method_hit = False  # 同一接口配置不同权限验证
        for permission in permissions:
            if permission.get('method') == request_method:
                method_hit = True
                if permission.get('sign') in user_permissions:
                    return True
        else:
            if method_hit:
                return False
            else:
                return True
